from PySide6.QtWidgets import QWidget, QLabel


class BoxImageWidget(QWidget):
    def __init__(self, iden: str):
        super().__init__()
        self._iden = iden
        label = QLabel("BoxImageWidget", self)

