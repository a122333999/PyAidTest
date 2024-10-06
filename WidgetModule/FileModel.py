from PySide6.QtCore import QAbstractItemModel, Qt, QModelIndex, QDir

"""
ModelNode {
    icon: None
    data:["第一列", "第二列", ...]
    parent: ModelNode
    children: [ModelNode, ModelNode, ...]
}
"""


class FileModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self._root = {"icon": None, "data": ["项目名称?"], "parent": None, "children": []}
        # self._root["children"].append({"data": ["数据"], "parent": self._root, "children": []})
        # self._root["children"].append({"data": ["数据"], "parent": self._root, "children": []})

    def updateModel(self, qtDir: QDir):
        self.beginResetModel()
        self._root["children"].clear()
        if qtDir.exists():
            self._root["children"] = _recursiveDirectory(qtDir, self._root)
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
            if role == Qt.ItemDataRole.DisplayRole:
                node = index.internalPointer()
                return node["data"][index.column()]
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


def _recursiveDirectory(qtDir: QDir, parent: dict):
    result = []
    filter_ = QDir.Filter.NoDotAndDotDot | QDir.Filter.Files | QDir.Filter.Dirs
    for info in qtDir.entryInfoList("*", filter_):
        node = {"icon": None, "data": [info.fileName()], "parent": parent, "children": []}
        if info.isDir():
            node["children"] = (_recursiveDirectory(QDir(info.absoluteFilePath()), node))
        result.append(node)
    return result
