# -*- coding:utf-8 -*-

from PySide6.QtWidgets import QWidget, QLabel


class BoxImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel("BoxImageWidget", self)

    def setFilePath(self, filePath: str):
        self._filePath = filePath

    def getFilePath(self):
        return self._filePath