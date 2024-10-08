from PySide6 import QtCore
from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget, QTreeView, QTabWidget
from WidgetModule import Project as ProjectModule
from WidgetModule.BoxWidget.BoxHomeWidget import BoxHomeWidget
from WidgetModule.BoxWidget.BoxTestWidget import BoxTestWidget
from WidgetModule.BoxWidget.BoxEditWidget import BoxEditWidget
from WidgetModule.BoxWidget.BoxImageWidget import BoxImageWidget


class BoxWidget(QWidget):
    # 当前页改变
    currentPageChanged = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

        self._entryPage = set()
        self._filePage = set()

        self._tabWidget = QTabWidget()
        self._tabWidget.setTabsClosable(True)
        self._tabWidget.addTab(BoxHomeWidget(), "主页")
        self._tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._tabWidget)

    def hasTabPage(self, entry):
        pass

    def addTabPage(self, entry):
        if entry[0] in self._entryPage:
            self._changeCurrentPage(entry[0])
            return False

        name = QFileInfo(entry[0]).fileName()
        if entry[1] == "test":
            widget = BoxTestWidget()
            widget.setProperty("iden", entry[0])
            self._entryPage.add(entry[0])
            self._tabWidget.addTab(widget, name)
            self._tabWidget.setCurrentWidget(widget)
            return True
        elif entry[1] == "script":
            widget = BoxEditWidget()
            widget.setProperty("iden", entry[0])
            self._entryPage.add(entry[0])
            self._tabWidget.addTab(widget, name)
            self._tabWidget.setCurrentWidget(widget)
            return True
        elif entry[1] == "resource":
            widget = BoxImageWidget()
            widget.setProperty("iden", entry[0])
            self._entryPage.add(entry[0])
            self._tabWidget.addTab(widget, name)
            self._tabWidget.setCurrentWidget(widget)
            return True

        return False

    def addTabPageForFile(self, file):
        if file in self._filePage:
            self._changeCurrentPage(file)
            return False

        name = QFileInfo(file).fileName()
        widget = BoxImageWidget()
        widget.setProperty("iden", file)
        self._filePage.add(file)
        self._tabWidget.addTab(widget, name)
        self._tabWidget.setCurrentWidget(widget)
        return True

    def clearContent(self):
        pass

    def onTabCloseRequested(self, index):
        widget = self._tabWidget.widget(index)
        self._filePage.discard(widget.property("iden"))
        self._entryPage.discard(widget.property("iden"))
        self._tabWidget.removeTab(index)

    def _changeCurrentPage(self, iden):
        for index in range(self._tabWidget.count()):
            widget = self._tabWidget.widget(index)
            if widget.property("iden") == iden:
                self._tabWidget.setCurrentIndex(index)
                break
