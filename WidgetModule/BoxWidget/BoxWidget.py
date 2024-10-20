# -*- coding:utf-8 -*-

from PySide6 import QtCore
from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget, QTabWidget
from WidgetModule import ProjectManager
from WidgetModule import ExecuteManager
from WidgetModule.BoxWidget.BoxHomeWidget import BoxHomeWidget
from WidgetModule.BoxWidget.BoxTestWidget import BoxTestWidget
from WidgetModule.BoxWidget.BoxEditWidget import BoxEditWidget
from WidgetModule.BoxWidget.BoxImageWidget import BoxImageWidget


class BoxWidget(QWidget):
    # 当前页改变
    # args: filePath
    currentPageChanged = QtCore.Signal(str)

    # 测试文件的节点被点击
    # args: entry
    hintNodeClicked = QtCore.Signal(str)
    # args: entry, caseIden, actionIden
    testNodeClicked = QtCore.Signal(str, str, str)

    def __init__(self):
        super().__init__()

        self._filePage = set()

        self._tabWidget = QTabWidget()
        self._tabWidget.setTabsClosable(True)
        self._tabWidget.addTab(BoxHomeWidget(), "主页")
        self._tabWidget.currentChanged.connect(self.onCurrentTabChanged)
        self._tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._tabWidget)

    def addTabPage(self, absFilePath):
        filePath = absFilePath
        fileName = QFileInfo(absFilePath).fileName()

        # 是否已存在该文件的Tab
        if filePath in self._filePage:
            self._changeCurrentPage(filePath)
            return False

        if entry := ProjectManager.pathToEntry(filePath):
            entryFile, entryType = entry
            if entryType == "test":
                widget = BoxTestWidget(entryFile)
                widget.setProperty("filePath", filePath)
                widget.nodeClicked.connect(self.onNoneClicked)
                self._filePage.add(filePath)
                self._tabWidget.addTab(widget, fileName)
                self._tabWidget.setCurrentWidget(widget)
                return True
            elif entryType == "script":
                widget = BoxEditWidget(entryFile)
                widget.setProperty("filePath", filePath)
                self._filePage.add(filePath)
                self._tabWidget.addTab(widget, fileName)
                self._tabWidget.setCurrentWidget(widget)
                return True
            elif entryType == "resource":
                widget = BoxImageWidget(entryFile)
                widget.setProperty("filePath", filePath)
                self._filePage.add(filePath)
                self._tabWidget.addTab(widget, fileName)
                self._tabWidget.setCurrentWidget(widget)
                return True
        else:
            widget = BoxImageWidget(filePath)
            widget.setProperty("filePath", filePath)
            self._filePage.add(filePath)
            self._tabWidget.addTab(widget, fileName)
            self._tabWidget.setCurrentWidget(widget)
            return True

        return False

    def clearTabPage(self):
        pass

    def refreshTabPage(self):
        if widget := self._tabWidget.currentWidget():
            if isinstance(widget, BoxTestWidget):
                widget.refreshWidget()

    @QtCore.Slot(int)
    def onTabCloseRequested(self, index):
        widget = self._tabWidget.widget(index)
        self._filePage.discard(widget.property("filePath"))
        self._tabWidget.removeTab(index)

    @QtCore.Slot()
    def onCurrentTabChanged(self):
        if widget := self._tabWidget.currentWidget():
            filePath = widget.property("filePath")
            self.currentPageChanged.emit(filePath)

    @QtCore.Slot(str, str, str)
    def onNoneClicked(self, entry, caseIden, actionIden):
        if len(entry) and len(caseIden):
            self.testNodeClicked.emit(entry, caseIden, actionIden)
        elif len(entry):
            self.hintNodeClicked.emit(entry)

    def _changeCurrentPage(self, filePath):
        for index in range(self._tabWidget.count()):
            widget = self._tabWidget.widget(index)
            if widget.property("filePath") == filePath:
                self._tabWidget.setCurrentIndex(index)
                break
