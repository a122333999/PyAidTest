# -*- coding:utf-8 -*-

from PySide6.QtCore import QFile
from PySide6.QtWidgets import QWidget, QTextEdit, QLabel, QVBoxLayout


class BoxEditWidget(QWidget):

    def __init__(self):
        super().__init__()
        self._filePath = None

        self._widTitle = QLabel("BoxEditWidget", self)
        self._textEdit = QTextEdit(self)
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._widTitle)
        self._layout.addWidget(self._textEdit)

    def setFilePath(self, filePath: str):
        self._filePath = filePath
        file = QFile(filePath)
        if file.open(QFile.OpenModeFlag.ReadOnly):
            self._textEdit.setPlainText(str(file.readAll()))

    def getFilePath(self):
        return self._filePath

