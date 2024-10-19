from ExecuteModule.TestBase import TestBase
from ExecuteModule.TestResult import TestResult
from UtilsModule.CommonUtils import CommonUtils


_defaultClass = "empty"
_defaultDelay = 500
_defaultTimes = 1
_defaultRetry = 0
_defaultChild = None


class TestAction(TestBase):
    def __init__(self):
        super().__init__()
        self.setName("TestAction")
        self.setDesc("This TestAction")
        self._class = ""
        self._delay = 500
        self._times = 1
        self._retry = 0
        self._child = None

    def exec(self) -> TestResult:
        pass

    def setClass(self, data):
        self._class = data
        return True

    def setDelay(self, data):
        self._delay = _defaultDelay
        if isinstance(data, int) and 0 <= data:
            self._delay = data
            return True
        return False

    def setTimes(self, data):
        self._times = _defaultTimes
        if isinstance(data, int) and 0 < data:
            self._times = data
            return True
        return False

    def setRetry(self, data):
        self._retry = _defaultTimes
        if isinstance(data, int) and 0 <= data:
            self._retry = data
            return True
        return False

    def setChild(self, child):
        self._child = _defaultChild
        if CommonUtils.checkUuid(child) or child is None:
            self._child = child
            return True
        return False

    def setConfig(self, data):
        return True

    def getClass(self):
        return self._class

    def getDelay(self):
        return self._delay

    def getTimes(self):
        return self._times

    def getRetry(self):
        return self._retry

    def getChild(self):
        return self._child

    def getConfig(self):
        pass
