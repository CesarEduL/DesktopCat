import sys
from PyQt6.QtWidgets import QApplication
from cat import DesktopCat


def main():
    app = QApplication(sys.argv)
    cat = DesktopCat()
    cat.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
