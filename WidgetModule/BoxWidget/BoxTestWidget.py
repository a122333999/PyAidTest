# -*- coding:utf-8 -*-

from PySide6 import QtCore
from PySide6.QtCore import Qt, QModelIndex, QPoint
from PySide6.QtGui import QCursor, QAction
from PySide6.QtWidgets import QWidget, QLabel, QTreeView, QVBoxLayout, QMenu
from WidgetModule import ExecuteManager
from WidgetModule.LogWidget import LogInst as log
from WidgetModule.BoxWidget.BoxTestModel import BoxTestModel


"""
添加测试用例
删除测试用例
添加动作到头部
添加动作到末尾

插入动作
插入跳转
删除动作


"""


class BoxTestWidget(QWidget):
    # args: entry, caseIden, actionIden
    nodeClicked = QtCore.Signal(str, str, str)

    def __init__(self, entry: str):
        super().__init__()
        self._entry = entry

        self._header = QLabel("Test Header")

        self._view = QTreeView()
        self._model = BoxTestModel()
        self._view.setModel(self._model)
        self._view.setColumnWidth(0, 210)
        self._view.clicked.connect(self.onViewClicked)
        self._view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._view.customContextMenuRequested.connect(self.onMenuRequested)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 5, 0, 0)
        self._layout.addWidget(self._header)
        self._layout.addWidget(self._view)

        # 无操作 复制标识 插入动作到头部 插入动作到末尾 插入动作 添加跳转 创建用例 删除用例 删除动作 分离动作
        self._notAct = QAction("无操作", self)
        self._copyIdenAct = QAction("复制标识", self)
        self._notMenu = QMenu(self)
        self._notMenu.addAction(self._notAct)
        self._caseMenu = QMenu(self)
        self._caseMenu.addAction(self._copyIdenAct)
        self._actionMenu = QMenu(self)
        self._actionMenu.addAction(self._copyIdenAct)

        if not ExecuteManager.hasHandle(self._entry):
            pass  # TODO: 尝试打开

        if ExecuteManager.hasHandle(self._entry):
            self._model.updateModel(self._entry)
            self._view.expandAll()
            self._updateHeader()
        else:
            log.error("文件打开失败")

    def refreshWidget(self):
        self._model.updateModel(self._entry)
        self._view.expandAll()
        self._updateHeader()

    def _updateHeader(self):
        if info := ExecuteManager.getFileInfo(self._entry):
            baseName = info.get("baseName", "未找到名称")
            baseDesc = info.get("baseDesc", "未找到描述")
            self._header.setText(f"名称: {baseName}    描述: {baseDesc}")

    @QtCore.Slot(QModelIndex)
    def onViewClicked(self, index):
        if not index.isValid():
            return
        if node := index.internalPointer():
            type_ = node["type"]
            addition = node["addition"]
            caseIden, actionIden = addition["caseIden"], addition["actionIden"]
            if type_ == "case" or type_ == "action":
                self.nodeClicked.emit(self._entry, caseIden, actionIden)
            else:
                self.nodeClicked.emit(self._entry, None, None)

    @QtCore.Slot(QPoint)
    def onMenuRequested(self, pos):
        index = self._view.currentIndex()
        if not index.isValid():
            print("测试动作菜单")
            return
        if node := index.internalPointer():
            if node["type"] == "case":
                self._caseMenu.exec(QCursor.pos())
            elif node["type"] == "action":
                self._actionMenu.exec(QCursor.pos())
            else:
                self._notMenu.exec(QCursor.pos())


