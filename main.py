# -*- coding:utf-8 -*-

import sys
import pyautogui

from PySide6.QtWidgets import QApplication
# from ExecuteModule.Execute import Execute
from ExecuteModule2.Execute import Execute
from WidgetModule.Window import MainWindow



if __name__ == '__main__':

    execute = Execute()
    # handle = execute.load("./Docs/test2.json")
    # print(handle)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



