from PySide6.QtWidgets import QWidget, QLabel


class BoxImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel("BoxImageWidget", self)

