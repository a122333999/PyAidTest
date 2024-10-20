# -*- coding:utf-8 -*-

from PySide6.QtCore import QAbstractItemModel, Qt, QModelIndex
from WidgetModule import ExecuteManager


"""
ModelNode {
    icon: None
    info: TestInfo
    type: "case|action|hint|sep"
    title: None
    parent: ModelNode
    children: [ModelNode, ModelNode, ...]
    addition: {caseIden, actionIden}
}
"""


class BoxTestModel(QAbstractItemModel):

    def __init__(self):
        super().__init__()
        self._root = {"icon": None, "info": None, "type": "other", "parent": None, "children": [],
                      "addition": {"caseIden": None, "actionIden": None}}
        self._header = ["名称", "类型", "标识", "描述"]

    def updateModel(self, iden):
        self.beginResetModel()
        _generateCase(iden, self._root)
        self.endResetModel()

    def getCaseAndActionIden(self, index):
        self.__str__()
        if index.isValid():
            if node := index.internalPointer():
                if addition := node.get("addition", None):
                    return addition.get("caseIden", None), addition.get("actionIden", None)
        return None, None

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
        if index.isValid():
            node = index.internalPointer()
            # 显示角色
            if role == Qt.ItemDataRole.DisplayRole:
                displays = self._retDisplays(node)
                return displays[index.column()]
            # 图标角色
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

    @staticmethod
    def _retDisplays(node):
        result = []
        if node["type"] == "sep":
            result.append("")
            result.append("")
            result.append("")
            result.append("")
        elif node["type"] == "hint":
            result.append(node["title"])
            result.append("")
            result.append("")
            result.append("")
        elif info := node.get("info", None):
            keys = {
                "case": "测试用例",
                "check": "检查动作",
                "empty": "空动作",
                "operate": "操作动作",
                "control": "控制动作"
            }
            result.append(info["baseName"])
            result.append(keys.get(info["baseType"], ""))
            result.append(info["baseIden"])
            result.append(info["baseDesc"])

        return result


def _generateCase(entry, parent):
    parent["children"].clear()
    for caseInfo in ExecuteManager.getCaseList(entry):
        # 创建用例节点
        caseNode = _createCaseNode(caseInfo, parent)

        # 收集动作信息
        actionSet = dict()
        for action in ExecuteManager.getActionList(entry, caseInfo["baseIden"]):
            actionSet[action["baseIden"]] = action

        # 生成动作链条
        iden = caseInfo["caseStart"]
        if iden in actionSet:
            _generateAction(iden, actionSet, caseNode)

        # 处理未使用的节点
        if len(actionSet):
            # _createSepNone(caseNode)
            unNode = _createHintNone("未使用节点", caseNode)
            for action in actionSet.values():
                _createActionNode(action, unNode)
            # _createSepNone(caseNode)


def _generateAction(iden, actionSet, parent):
    subset = list()
    actInfo = actionSet.get(iden, None)
    while actInfo:
        # 创建节点
        actNode = _createActionNode(actInfo, parent)

        # 记录分叉节点
        if goto_ := actInfo.get("controlForkGoto", None):
            subset.append((goto_, actNode))

        # 获取子节点标识
        del actionSet[iden]
        iden = actInfo.get("actionChild", None)
        if iden is None:
            _createHintNone(f" - 执行结束", parent)
            break

        # 获取子节点信息
        actInfo = actionSet.get(iden, None)
        if actInfo is None:
            _createHintNone(f" → 跳转到{iden}", parent)
            break

    # 递归处理下一层级
    for iden, node in subset:
        if iden in actionSet:
            _generateAction(iden, actionSet, node)
        elif iden is not None:
            _createHintNone(f" → 跳转到{iden}", node)
        else:
            _createHintNone(f" - 执行结束", node)


def _createCaseNode(info, parent):
    result = {
        "icon": None,
        "info": info,
        "type": "case",
        "title": None,
        "parent": parent,
        "children": [],
        "addition": {
            "caseIden": info.get("baseIden"),
            "actionIden": None,
        }
    }
    parent["children"].append(result)
    return result


def _createActionNode(info, parent):
    result = {
        "icon": None,
        "info": info,
        "type": "action",
        "title": None,
        "parent": parent,
        "children": [],
        "addition": {
            "caseIden": parent["addition"]["caseIden"],
            "actionIden": info.get("baseIden"),
        }
    }
    parent["children"].append(result)
    return result


def _createSepNone(parent):
    result = {
        "icon": None,
        "info": None,
        "type": "sep",
        "title": "",
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
        "info": None,
        "type": "hint",
        "title": title,
        "parent": parent,
        "children": [],
        "addition": {
            "caseIden": parent["addition"]["caseIden"],
            "actionIden": None,
        }
    }
    parent["children"].append(result)
    return result
