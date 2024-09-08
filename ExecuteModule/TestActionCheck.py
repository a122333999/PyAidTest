import pyautogui
from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult

_defaultCount = 15
_defaultTime = 3000
_defaultHit = 3


class TestActionCheck(TestAction):

    _type = "check"

    def __init__(self):
        super().__init__()
        self.setName("TestCheck")
        self.setDesc("This TestCheck")
        self._configCount = _defaultCount
        self._configTime = _defaultTime
        self._configHit = _defaultHit

    def start(self, rtd):
        print("start check", rtd, self.getName(), self.getIden())
        return TestResult()

    def stop(self):
        print("stop check", self.getName(), self.getIden())

    def setConfig(self, data):
        self._configCount = _returnConfigCount(data.get("count", _defaultCount))
        self._configTime = _returnConfigTime(data.get("time", _defaultTime))
        self._configHit = _returnConfigHit(data.get("hit", _defaultHit))

    def getConfig(self):
        return {
            "count": self._configCount,
            "time": self._configTime,
            "hit": self._configHit,
        }


def _returnConfigCount(data):
    if isinstance(data, int) and 0 < data:
        return data
    return _defaultCount


def _returnConfigTime(data):
    if isinstance(data, int) and 0 < data:
        return data
    return _defaultTime


def _returnConfigHit(data):
    if isinstance(data, int) and 0 < data:
        return data
    return _defaultHit