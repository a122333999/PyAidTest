# -*- coding:utf-8 -*-

from PySide6 import QtCore
from PySide6.QtCore import Qt, QSize, QFileInfo, QDir, QModelIndex, QPoint, QEvent, QFile
from PySide6.QtGui import QAction, QCursor, QDesktopServices
from PySide6.QtWidgets import QWidget, QTreeView, QVBoxLayout, QMenu, QInputDialog, QMessageBox
from WidgetModule.FileWidget.FileModel import FileModel
from WidgetModule.LogWidget import LogInst as log
from WidgetModule import InstanceHub as InstanceHub
from WidgetModule import ExecuteManager


class FileWidget(QWidget):

    # args: 文件的绝对路径
    fileActivated = QtCore.Signal(str)

    # 文件被删除 args: 文件的绝对路径
    fileDeleted = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self._info = None

        self._treeModel = FileModel()
        self._treeView = QTreeView()
        self._treeView.installEventFilter(self)
        self._treeView.setModel(self._treeModel)
        self._treeView.setHeaderHidden(True)
        self._treeView.doubleClicked.connect(self.onViewDoubleClicked)

        self._fileMenu = QMenu(self)
        self._createTestFileAct = QAction("创建测试文件")
        self._addExternalFileAct = QAction("添加外部文件")
        self._createDirectoryAct = QAction("创建目录")
        self._deleteDirectoryAct = QAction("删除目录")
        self._deleteFileAct = QAction("删除文件")
        self._excludeFileAct = QAction("排除文件")
        self._showInExplorerAct = QAction("在资源管理器显示")
        self._fileMenu.addAction(self._createTestFileAct)
        self._fileMenu.addAction(self._addExternalFileAct)
        self._fileMenu.addAction(self._createDirectoryAct)
        self._fileMenu.addAction(self._deleteDirectoryAct)
        self._fileMenu.addAction(self._deleteFileAct)
        self._fileMenu.addAction(self._excludeFileAct)
        self._fileMenu.addSeparator()
        self._fileMenu.addAction(self._showInExplorerAct)

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._treeView)

    def updateContent(self, path: str):
        info = QFileInfo(path)
        if info.exists() and info.isFile():
            self._treeModel.updateModel(info.absoluteDir())
            self._treeView.expandAll()
            self._info = info
            return True
        return False

    def clearContent(self):
        self._info = None
        self._treeModel.updateModel(QDir())

    def sizeHint(self):
        return QSize(260, -1)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.ContextMenu and obj is self._treeView:
            curr = self._treeView.currentIndex()
            node = self._treeModel.getIndexItem(curr)
            if node["type"] == "dir":
                self._createTestFileAct.setVisible(True)
                self._addExternalFileAct.setVisible(True)
                self._createDirectoryAct.setVisible(True)
                self._deleteDirectoryAct.setVisible(True)
                self._deleteFileAct.setVisible(False)
                self._excludeFileAct.setVisible(False)
                self._showInExplorerAct.setVisible(True)
            elif node["type"] == "file":
                self._createTestFileAct.setVisible(False)
                self._addExternalFileAct.setVisible(False)
                self._createDirectoryAct.setVisible(False)
                self._deleteDirectoryAct.setVisible(False)
                self._deleteFileAct.setVisible(True)
                self._excludeFileAct.setVisible(True)
                self._showInExplorerAct.setVisible(True)
            else:
                return True

            act = self._fileMenu.exec(QCursor.pos())
            if act is self._createTestFileAct:
                _createTestFile(self, node["absolute"])
            elif act is self._addExternalFileAct:
                _addExternalFile(self, node["absolute"])
            elif act is self._createDirectoryAct:
                _createDirectory(self, node["absolute"])
            elif act is self._deleteDirectoryAct:
                _deleteDirectory(self, node["absolute"])
            elif act is self._deleteFileAct:
                _deleteFile(self, node["absolute"])
                self.fileDeleted.emit(node["absolute"])
            elif act is self._excludeFileAct:
                _excludeFile(self, node["absolute"])
            elif act is self._showInExplorerAct:
                _showInExplorerAct(node["absolute"])
                return True

            self._treeModel.updateModel(self._info.absoluteDir())
            self._treeView.expandAll()
            return True

        return super().eventFilter(obj, event)

    @QtCore.Slot(QModelIndex)
    def onViewDoubleClicked(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node["type"] == "file":
                self.fileActivated.emit(node["absolute"])


def _showInExplorerAct(path):
    info = QFileInfo(path)
    if info.isFile():
        QDesktopServices.openUrl(info.absolutePath())
    else:
        QDesktopServices.openUrl(info.absoluteFilePath())


def _createDirectory(parent, path):
    """ 在 path 目录下创建目录 """
    if QFileInfo(path).isDir():
        text, ret = QInputDialog.getText(parent, "创建目录", "目录名称")
        if ret and len(text):
            QDir(path).mkdir(text)


def _deleteDirectory(parent, path):
    """ 删除 path 目录 """
    if QFileInfo(path).isDir():
        ret = QMessageBox.question(parent, "删除目录", "确认删除")
        if ret == QMessageBox.StandardButton.Yes:
            # 目录下全部文件
            dirs = [QDir(path)]
            files = []
            while len(dirs):
                files.extend(dirs[0].entryList(QDir.Filter.Files))
                dirs.extend(dirs[0].entryInfoList(QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot))
                dirs.pop(0)

            pass


def _createTestFile(parent, path):
    """ 在 path 目录下创建测试文件 """
    if not QFileInfo(path).isDir():
        return
    text, ret = QInputDialog.getText(parent, "创建测试文件", "文件名称", text="TestFile.test")
    if not ret or len(text) == 0:
        return
    ret = InstanceHub.project.createTestFile(path, text)
    if ret is None:
        log.error("创建失败")
        return
    if not InstanceHub.project.addTestFile(ret):
        log.error("添加失败")
        return
    entry = InstanceHub.project.pathToEntry(ret)
    if entry is None:
        log.error("添加失败")
        return
    if not ExecuteManager.load(entry):
        log.error("新测试文件加载失败")
        return

    InstanceHub.project.setModified(True)
    log.info("创建成功")


def _addExternalFile(parent, path):
    """ 在 path 目录下创建测试文件 """
    pass


def _deleteFile(parent, path):
    info = QFileInfo(path)
    if not info.exists() or not info.isFile():
        return
    ret = QMessageBox.question(parent, "删除文件", "确认删除文件?")
    if ret != QMessageBox.StandardButton.Yes:
        return
    if entry := InstanceHub.project.pathToEntry(path):
        InstanceHub.project.rmvEntry(entry)
    QFile(path).remove()
    InstanceHub.project.setModified(True)
    log.info("删除成功")


def _excludeFile(parent, path):
    info = QFileInfo(path)
    if not info.exists() or not info.isFile():
        return
    ret = QMessageBox.question(parent, "排除文件", "确认排除文件?")
    if ret != QMessageBox.StandardButton.Yes:
        return
    if entry := InstanceHub.project.pathToEntry(path):
        InstanceHub.project.rmvEntry(entry)
    InstanceHub.project.setModified(True)
    log.info("排除成功")
