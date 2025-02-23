# -*- coding:utf-8 -*-

from PySide6.QtCore import QAbstractItemModel, Qt, QModelIndex
from WidgetModule import InstanceHub


"""
ModelNode {
    icon: None
    type: "root|case|action"
    info: dict(测试信息)
    parent: ModelNode
    children: [ModelNode, ModelNode, ...]
    addition: {caseIden, actionIden}
}
"""


class BoxTestModel(QAbstractItemModel):

    def __init__(self):
        super().__init__()
        self._root = {"icon": None, "info": None, "type": "root", "parent": None, "children": [],
                      "addition": {"caseIden": None, "actionIden": None}}
        self._header = ["名称", "类型", "标识", "描述"]

    def updateModel(self, iden):
        self.beginResetModel()
        self._root["children"].clear()
        _generateCase(iden, self._root)
        self.endResetModel()

    def index(self, row, column, parent=None):
        if not super().hasIndex(row, column, parent):
            return QModelIndex()

        node = self._root
        if parent.isValid():
            node = parent.internalPointer()
        return super().createIndex(row, column, node["children"][row])

    def parent(self, *args):
        index = args[0]
        if index.isValid():
            node = index.internalPointer()
            temp = node["parent"]
            if temp != self._root:
                return super().createIndex(len(temp["children"]), 0, temp)
        return QModelIndex()

    def rowCount(self, parent=None):
        if parent.isValid():
            node = parent.internalPointer()
            return len(node["children"])
        return len(self._root["children"])

    def columnCount(self, parent=None):
        return len(self._header)

    def data(self, index, role=...):
        if not index.isValid():
            return None
        
        node = index.internalPointer()
        if role == Qt.ItemDataRole.DisplayRole:
            if node["type"] == "case" or node["type"] == "action":
                if index.column() == 0:
                    return node["info"]["baseName"]
                elif index.column() == 1:
                    return _retNodeTypeStr(node["type"])
                elif index.column() == 2:
                    return node["info"]["baseIden"]
                elif index.column() == 3:
                    return node["info"]["baseDesc"]
        elif role == Qt.ItemDataRole.DecorationRole:
            return node["icon"]
        
        return None

    def setData(self, index, value, role=...):
        super().setData(index, value, role)

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._header[section]
            elif orientation == Qt.Orientation.Vertical:
                return section
        return super().headerData(section, orientation, role)

    def flags(self, index):
        return super().flags(index)


def _retNodeTypeStr(t):
    if t == "case":
        return "测试用例"
    elif t == "search":
        return "搜索动作"
    elif t == "operate":
        return "操作动作"
    elif t == "control":
        return "控制动作"
    elif t == "empty":
        return "空动作"
    return "未知类型"


def _generateCase(entry, parent):
    for caseInfo in InstanceHub.execute.getCaseList(entry):
        # 创建用例节点
        caseNode = {
            "icon": None,
            "type": "case",
            "info": caseInfo,
            "parent": parent,
            "children": [],
            "addition": {
                "caseIden": caseInfo.get("baseIden"),
                "actionIden": None,
            }
        }
        parent["children"].append(caseNode)

        # 创建动作节点
        for actionInfo in InstanceHub.execute.getActionList(entry, caseInfo["baseIden"]):
            actionNode = {
                "icon": None,
                "type": "action",
                "info": actionInfo,
                "parent": caseNode,
                "children": [],
                "addition": {
                    "caseIden": caseNode["addition"]["caseIden"],
                    "actionIden": actionInfo.get("baseIden"),
                }
            }
            caseNode["children"].append(actionNode)


def _createSepNone(parent):
    result = {
        "icon": None,
        "type": "sep",
        "info": "",
        "parent": parent,
        "children": [],
        "addition": {
            "caseIden": parent["addition"]["caseIden"],
            "actionIden": None,
        }
    }
    parent["children"].append(result)
    return result


def _createHintNone(title, parent):
    result = {
        "icon": None,
        "type": "hint",
        "info": title,
        "parent": parent,
        "children": [],
        "addition": {
            "caseIden": parent["addition"]["caseIden"],
            "actionIden": None,
        }
    }
    parent["children"].append(result)
    return result
