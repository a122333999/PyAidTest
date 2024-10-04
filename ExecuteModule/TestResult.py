

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
    InputtingFlag = 0x08
    ErrorFlag = 0x10
    CriticalFlag = 0x20

    def __init__(self, flags, msg):
        super().__init__()
        self._next = None
        self._flags = int(flags)
        self._rects = list()
        self._images = list()
        self._message = msg
        self._callback = None

    def isValid(self):
        return bool(len(self._rects))

    def callback(self, data, *args):
        if self._callback:
            ret = self._callback(self, data, *args)
            if isinstance(ret, TestResult):
                return ret

        return TestResult(TestResult.CriticalFlag, "回调处理不存在")

    def getNext(self):
        return self._next

    def setNext(self, uuid):
        self._next = uuid

    def getFlags(self):
        return self._flags

    def addImage(self, image):
        self._images.append(image)

    def getImages(self):
        return self._images

    def setMessage(self, msg):
        self._message = msg

    def getMessage(self):
        return self._message

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

