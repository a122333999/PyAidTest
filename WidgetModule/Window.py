# -*- coding:utf-8 -*-

from PySide6 import QtCore
from PySide6.QtGui import Qt, QAction
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu, QFileDialog, QToolBar, QMessageBox
from WidgetModule import ProjectManager
from WidgetModule import ExecuteManager
from WidgetModule.LogWidget import LogInst as log
from WidgetModule.DockWidget import DockWidget
from WidgetModule.FileWidget.FileWidget import FileWidget
from WidgetModule.BoxWidget.BoxWidget import BoxWidget
from WidgetModule.AttrWidget.AttrWidget import AttrWidget
from WidgetModule.LogWidget.LogWidget import LogWidget
from WidgetModule.ZzzWidget.NewProjectDialog import NewProjectDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._fileMenu = QMenu("File")
        self._fileNewAction = QAction("新建", self)
        self._fileNewAction.triggered.connect(self.onFileNewAction)
        self._fileLoadAction = QAction("打开", self)
        self._fileLoadAction.triggered.connect(self.onFileLoadAction)
        self._fileSaveAction = QAction("保存", self)
        self._fileSaveAction.triggered.connect(self.onFileSaveAction)
        self._fileMenu.addAction(self._fileNewAction)
        self._fileMenu.addAction(self._fileLoadAction)
        self._fileMenu.addAction(self._fileSaveAction)
        self._fileMenu.addSeparator()
        self._fileMenu.addAction("关闭", lambda: self.close())
        self._runMenu = QMenu("Run")
        self._runRunAction = QAction("运行文件", self)
        self._runMenu.addAction(self._runRunAction)
        self._helpMenu = QMenu("Help")
        self._helpHomeAction = QAction("主页", self)
        self._helpMenu.addAction(self._helpHomeAction)
        self._menuBar = QMenuBar()
        self._menuBar.setContentsMargins(0, 0, 0, 0)
        self._menuBar.addMenu(self._fileMenu)
        self._menuBar.addMenu(self._runMenu)
        self._menuBar.addMenu(self._helpMenu)

        self._fileWidget = FileWidget()
        self._fileWidget.fileActivated.connect(self.onFileActivated)
        self._boxWidget = BoxWidget()
        self._boxWidget.testNodeClicked.connect(self.onTestNodeClicked)
        self._boxWidget.hintNodeClicked.connect(self.onHintNodeClicked)
        self._boxWidget.currentPageChanged.connect(self.onCurrentPageChanged)
        self._attrWidget = AttrWidget()
        self._attrWidget.attrModified.connect(self.onAttrModified)
        self._logWidget = LogWidget()

        dw = DockWidget()
        dw.setWindowTitle("项目")
        dw.setWidget(self._fileWidget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dw)
        dw = DockWidget()
        dw.setWindowTitle("属性")
        dw.setWidget(self._attrWidget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dw)
        dw = DockWidget()
        dw.setWindowTitle("日志")
        dw.setWidget(self._logWidget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dw)
        self.setCentralWidget(self._boxWidget)
        self.setMenuBar(self._menuBar)

        self._toolBar = QToolBar(self)
        self._toolBar.addAction("AA")
        self._toolBar.setVisible(False)
        # self._menuBar.setCornerWidget(self._toolBar)

        self.setWindowTitle("PyGuiTest")
        self.resize(1200, 720)

    @QtCore.Slot()
    def onFileNewAction(self):
        # 1处理当前项目
        if ProjectManager.isModified():
            ret = QMessageBox.question(self, "提示", "当前工程未保存, 是否保存?")
            if ret == QMessageBox.StandardButton.Yes:
                if not self._saveProject():
                    return

        # 2新项目的位置
        path, name = NewProjectDialog(self).exec()
        if path is None or name is None:
            return

        # 3创建项目/清理项目/加载项目
        if ret := ProjectManager.createProject(path, name):
            self._clearProject()
            self._loadProject(ret)
            return
        log.error("新建项目失败")

    @QtCore.Slot()
    def onFileLoadAction(self):
        # 1处理当前项目 2加载项目
        if ProjectManager.isModified():
            ret = QMessageBox.question(self, "提示", "当前工程未保存, 是否保存?")
            if ret == QMessageBox.StandardButton.Yes:
                if not self._saveProject():
                    return

        file, _ = QFileDialog.getOpenFileName()
        if len(file):
            self._clearProject()
            if not self._loadProject(file):
                log.error("加载项目失败")

    @QtCore.Slot()
    def onFileSaveAction(self):
        self._saveProject()

    @QtCore.Slot(str)
    def onFileActivated(self, absPath):
        self._boxWidget.addTabPage(absPath)

    @QtCore.Slot(str, str, str)
    def onTestNodeClicked(self, entry, caseIden, actionIden):
        entry = entry if len(entry) else None
        caseIden = caseIden if len(caseIden) else None
        actionIden = actionIden if len(actionIden) else None
        self._attrWidget.resetContent(entry, caseIden, actionIden)

    @QtCore.Slot(str)
    def onHintNodeClicked(self, entry):
        self._attrWidget.clearContent()

    @QtCore.Slot(str)
    def onCurrentPageChanged(self, filePath):
        self._attrWidget.clearContent()
        if entry := ProjectManager.pathToEntry(filePath):
            entryFile, entryType = entry
            if entryType == "test":
                self._attrWidget.resetContent(entryFile, None, None)

    @QtCore.Slot()
    def onAttrModified(self):
        self._boxWidget.refreshTabPage()
        pass

    def _loadProject(self, absPath):
        if not ProjectManager.load(absPath):
            log.error("加载项目失败")
            return False
        if not ExecuteManager.init(ProjectManager.getProjectDirectory()):
            log.error("加载项目失败")
            return False
        for entryFile, entryType in ProjectManager.getTestEntryList():
            if not ExecuteManager.load(entryFile):
                ExecuteManager.uninit()
                ProjectManager.clear()
                log.error("加载项目失败")
                return False
        if absPath != ProjectManager.getProjectPath():
            log.error("加载项目失败")
            return False
        self._fileWidget.updateContent(absPath)
        log.info("加载项目成功")
        return True

    def _saveProject(self):
        self.objectName()  # 无意义
        if path := ProjectManager.getProjectPath():
            for entryFile, entryType in ProjectManager.getTestEntryList():
                if not ExecuteManager.save(entryFile):
                    log.error("项目保存失败")
                    return False
            if not ProjectManager.save(path):
                log.info("项目保存成功")
                return True
        log.error("项目保存失败")
        return False

    def _clearProject(self):
        # 1清理控件 2清理测试文件 3清理工程文件
        self._attrWidget.clearContent()
        self._boxWidget.clearTabPage()
        self._fileWidget.clearContent()
        ExecuteManager.uninit()
        ProjectManager.clear()











