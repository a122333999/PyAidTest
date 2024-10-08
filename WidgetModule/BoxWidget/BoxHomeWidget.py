from PySide6.QtWidgets import QWidget, QLabel


class BoxHomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel("BoxHomeWidget", self)
