from PySide6 import QtCore
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QTreeWidget, QVBoxLayout
from WidgetModule.LogWidget import LogInst as log
from WidgetModule.AttrWidget import AttrDefine as AttrDef
from WidgetModule.AttrWidget.AttrDelegate import AttrDelegate
from WidgetModule.AttrWidget.AttrTreeItem import AttrBaseHeader, AttrCaseHeader, AttrActionHeader
from WidgetModule.AttrWidget.AttrTreeItem import AttrEmptyConfig, AttrCheckConfig, AttrOperateConfig, AttrControlConfig
from WidgetModule import ExecuteManager


class AttrWidget(QWidget):

    # 属性已修改
    attrModified = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self._entry = None
        self._caseIden = None
        self._actionIden = None
        self._itemList = list()

        self._view = QTreeWidget()
        self._view.setColumnCount(2)
        self._view.setHeaderLabels(["名称", "值"])
        self._view.setColumnWidth(0, 140)
        self._view.setItemDelegate(AttrDelegate())
        self._view.itemChanged.connect(self.onTreeItemChanged)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._view)

    def resetContent(self, entry, caseIden, actionIden=None):
        self._view.clear()
        self._entry = entry
        self._caseIden = caseIden
        self._actionIden = actionIden
        self._itemList.clear()
        if entry and caseIden and actionIden:
            if actionInfo := ExecuteManager.getActionInfo(entry, caseIden, actionIden):
                config = AttrEmptyConfig()
                if actionInfo["baseType"] == "check":
                    config = AttrCheckConfig()
                elif actionInfo["baseType"] == "operate":
                    config = AttrOperateConfig()
                elif actionInfo["baseType"] == "control":
                    config = AttrControlConfig()

                for item in [AttrBaseHeader(), AttrActionHeader(), config]:
                    item.setInfo(actionInfo)
                    self._itemList.append(item)
                    self._view.addTopLevelItem(item)
                    item.updateItem()
                self._view.expandAll()
        elif entry and caseIden:
            if caseInfo := ExecuteManager.getCaseInfo(entry, caseIden):
                for item in [AttrBaseHeader(), AttrCaseHeader()]:
                    item.setInfo(caseInfo)
                    self._itemList.append(item)
                    self._view.addTopLevelItem(item)
                    item.updateItem()
                self._view.expandAll()
        elif entry:
            if fileInfo := ExecuteManager.getFileInfo(entry):
                for item in [AttrBaseHeader()]:
                    item.setInfo(fileInfo)
                    self._itemList.append(item)
                    self._view.addTopLevelItem(item)
                    item.updateItem()
                self._view.expandAll()

    def clearContent(self):
        self._view.clear()

    @QtCore.Slot()
    def onTreeItemChanged(self, treeItem, column):
        # 当前是: 文件/用例/动作
        # 修改是: base/case/action/empty/check/operate/control

        if self._entry and self._caseIden and self._actionIden:
            if actionInfo := ExecuteManager.getActionInfo(self._entry, self._caseIden, self._actionIden):
                for item in self._itemList:
                    item.getInfo(actionInfo)
                if ExecuteManager.setActionInfo(self._entry, self._caseIden, self._actionIden, actionInfo):
                    self.attrModified.emit()
                else:
                    log.error("修改失败")

        elif self._entry and self._caseIden:
            if caseInfo := ExecuteManager.getCaseInfo(self._entry, self._caseIden):
                for item in self._itemList:
                    item.getInfo(caseInfo)
                if ExecuteManager.setCaseInfo(self._entry, self._caseIden, caseInfo):
                    self.attrModified.emit()
                else:
                    log.error("修改失败")

        elif self._entry:
            if fileInfo := ExecuteManager.getFileInfo(self._entry):
                for item in self._itemList:
                    item.getInfo(fileInfo)
                if ExecuteManager.setFileInfo(self._entry, fileInfo):
                    self.attrModified.emit()
                else:
                    log.error("修改失败")

    def sizeHint(self):
        return QSize(300, -1)


