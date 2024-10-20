# -*- coding:utf-8 -*-

import time
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget, QTextEdit
from WidgetModule.LogWidget import LogInst as log
from WidgetModule.LogWidget.LogSigSink import LogSigSink


class LogWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._textEdit = QTextEdit()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._textEdit)

        self._sigSink = LogSigSink()
        self._sigSink.logRequested.connect(self.onLogRequested)
        log.addHandle("wid", self._sigSink)

    def clearContent(self):
        pass

    def onLogRequested(self, msg):
        at = time.localtime(msg['time'])
        st = time.strftime("%Y-%m-%d %H:%M:%S", at)
        self._textEdit.append(f"{st} [{msg['type']}] - {msg['text']}")

    def sizeHint(self):
        return QSize(-1, 150)

