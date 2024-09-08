from enum import Enum


class ExecStatus(Enum):
    # ExecStatus = ("NoneStatus", "FinishedStatus", "FailedStatus", "RunningStatus",  "JumpingStatus", "WaitingStatus")
    NoneStatus = 0
    FinishedStatus = 1
    FailedStatus = 2
    RunningStatus = 3
    JumpingStatus = 4
    WaitingStatus = 5


class TestResult:

    def __init__(self, status=ExecStatus.NoneStatus):
        super().__init__()
        self._rects = list()
        self._status = status

    def isValid(self):
        return bool(len(self._rects))

    def getStatus(self):
        return self._status

    def addRectItem(self, rect):
        self._rects.append(rect)

    def getRectSize(self):
        return len(self._rects)

    def getRectList(self):
        return self._rects

    def getRectInfo(self, index):
        return self._rects[index]

    def getCenterPoint(self, index=0, offset=(0, 0)):
        pass

    def getTopCenterPoint(self, index=0, offset=(0, 0)):
        pass

    def getTopRightPoint(self, index=0, offset=(0, 0)):
        pass

    def getTopLeftPoint(self, index=0, offset=(0, 0)):
        pass

    def getBottomCenterPoint(self, index=0, offset=(0, 0)):
        pass

    def getBottomRightPoint(self, index=0, offset=(0, 0)):
        pass

    def getBottomLeftPoint(self, index=0, offset=(0, 0)):
        pass

    def getRightCenterPoint(self, index=0, offset=(0, 0)):
        pass

    def getLeftCenterPoint(self, index=0, offset=(0, 0)):
        pass


