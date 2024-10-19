from PySide6 import QtCore
from PySide6.QtCore import QObject


class LogSigSink(QObject):

    # 请求输出日志信号
    logRequested = QtCore.Signal(dict)

    def __init__(self):
        super().__init__()

    def __call__(self, msg: dict, *args, **kwargs):
        self.logRequested.emit(msg)
