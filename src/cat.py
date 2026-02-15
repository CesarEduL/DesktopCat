import os
import sys
import random
from enum import Enum
from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtCore import Qt, QTimer, QPoint


class CatState(Enum):
    QUIETO = 0
    CAMINANDO = 1
    IDLE = 2
    ESPECIAL = 3
    CAYENDO = 4
    ATERRIZAJE = 5
    ARRASTRANDO = 6
    AGARRADO = 7


class DesktopCat(QLabel):
    TARGET_WIDTH = 46
    TARGET_HEIGHT = 44

    def __init__(self):
        super().__init__()

        # -------- Cargar y redimensionar imágenes --------
        # Ejecutable (PyInstaller): recursos en sys._MEIPASS
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets_path = os.path.join(base_path, "assets")

        def load_image(name):
            pix = QPixmap(os.path.join(assets_path, name))
            return pix.scaled(self.TARGET_WIDTH, self.TARGET_HEIGHT,
                              Qt.AspectRatioMode.IgnoreAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)

        self.img_quieto = load_image("gato.png")
        self.img_walk1 = load_image("gato1.png")
        self.img_walk2 = load_image("gato2.png")
        self.img_idle = load_image("gato3.png")
        self.img_special = load_image("gato4.png")
        self.img_fall = load_image("gato5.png")
        self.img_land = load_image("gato6.png")
        self.img_catch = load_image("gato7.png")

        self.setPixmap(self.img_quieto)
        self.resize(self.TARGET_WIDTH, self.TARGET_HEIGHT)

        # -------- Ventana --------
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().availableGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        self.ground_y = self.screen_height - self.height()

        self.move(0, self.ground_y)

        # -------- Variables --------
        self.state = CatState.QUIETO
        self.direction = 1
        self.speed = 5
        self.current_frame = 0
        self.dragging = False
        self.offset = QPoint()
        self.fall_speed = 0

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
            self.set_cat_image(self.img_fall)

        self.move(self.x(), new_y)

    def finish_landing(self):
        if self.state == CatState.ATERRIZAJE:
            self.state = CatState.QUIETO

    # ==================================================
    #                 EVENTO ESPECIAL
    # ==================================================
    def trigger_special(self):
        if self.state not in [CatState.ARRASTRANDO, CatState.CAYENDO]:
            self.state = CatState.ESPECIAL
            self.set_cat_image(self.img_special)
            QTimer.singleShot(2000, self.end_special)

    def end_special(self):
        if self.state == CatState.ESPECIAL:
            self.state = CatState.QUIETO

    # ==================================================
    #                 ARRASTRAR
    # ==================================================
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.state = CatState.ARRASTRANDO
            self.set_cat_image(self.img_catch)
            self.offset = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        if self.y() < self.ground_y:
            self.state = CatState.CAYENDO
        else:
            self.state = CatState.QUIETO
