# -*- coding:utf-8 -*-

from PySide6.QtWidgets import QWidget, QLabel


class BoxEditWidget(QWidget):
    def __init__(self, iden: str):
        super().__init__()
        self._iden = iden
        label = QLabel("BoxEditWidget", self)
