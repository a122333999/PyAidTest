from PySide6.QtCore import QAbstractItemModel, Qt, QModelIndex
from WidgetModule import ExecuteManager


"""
ModelNode {
    icon: None
    type: "case|action|other"
    data:["第一列"]
    parent: ModelNode
    children: [ModelNode, ModelNode, ...]
}
"""


class BoxTestModel(QAbstractItemModel):

    def __init__(self):
        super().__init__()
        self._root = {"icon": None, "type": "", "data": ["AAA"], "parent": None, "children": []}

    def updateModel(self, iden):
        self.beginResetModel()
        _generate(iden, self._root)
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
        if parent.isValid():
            node = parent.internalPointer()
            return len(node["data"])
        return len(self._root["data"])

    def data(self, index, role=...):
        if index.isValid():
            node = index.internalPointer()
            if role == Qt.ItemDataRole.DisplayRole:
                return node["data"][index.column()]
            elif role == Qt.ItemDataRole.DecorationRole:
                return node["icon"]
        return None

    def setData(self, index, value, role=...):
        super().setData(index, value, role)

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._root["data"][section]
        return super().headerData(section, orientation, role)

    def flags(self, index):
        return super().flags(index)


def _generate(entry, parent):
    for case in ExecuteManager.getCaseList(entry):
        title = f"启用: {case['active']} {case['name']}  -  {case['desc']}"
        node = _createNode(None, "case", [title], parent)

        actionSet = dict()
        for action in ExecuteManager.getActionList(entry, case["iden"]):
            actionSet[action["iden"]] = action

        iden = case["start"]
        if iden in actionSet:
            _generateLink(iden, actionSet, node)

        # 未使用的节点
        if len(actionSet):
            title = f"未使用节点"
            unused = _createNode(None, "other", [title], node)
            for action in actionSet.values():
                title = f"{action['name']}  -  {action['desc']}"
                act = _createNode(None, "action", [title], unused)


def _generateLink(iden, actionSet, parent):
    subset = list()
    action = actionSet.get(iden, None)
    while action:
        title = f"{action['name']}  -  {action['desc']}"
        node = _createNode(None, "action", [title], parent)

        # fork节点
        if conf_ := action.get("config", None):
            if fork_ := conf_.get("fork", None):
                if goto_ := fork_.get("goto", None):
                    if goto_ in actionSet:
                        subset.append((goto_, node))
                    else:
                        title = f" → 跳转到{goto_}"
                        _createNode(None, "other", [title], node)

        del actionSet[iden]
        iden = action.get("child", None)
        if iden is None:
            break
        action = actionSet.get(iden, None)
        if action is None:
            title = f" → 跳转到{iden}"
            _createNode(None, "other", [title], parent)
            break

    for iden, node in subset:
        _generateLink(iden, actionSet, node)


def _createNode(icon, type_, data, parent):
    # 根据节点类型创建
    result = {
        "icon": icon,
        "type": type_,
        "data": data,
        "parent": parent,
        "children": []
    }
    parent["children"].append(result)
    return result

#

