from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget, QTreeView, QTabWidget


class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._tabWidget = QTabWidget()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._tabWidget)

        self._treeView = QTreeView()
        self._tabWidget.addTab(self._treeView, "主页")

    def clearContent(self):
        pass
