from PySide6 import QtCore
from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QWidget, QLabel, QTreeView, QVBoxLayout
from WidgetModule import ExecuteManager
from WidgetModule.LogWidget import LogInst as log
from WidgetModule.BoxWidget.BoxTestModel import BoxTestModel


class BoxTestWidget(QWidget):
    # args: entry, caseIden, actionIden
    nodeClicked = QtCore.Signal(str, str, str)

    def __init__(self, entry: str):
        super().__init__()
        self._entry = entry

        self._header = QLabel("Test Header")

        self._view = QTreeView()
        self._model = BoxTestModel()
        self._view.setModel(self._model)
        self._view.setColumnWidth(0, 210)
        self._view.clicked.connect(self.onViewClicked)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 5, 0, 0)
        self._layout.addWidget(self._header)
        self._layout.addWidget(self._view)

        if ExecuteManager.hasHandle(self._entry):
            self._model.updateModel(self._entry)
            self._view.expandAll()
            self._updateHeader()
        else:
            log.error("文件打开失败")

    def refreshWidget(self):
        self._model.updateModel(self._entry)
        self._view.expandAll()
        self._updateHeader()

    def _updateHeader(self):
        if info := ExecuteManager.getFileInfo(self._entry):
            baseName = info.get("baseName", "未找到名称")
            baseDesc = info.get("baseDesc", "未找到描述")
            self._header.setText(f"名称: {baseName}    描述: {baseDesc}")

    @QtCore.Slot(QModelIndex)
    def onViewClicked(self, index):
        caseIden, actionIden = self._model.getCaseAndActionIden(index)
        self.nodeClicked.emit(self._entry, caseIden, actionIden)
