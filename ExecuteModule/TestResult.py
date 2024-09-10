from enum import Enum


class TestResult:

    """
    stop:none       NoneFlag
    stop:failed     FailedFlag
    stop:finished   FinishedFlag
    stop:next       X
    stop:input      X
    stop:error      CriticalFlag
    run:none        X
    run:failed      X
    run:finished    X
    run:next        RunningFlag
    run:input       X
    run:error       ErrorFlag
    wait:none       X
    wait:failed     X
    wait:finished   X
    wait:next       X
    wait:input      WaitingFlag
    wait:error      X
    """
    NoneFlag = 0x00
    FinishedFlag = 0x01
    FailedFlag = 0x02
    RunningFlag = 0x04
    WaitingFlag = 0x08
    ErrorFlag = 0x10
    CriticalFlag = 0x20

    def __init__(self, status=NoneFlag):
        super().__init__()
        self._next = None
        self._rects = list()
        self._status = int(status)
        self._callback = None
        # 错误信息

    def isValid(self):
        return bool(len(self._rects))

    def callback(self, *args):
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
