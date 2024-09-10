import sys
import uuid

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication
from ExecuteModule.Execute import Execute
from WidgetModule.Window import MainWindow


@QtCore.Slot(dict)
def testSlot(path):
    print(path)


if __name__ == '__main__':
    execute = Execute()
    execute.execSignal.connect(testSlot)

    ret = execute.load("./Docs/test1.json")
    print(ret)
    # print(execute.getHandleList())
    # print(execute.getHandleInfo(ret))
    # print(execute.getCaseList(ret))
    # print(execute.getCaseInfo(ret, uuid.UUID('3c425f31-344f-4383-bf52-d20828f8a043')))
    # print(execute.getActionList(ret, 0))
    # print(execute.getActionList(ret, uuid.UUID('3c425f31-344f-4383-bf52-d20828f8a043')))
    # print(execute.getActionInfo(ret, 0, uuid.UUID('741ee909-d55c-45b5-8516-20ed160479cc')))
    # print(execute.getActionInfo(ret, 0, uuid.UUID('9a0fff5c-3d29-4eba-acae-29f2bf4b52c3')))

    execute.start(ret, 0)
    execute.start(ret, 0)
    # execute.startAll(ret)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


