# -*- coding:utf-8 -*-

from PySide6 import QtCore
from PySide6.QtCore import QSize, QFileInfo, QDir
from PySide6.QtWidgets import QWidget, QTreeView, QVBoxLayout
from WidgetModule.FileWidget.FileModel import FileModel


class FileWidget(QWidget):

    # args: 文件的绝对路径
    fileActivated = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self._treeModel = FileModel()
        self._treeView = QTreeView()
        self._treeView.setModel(self._treeModel)
        self._treeView.doubleClicked.connect(self._onViewDoubleClicked)

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._treeView)

    def updateContent(self, path: str):
        info = QFileInfo(path)
        if info.exists() and info.isFile():
            self._treeModel.updateModel(info.absoluteDir())
            self._treeView.expandAll()
            return True
        return False

    def clearContent(self):
        self._treeModel.updateModel(QDir())

    def sizeHint(self):
        return QSize(260, -1)

    def _onViewDoubleClicked(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node["type"] == "file":
                self.fileActivated.emit(node["absolute"])

