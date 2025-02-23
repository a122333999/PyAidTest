# -*- coding:utf-8 -*-

from PySide6 import QtCore
from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget, QTabWidget
from WidgetModule import InstanceHub as InstanceHub
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

        if entry := InstanceHub.project.pathToEntry(filePath):
            entryFile, entryType = InstanceHub.project.getEntryInfo(entry)
            if entryType == "test":
                widget = BoxTestWidget()
                widget.setFilePath(filePath)
                widget.nodeClicked.connect(self.onNoneClicked)
                self._filePage.add(filePath)
                self._tabWidget.addTab(widget, fileName)
                self._tabWidget.setCurrentWidget(widget)
                return True
            elif entryType == "script":
                widget = BoxEditWidget()
                widget.setFilePath(filePath)
                self._filePage.add(filePath)
                self._tabWidget.addTab(widget, fileName)
                self._tabWidget.setCurrentWidget(widget)
                return True
            elif entryType == "resource":
                widget = BoxImageWidget()
                widget.setFilePath(filePath)
                self._filePage.add(filePath)
                self._tabWidget.addTab(widget, fileName)
                self._tabWidget.setCurrentWidget(widget)
                return True

        widget = BoxEditWidget()
        widget.setFilePath(filePath)
        self._filePage.add(filePath)
        self._tabWidget.addTab(widget, fileName)
        self._tabWidget.setCurrentWidget(widget)
        return True

    def clearTabPage(self):
        self._tabWidget.clear()
        self._filePage.clear()
        self._tabWidget.addTab(BoxHomeWidget(), "主页")

    @QtCore.Slot(int)
    def onTabCloseRequested(self, index):
        widget = self._tabWidget.widget(index)
        self._filePage.discard(widget.getFilePath())
        self._tabWidget.removeTab(index)

    @QtCore.Slot()
    def onCurrentTabChanged(self):
        if widget := self._tabWidget.currentWidget():
            filePath = widget.getFilePath()
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
            if widget.getFilePath() == filePath:
                self._tabWidget.setCurrentIndex(index)
                break
