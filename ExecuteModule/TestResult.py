from enum import Enum


class ExecStatus(Enum):
    # ExecStatus = ("NoneStatus", "FinishedStatus", "FailedStatus", "RunningStatus",  "JumpingStatus", "WaitingStatus")
    NoneStatus = 0
    FinishedStatus = 1
    FailedStatus = 2
    RunningStatus = 3
    WaitingStatus = 5
    ErrorStatus = 6


class TestResult:

    def __init__(self, status=ExecStatus.NoneStatus):
        super().__init__()
        self._next = None
        self._rects = list()
        self._status = status
        self._callback = None

    def isValid(self):
        return bool(len(self._rects))

    def callback(self, *args) -> 'TestResult':
        if self._callback:
            ret = self._callback(self, args)
            if isinstance(ret, TestResult):
                return ret
        return TestResult()

    def getNext(self):
        return self._next

    def setNext(self, uuid):
        self._next = uuid

    def getStatus(self):
        return self._status

    def setCallback(self, callback):
        self._callback = callback

    def getCallback(self):
        return self._callback

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


