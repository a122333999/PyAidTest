from PySide6.QtCore import QAbstractItemModel


class AttrModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()

    def updateModel(self, path):
        self.beginResetModel()
        self.endResetModel()

    


