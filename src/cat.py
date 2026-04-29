import os
import sys
import random
from enum import Enum
from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect


class CatState(Enum):
    QUIETO = 0
    CAMINANDO = 1
    IDLE = 2
    ESPECIAL = 3
    CAYENDO = 4
    ATERRIZAJE = 5
    ARRASTRANDO = 6
    AGARRADO = 7
    JUGANDO = 8


class DesktopCat(QLabel):
    TARGET_WIDTH = 46
    TARGET_HEIGHT = 44

    def __init__(self):
        super().__init__()

        # -------- Cargar y redimensionar imágenes --------
        # Ejecutable (PyInstaller): recursos en sys._MEIPASS
        if getattr(sys, "frozen", False):
            base_path = getattr(sys, "_MEIPASS", None)
            if base_path is None:
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets_path = os.path.join(base_path, "assets")

        def load_image(name):
            pix = QPixmap(os.path.join(assets_path, name))
            # // redimensionado a 46x44 en tiempo de ejecución
            return pix.scaled(self.TARGET_WIDTH, self.TARGET_HEIGHT,
                              Qt.AspectRatioMode.IgnoreAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)

        def load_optional_image(name):
            path = os.path.join(assets_path, name)
            if os.path.exists(path):
                return load_image(name)
            return self.img_special

        self.img_quieto = load_image("gato.png")
        self.img_walk1 = load_image("gato1.png")
        self.img_walk2 = load_image("gato2.png")
        self.img_idle = load_image("gato3.png")
        self.img_special = load_image("gato4.png")
        self.img_fall = load_image("gato5.png")
        self.img_land = load_image("gato6.png")
        self.img_catch = load_image("gato7.png")
        self.img_play = load_optional_image("gato8.png")
        self.img_jump = load_optional_image("gato9.png")
        self.img_roll = load_optional_image("gato10.png")
        self.img_stealth = load_optional_image("gato11.png")

        self.setPixmap(self.img_quieto)
        self.resize(self.TARGET_WIDTH, self.TARGET_HEIGHT)

        # -------- Ventana --------
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        screen = QApplication.primaryScreen()
        if screen is None:
            screens = QApplication.screens()
            screen = screens[0] if screens else None
        if screen is not None:
            geometry = screen.availableGeometry()
        else:
            geometry = QRect(0, 0, 800, 600)
        self.screen_width = geometry.width()
        self.screen_height = geometry.height()
        self.ground_y = self.screen_height - self.height()

        self.move(0, self.ground_y)

        # -------- Variables --------
        self.state = CatState.QUIETO
        self.direction = 1
        self.speed = 5
        self.current_frame = 0
        self.dragging = False
        self.mouse_pressed = False
        self.offset = QPoint()
        self.fall_speed = 0
        self.game_active = False
        self.game_score = 0
        self.press_pos = QPoint()
        self.status_label = QLabel(self)
        self.status_label.setStyleSheet(
            "color: white; background-color: rgba(0, 0, 0, 160);"
            "border-radius: 6px; padding: 4px; font-size: 11px;"
        )
        self.status_label.hide()
        self.status_label.move(0, 0)
        self.status_label.resize(self.TARGET_WIDTH, 24)

        # -------- Timers --------
        self.timer_main = QTimer()
        self.timer_main.timeout.connect(self.update_behavior)
        self.timer_main.start(100)  # 10 FPS suficiente para suavidad

        self.timer_special = QTimer()
        self.timer_special.timeout.connect(self.trigger_special)
        self.timer_special.start(25000)  # cada 25 seg

        self.timer_frame = QTimer()
        self.timer_frame.timeout.connect(self.animate_walk)
        self.timer_frame.start(200)  # cambio de frame caminar

        self.timer_game = QTimer(self)
        self.timer_game.timeout.connect(self.move_game_target)

    # ==================================================
    #                 UTILIDAD VOLTEAR
    # ==================================================
    def set_cat_image(self, pixmap):
        if self.direction == -1:
            transform = QTransform().scale(-1, 1)
            self.setPixmap(pixmap.transformed(transform))
        else:
            self.setPixmap(pixmap)

    # ==================================================
    #                 LÓGICA PRINCIPAL
    # ==================================================
    def update_behavior(self):
        if self.game_active:
            return

        if self.state == CatState.ARRASTRANDO:
            return

        if self.state == CatState.CAMINANDO:
            self.walk()
        elif self.state == CatState.IDLE:
            self.set_cat_image(self.img_idle)
        elif self.state == CatState.QUIETO:
            self.set_cat_image(self.img_quieto)
        elif self.state == CatState.CAYENDO:
            self.fall()
        elif self.state == CatState.ATERRIZAJE:
            self.set_cat_image(self.img_land)
        elif self.state == CatState.ESPECIAL:
            self.set_cat_image(self.img_special)
        elif self.state == CatState.JUGANDO:
            self.set_cat_image(self.img_play)
            

        # Cambio aleatorio de comportamiento solo si no está cayendo o especial
        if self.state not in [CatState.CAYENDO, CatState.ESPECIAL, CatState.ARRASTRANDO]:
            if random.randint(1, 50) == 1:
                self.state = random.choice(
                    [CatState.CAMINANDO, CatState.IDLE, CatState.QUIETO])

    # ==================================================
    #                 CAMINAR
    # ==================================================
    def walk(self):
        x = self.x() + self.speed * self.direction

        # Rebotar en bordes
        if x <= 0:
            self.direction = 1
        elif x + self.width() >= self.screen_width:
            self.direction = -1

        self.move(self.x() + self.speed * self.direction, self.ground_y)

    def animate_walk(self):
        if self.state == CatState.CAMINANDO:
            if self.current_frame == 0:
                self.set_cat_image(self.img_walk1)
                self.current_frame = 1
            else:
                self.set_cat_image(self.img_walk2)
                self.current_frame = 0

    # ==================================================
    #                 CAÍDA + ATERRIZAJE
    # ==================================================
    def fall(self):
        self.fall_speed += 2
        new_y = self.y() + self.fall_speed

        if new_y >= self.ground_y:
            new_y = self.ground_y
            self.fall_speed = 0
            self.state = CatState.ATERRIZAJE
            self.set_cat_image(self.img_land)
            QTimer.singleShot(500, self.finish_landing)
        else:
            if self.fall_speed < 0:
                self.set_cat_image(self.img_special)
            else:
                self.set_cat_image(self.img_fall)

        self.move(self.x(), new_y)

    def finish_landing(self):
        if self.state == CatState.ATERRIZAJE:
            self.state = CatState.QUIETO
            self.status_label.hide()

    # ==================================================
    #                 EVENTO ESPECIAL
    # ==================================================
    def trigger_special(self):
        if self.state not in [CatState.ARRASTRANDO, CatState.CAYENDO]:
            self.trigger_special_action()

    def trigger_special_action(self):
        if self.state in [CatState.ARRASTRANDO, CatState.CAYENDO, CatState.JUGANDO]:
            return

        action = random.choice(['salto', 'rueda', 'acecha'])
        self.state = CatState.ESPECIAL
        self.set_cat_image(self.img_special)
        if action == 'salto':
            self.status_label.setText('¡Salto especial!')
            self.status_label.show()
            self.jump()
            QTimer.singleShot(2000, self.end_special)
        elif action == 'rueda':
            self.status_label.setText('¡Acrobacia felina!')
            self.status_label.show()
            self.set_cat_image(self.img_roll)
            QTimer.singleShot(2000, self.end_special)
        else:
            self.status_label.setText('¡El gato acecha!')
            self.status_label.show()
            self.set_cat_image(self.img_stealth)
            QTimer.singleShot(2000, self.end_special)

    def end_special(self):
        if self.state == CatState.ESPECIAL:
            self.state = CatState.QUIETO
            self.status_label.hide()

    def jump(self):
        if self.state in [CatState.CAYENDO, CatState.ARRASTRANDO]:
            return
        self.fall_speed = -16
        self.state = CatState.CAYENDO
        self.set_cat_image(self.img_jump)

    # ==================================================
    #                 ARRASTRAR
    # ==================================================
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.trigger_special_action()
            return

        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = True
            self.press_pos = event.globalPosition().toPoint()
            self.dragging = False
            self.offset = self.press_pos - self.pos()

    def mouseMoveEvent(self, event):
        if not self.mouse_pressed:
            return

        current_pos = event.globalPosition().toPoint()
        if not self.dragging and (current_pos - self.press_pos).manhattanLength() > 6:
            self.dragging = True
            self.state = CatState.ARRASTRANDO
            self.set_cat_image(self.img_catch)

        if self.dragging:
            self.move(current_pos - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.game_active and not self.dragging:
            self.increment_game_score()

        self.dragging = False
        self.mouse_pressed = False
        if self.game_active:
            return

        if self.y() < self.ground_y:
            self.state = CatState.CAYENDO
        else:
            self.state = CatState.QUIETO

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_play_game()

    def start_play_game(self):
        if self.game_active or self.state == CatState.ARRASTRANDO:
            return

        self.game_active = True
        self.game_score = 0
        self.state = CatState.JUGANDO
        self.set_cat_image(self.img_special)
        self.status_label.setText('Juego: atrapa al gato! 0')
        self.status_label.show()
        self.timer_game.start(700)
        QTimer.singleShot(10000, self.end_play_game)

    def move_game_target(self):
        x = random.randint(0, self.screen_width - self.width())
        y = random.randint(0, self.screen_height - self.height())
        self.move(x, y)

    def increment_game_score(self):
        self.game_score += 1
        self.status_label.setText(f'Juego: atrapa al gato! {self.game_score}')

    def end_play_game(self):
        self.game_active = False
        self.timer_game.stop()
        self.state = CatState.QUIETO
        self.status_label.setText(f'Juego terminado: {self.game_score}')
        QTimer.singleShot(2000, self.status_label.hide)
