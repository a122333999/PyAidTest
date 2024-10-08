from PySide6 import QtCore
from PySide6.QtCore import QSize, QFileInfo
from PySide6.QtWidgets import QWidget, QTreeView, QVBoxLayout
from WidgetModule.FileModel import FileModel


class FileWidget(QWidget):

    fileActivated = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self._treeModel = FileModel()
        self._treeView = QTreeView()
        self._treeView.setModel(self._treeModel)

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._treeView)

        self._treeView.doubleClicked.connect(self._onViewDoubleClicked)

    def updateContent(self, path: str):
        info = QFileInfo(path)
        if info.exists() and info.isFile():
            self._treeModel.updateModel(info.absoluteDir())
            return True
        return False

    def sizeHint(self):
        return QSize(200, -1)

    def _onViewDoubleClicked(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node["type"] == "file":
                self.fileActivated.emit(node["absolute"])

