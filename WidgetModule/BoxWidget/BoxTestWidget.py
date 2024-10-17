from PySide6.QtWidgets import QWidget, QLabel, QTreeView, QVBoxLayout
from WidgetModule import ExecuteManager
from WidgetModule.BoxWidget.BoxTestModel import BoxTestModel


class BoxTestWidget(QWidget):
    def __init__(self, iden: str):
        super().__init__()
        self._iden = iden
        self._view = QTreeView()
        self._model = BoxTestModel()
        self._view.setModel(self._model)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(QLabel("BoxTestWidget"))
        self._layout.addWidget(self._view)

        if ExecuteManager.hasHandle(self._iden):
            self._model.updateModel(self._iden)
            self._view.expandAll()
            # print(ExecuteManager.getFileInfo(self._iden))
            # print(ExecuteManager.getFileList())
            # print(ExecuteManager.getCaseInfo(self._iden, 0))
            # print(ExecuteManager.getCaseList(self._iden))
            # print(ExecuteManager.getActionInfo(self._iden, 0, ""))
            # print(ExecuteManager.getActionList(self._iden, 0))

            # print(ExecuteManager.start(self._iden, 0))


