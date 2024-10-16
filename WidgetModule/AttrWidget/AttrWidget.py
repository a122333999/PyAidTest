from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QTreeWidget, QVBoxLayout, QTreeWidgetItem


class AttrWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._view = QTreeWidget()
        self._view.setColumnCount(2)
        self._view.setHeaderLabels(["名称", "值"])

        self._view.addTopLevelItem(_createBaseHeader())
        self._view.addTopLevelItem(_createCaseHeader())
        self._view.addTopLevelItem(_createActionHeader())
        self._view.addTopLevelItem(_createCheckHeader())
        self._view.expandToDepth(0)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._view)

    def clearContent(self):
        pass

    def sizeHint(self):
        return QSize(210, -1)


def _createBaseHeader():
    master = QTreeWidgetItem()
    master.setText(0, "基础")
    master.setFirstColumnSpanned(True)
    node = QTreeWidgetItem(master)
    node.setText(0, "类型")
    node.setText(1, "测试用例")
    node = QTreeWidgetItem(master)
    node.setText(0, "标识")
    node.setText(1, "UUID")
    node = QTreeWidgetItem(master)
    node.setText(0, "名称")
    node.setText(1, "测试用例名称")
    node = QTreeWidgetItem(master)
    node.setText(0, "描述")
    node.setText(1, "测试用例描述")
    return master


def _createCaseHeader():
    master = QTreeWidgetItem()
    master.setText(0, "测试用例")
    master.setFirstColumnSpanned(True)
    node = QTreeWidgetItem(master)
    node.setText(0, "启用")
    node.setText(1, "是否启用")
    node = QTreeWidgetItem(master)
    node.setText(0, "起始")
    node.setText(1, "起始Action标识")
    return master


def _createActionHeader():
    master = QTreeWidgetItem()
    master.setText(0, "测试动作")
    master.setFirstColumnSpanned(True)
    node = QTreeWidgetItem(master)
    node.setText(0, "分类")
    node.setText(1, "image(图片检查)")
    node = QTreeWidgetItem(master)
    node.setText(0, "延迟")
    node.setText(1, "1000")
    node = QTreeWidgetItem(master)
    node.setText(0, "次数")
    node.setText(1, "1")
    node = QTreeWidgetItem(master)
    node.setText(0, "重试")
    node.setText(1, "0")
    node = QTreeWidgetItem(master)
    node.setText(0, "后继")
    node.setText(1, "UUID")
    return master


def _createCheckHeader():
    level1 = QTreeWidgetItem()
    level1.setText(0, "检查配置")
    level1.setFirstColumnSpanned(True)

    level2 = QTreeWidgetItem(level1)
    level2.setText(0, "检查范围")
    level2.setFirstColumnSpanned(True)
    if True:
        level3 = QTreeWidgetItem(level2)
        level3.setText(0, "左边界")
        level3.setText(1, "last::topCenter")

        level3 = QTreeWidgetItem(level2)
        level3.setText(0, "顶边界")
        level3.setText(1, "uuid:UUID.topLeft")

        level3 = QTreeWidgetItem(level2)
        level3.setText(0, "右边界")
        level3.setText(1, "user:(10,10)")

        level3 = QTreeWidgetItem(level2)
        level3.setText(0, "底边界")
        level3.setText(1, "None")

    level2 = QTreeWidgetItem(level1)
    level2.setText(0, "检查来源")
    level2.setText(1, "10")

    level2 = QTreeWidgetItem(level1)
    level2.setText(0, "检查目标")
    level2.setFirstColumnSpanned(True)
    if True:
        level3 = QTreeWidgetItem(level2)
        level3.setFirstColumnSpanned(True)
        level3.setText(0, "图片")

        level3 = QTreeWidgetItem(level2)
        level3.setFirstColumnSpanned(True)
        level3.setText(0, "添加")

    if "采样分类":
        level2 = QTreeWidgetItem(level1)
        level2.setText(0, "采样配置")
        level2.setFirstColumnSpanned(True)

        level3 = QTreeWidgetItem(level2)
        level3.setText(0, "采样次数")
        level3.setText(1, "10")

        level3 = QTreeWidgetItem(level2)
        level3.setText(0, "命中次数")
        level3.setText(1, "10")

        level3 = QTreeWidgetItem(level2)
        level3.setText(0, "采样时长")
        level3.setText(1, "5000")
    return level1
