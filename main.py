# -*- coding:utf-8 -*-

import sys
import time
import uuid
import pyscreeze
import pyautogui
import pytesseract
from PySide6 import QtCore
from PySide6.QtCore import QMetaObject, QObject, QTimer
from PySide6.QtWidgets import QApplication
from ExecuteModule.Execute import Execute
from WidgetModule.Window import MainWindow


from ExecuteModule.TestRect import TestRect


handle = None
execute = None


@QtCore.Slot(dict)
def testSlot(info: dict):
    print(info)


class A(QObject):
    def __init__(self):
        super().__init__()

    @QtCore.Slot()
    def say(self):
        print(111)


if __name__ == '__main__':
    execute = Execute()
    execute.execSignal.connect(testSlot)

    print(pyautogui.locateOnScreen('./Docs/testimg1.png'))

    handle = execute.load("./Docs/test1.json")
    print(handle)

    a1 = A()
    a2 = A()
    print(A.say, a1.say, a2.say)

    # QMetaObject.invokeMethod(a1, "say")

    t = a1.say

    QTimer.singleShot(0, t)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



