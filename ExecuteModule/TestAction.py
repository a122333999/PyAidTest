from ExecuteModule.TestBase import TestBase
from ExecuteModule.TestResult import TestResult
from UtilsModule.CommonUtils import CommonUtils


class TestAction(TestBase):
    def __init__(self):
        super().__init__()
        self.setName("TestAction")
        self.setDesc("This TestAction")
        self._class = ""
        self._delay = 500
        self._retry = 0
        self._child = None

    def exec(self) -> TestResult:
        pass

    def setClass(self, data):
        self._class = data

    def setDelay(self, data):
        self._delay = data

    def setRetry(self, data):
        self._retry = data

    def setChild(self, child):
        if CommonUtils.checkUuid(child):
            self._child = child

    def setConfig(self, data):
        pass

    def getClass(self):
        return self._class

    def getDelay(self):
        return self._delay

    def getRetry(self):
        return self._retry

    def getChild(self):
        return self._child

    def getConfig(self):
        pass


