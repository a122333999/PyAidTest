import sys

from PySide6.QtWidgets import QApplication
from Widget import window


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = window.MainWindow()
    window.show()
    sys.exit(app.exec())


