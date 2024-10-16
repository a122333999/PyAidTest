import os
from PySide6.QtGui import Qt, QAction
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu, QFileDialog
from WidgetModule import Project as ProjectModule
from WidgetModule import ExecuteManager
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
        self._menuBar = QMenuBar()
        self._menuBar.addMenu(self._fileMenu)

        self._fileWidget = FileWidget()
        self._fileWidget.fileActivated.connect(self.onFileActivated)
        self._boxWidget = BoxWidget()
        self._attrWidget = AttrWidget()
        self._logWidget = LogWidget()

        dw = DockWidget()
        dw.setWidget(self._fileWidget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dw)
        dw = DockWidget()
        dw.setWidget(self._attrWidget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dw)
        dw = DockWidget()
        dw.setWidget(self._logWidget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dw)
        self.setCentralWidget(self._boxWidget)
        self.setMenuBar(self._menuBar)

        self.setWindowTitle("PyGuiTest")
        self.resize(1000, 600)

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

    def onFileLoadAction(self):
        if not ProjectModule.isEmpty():
            print("已经打开了一个项目")
            return
        file, _ = QFileDialog.getOpenFileName()
        if len(file):
            self._loadProject(file)

    def onFileSaveAction(self):
        print("保存项目", self)

    def onFileActivated(self, path):
        # 判断是否为entry
        if entry := ProjectModule.pathToEntry(path):
            self._boxWidget.addTabPage(entry)
        else:
            self._boxWidget.addTabPageForFile(path)

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
        self._boxWidget.clearContent()
        self._fileWidget.updateContent(ProjectModule.getProjectPath())
        return True




