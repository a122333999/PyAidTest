from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDockWidget


class DockWidget(QDockWidget):
    def __init__(self):
        super().__init__()
        self._hintWidth = -1
        self._hintHeight = -1
