import os

from PySide6 import QtCore
from PySide6.QtGui import Qt, QAction
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu, QFileDialog, QToolBar
from WidgetModule import Project as ProjectModule
from WidgetModule import ExecuteManager
from WidgetModule.LogWidget import LogInst as log
from WidgetModule.DockWidget import DockWidget
from WidgetModule.FileWidget.FileWidget import FileWidget
from WidgetModule.BoxWidget.BoxWidget import BoxWidget
from WidgetModule.AttrWidget.AttrWidget import AttrWidget
from WidgetModule.LogWidget.LogWidget import LogWidget


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
        self._menuBar = QMenuBar()
        self._menuBar.setContentsMargins(0, 0, 0, 0)
        self._menuBar.addMenu(self._fileMenu)
        self._menuBar.addMenu(self._runMenu)

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
        self._menuBar.setCornerWidget(self._toolBar)

        self.setWindowTitle("PyGuiTest")
        self.resize(1200, 720)

    @QtCore.Slot()
    def onFileNewAction(self):
        # 1确定目录和项目名称 2新建目录和输出项目文件
        path = QFileDialog.getExistingDirectory(self, "新建项目", "TestProject")
        if len(path) == 0:
            return
        if ret := ProjectModule.createProject(*os.path.split(path)):
            # TODO: 关闭现在的项目
            self._loadProject(ret)
            return

        print("新建项目失败")

    @QtCore.Slot()
    def onFileLoadAction(self):
        if not ProjectModule.isEmpty():
            print("已经打开了一个项目")
            return
        file, _ = QFileDialog.getOpenFileName()
        if len(file):
            self._loadProject(file)

    @QtCore.Slot()
    def onFileSaveAction(self):
        if path := ProjectModule.getProjectPath():
            self._saveProject(path)

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
        if entry := ProjectModule.pathToEntry(filePath):
            entryFile, entryType = entry
            if entryType == "test":
                self._attrWidget.resetContent(entryFile, None, None)

    @QtCore.Slot()
    def onAttrModified(self):
        self._boxWidget.refreshTabPage()
        pass

    def _loadProject(self, path):
        if not ProjectModule.load(path):
            print("项目打开失败")
            return False

        if not ExecuteManager.init(ProjectModule.getProjectDirectory()):
            return False

        for entry0, entry1 in ProjectModule.getTestEntryList():
            if not ExecuteManager.load(entry0):
                # TODO: 打开失败时的清理
                return False

        self._attrWidget.clearContent()
        self._boxWidget.clearTabPage()
        self._fileWidget.updateContent(ProjectModule.getProjectPath())
        return True

    def _saveProject(self, path):
        self.objectName()  # 无意义
        ProjectModule.save(path)
        for entryFile, entryType in ProjectModule.getTestEntryList():
            if not ExecuteManager.save(entryFile):
                log.error("保存失败")






