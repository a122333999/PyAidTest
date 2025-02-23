# -*- coding:utf-8 -*-

from PySide6 import QtCore
from PySide6.QtGui import Qt, QAction
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu, QFileDialog, QToolBar, QMessageBox
from WidgetModule import InstanceHub as InstanceHub
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
        self._fileNewAction.triggered.connect(self.onFileNewActionClicked)
        self._fileLoadAction = QAction("打开", self)
        self._fileLoadAction.triggered.connect(self.onFileLoadActionClicked)
        self._fileSaveAction = QAction("保存", self)
        self._fileSaveAction.triggered.connect(self.onFileSaveActionClicked)
        self._fileMenu.addAction(self._fileNewAction)
        self._fileMenu.addAction(self._fileLoadAction)
        self._fileMenu.addAction(self._fileSaveAction)
        self._fileMenu.addSeparator()
        self._fileMenu.addAction("关闭", lambda: self.close())
        self._runMenu = QMenu("Run")
        self._runRunAction = QAction("运行", self)
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

        self.setWindowTitle("PyAidTest [*]")
        self.resize(1200, 720)

        # TODO: 项目管理器信号
        # ProjectManager.addObserver("MainWindow", self.projectCallback)

    def __del__(self):
        # ProjectManager.rmvObserver("MainWindow")
        pass

    @QtCore.Slot()
    def onFileNewActionClicked(self):
        # 1处理当前项目
        if InstanceHub.project.isModified():
            ret = QMessageBox.question(self, "提示", "当前工程未保存, 是否保存?")
            if ret == QMessageBox.StandardButton.Yes:
                if not self._saveProject():
                    return

        # 2新项目的位置
        path, name = NewProjectDialog(self).exec()
        if path is None or name is None:
            return

        # 3创建项目/清理项目/加载项目
        if ret := InstanceHub.project.createProject(path, name):
            self._clearProject()
            self._loadProject(ret)
            return
        log.error("新建项目失败")

    @QtCore.Slot()
    def onFileLoadActionClicked(self):
        # 1处理当前项目 2加载项目
        if InstanceHub.project.isModified():
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
    def onFileSaveActionClicked(self):
        self._saveProject()

    @QtCore.Slot(str)
    def onFileActivated(self, absPath):
        if entryFile := InstanceHub.project.pathToEntry(absPath):
            if not InstanceHub.execute.hasHandle(entryFile):
                if not InstanceHub.execute.load(entryFile):
                    log.error(f"加载测试文件失败: {entryFile}")
        self._boxWidget.addTabPage(absPath)

    @QtCore.Slot(str, str, str)
    def onTestNodeClicked(self, entry, caseIden, actionIden):
        # entry = entry if len(entry) else None
        # caseIden = caseIden if len(caseIden) else None
        # actionIden = actionIden if len(actionIden) else None
        # self._attrWidget.resetContent(entry, caseIden, actionIden)
        pass

    @QtCore.Slot(str)
    def onHintNodeClicked(self, entry):
        # self._attrWidget.clearContent()
        pass

    @QtCore.Slot(str)
    def onCurrentPageChanged(self, filePath):
        # self._attrWidget.clearContent()
        # if entry := InstanceHub.project.pathToEntry(filePath):
        #     entryFile, entryType = InstanceHub.project.getEntryInfo(entry)
        #     if entryType == "test":
        #         self._attrWidget.resetContent(entryFile, None, None)
        pass

    def projectCallback(self, event, data):
        if event == InstanceHub.project.ProjectModifiedEvent:
            self.setWindowModified(data["modified"])

    def closeEvent(self, event):
        if InstanceHub.project.isModified():
            btn = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            ret = QMessageBox.question(self, "是否保存项目", "项目已修改, 是否保存", btn)
            if ret == QMessageBox.StandardButton.Yes:
                if not self._saveProject():
                    event.ignore()
                    return
            elif ret == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
        super().closeEvent(event)

    def _loadProject(self, absPath):
        if not InstanceHub.project.load(absPath):
            log.error("加载项目失败")
            return False
        if not InstanceHub.execute.init(InstanceHub.project.getProjectDirPath()):
            log.error("加载项目失败")
            return False
        if absPath != InstanceHub.project.getProjectFilePath():
            log.error("加载项目失败")
            return False
        self._fileWidget.updateContent(absPath)
        log.info("加载项目成功")
        return True

    def _saveProject(self):
        self.objectName()  # 无意义
        if path := InstanceHub.project.getProjectFilePath():
            if not InstanceHub.project.save(path):
                log.error("项目保存失败")
                return False
            for entryFile, entryType in InstanceHub.project.getTestEntryList():
                if not InstanceHub.execute.save(entryFile):
                    log.error(f"测试文件保存失败: {entryFile}")
                    return False
        InstanceHub.project.setModified(False)
        log.info("项目保存成功")
        return True

    def _clearProject(self):
        # 1清理控件 2清理测试文件 3清理工程文件
        self._attrWidget.clearContent()
        self._boxWidget.clearTabPage()
        self._fileWidget.clearContent()
        InstanceHub.execute.uninit()
        InstanceHub.project.unload()







"""
        for entryFile, entryType in InstanceHub.project.getTestEntryList():
            if not InstanceHub.execute.load(entryFile):
                InstanceHub.project.rmvEntry(entryFile)
                InstanceHub.project.setModified(True)
                log.error(f"加载测试文件失败: {entryFile}")
"""



