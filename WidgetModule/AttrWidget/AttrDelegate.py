from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit, QComboBox, QSpinBox
from WidgetModule.AttrWidget import AttrDefine as AttrDef


class AttrDelegate(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def createEditor(self, parent, option, index):
        itemAbc = index.data(AttrDef.ItemAbcRole)
        if itemAbc == AttrDef.BaseTypeItem:
            return None
        elif itemAbc == AttrDef.BaseIdenItem:
            return None
        elif itemAbc == AttrDef.BaseNameItem:
            return _createDftLineEdit(parent, option, index)
        elif itemAbc == AttrDef.BaseDescItem:
            return _createDftLineEdit(parent, option, index)
        elif itemAbc == AttrDef.CaseStartItem:
            return _createDftLineEdit(parent, option, index)
        elif itemAbc == AttrDef.CaseActiveItem:
            return _createBoolComboBox(parent, option, index)
        elif itemAbc == AttrDef.ActionClassItem:
            return None
        elif itemAbc == AttrDef.ActionDelayItem:
            return _createDftSpinBox(parent, option, index, 0, 1000000000)
        elif itemAbc == AttrDef.ActionTimesItem:
            return _createDftSpinBox(parent, option, index, 1, 1000000000)
        elif itemAbc == AttrDef.ActionRetryItem:
            return _createDftSpinBox(parent, option, index, 0, 1000000000)
        elif itemAbc == AttrDef.ActionChildItem:
            return _createDftLineEdit(parent, option, index)

        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        if isinstance(editor, QComboBox):
            super().setEditorData(editor, index)
            editor.showPopup()
            return
        super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        super().setModelData(editor, model, index)


def _createDftLineEdit(parent, option, index):
    return QLineEdit(parent)


def _createDftSpinBox(parent, option, index, minValue=0, maxValue=99999):
    spin = QSpinBox(parent)
    spin.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
    spin.setRange(minValue, maxValue)
    return spin


def _createBoolComboBox(parent, option, index):
    combo = QComboBox(parent)
    combo.addItem("True", True)
    combo.addItem("False", False)
    return combo


def _createActionClassComboBox(parent, option, index):
    combo = QComboBox(parent)
    combo.addItem("empty", "empty")
    combo.addItem("check", "check")
    combo.addItem("operate", "operate")
    combo.addItem("control", "control")
    return combo
