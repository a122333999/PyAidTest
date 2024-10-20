# -*- coding:utf-8 -*-

import sys
import time
import uuid
import pyscreeze
import pyautogui
import pytesseract
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication
from ExecuteModule.Execute import Execute
from WidgetModule.Window import MainWindow


from ExecuteModule.TestRect import TestRect


handle = None
execute = None


@QtCore.Slot(dict)
def testSlot(info: dict):
    print(info)


if __name__ == '__main__':
    execute = Execute()
    execute.execSignal.connect(testSlot)

    print(pyautogui.locateOnScreen('./Docs/testimg1.png'))

    handle = execute.load("./Docs/test1.json")
    print(handle)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



