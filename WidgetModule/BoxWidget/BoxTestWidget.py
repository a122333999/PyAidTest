from PySide6.QtWidgets import QWidget, QLabel


class BoxTestWidget(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel("BoxTestWidget", self)

