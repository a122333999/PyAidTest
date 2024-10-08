from PySide6.QtWidgets import QWidget, QLabel


class BoxEditWidget(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel("BoxEditWidget", self)
