from PySide6.QtCore import QSize
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget, QTextEdit

class LogWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._textEdit = QTextEdit()

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._textEdit)

    def clearContent(self):
        pass

    def sizeHint(self):
        return QSize(-1, 150)

