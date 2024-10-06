from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget
from WidgetModule.AttrModel import AttrModel


class AttrWidget(QWidget):
    def __init__(self):
        super().__init__()

    def clearContent(self):
        pass

    def sizeHint(self):
        return QSize(200, -1)



