from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult


_defaultPoint = "user:{0,0}"
_defaultOffset = {"x": 0, "y": 0}
_defaultTime = 10
_defaultKeys = ["Ctrl"]
_defaultRoll = 0
_defaultContent = "buff:clear"


class TestActionOperate(TestAction):
    _type = "operate"

    def __init__(self):
        super().__init__()
        self.setName("TestOperate")
        self.setDesc("This TestOperate")
        self._configPoint = _defaultPoint
        self._configOffset = _defaultOffset
        self._configTime = _defaultTime
        self._configKeys = _defaultKeys
        self._configRoll = _defaultRoll
        self._configContent = _defaultContent

    def exec(self):
        if self.getClass() == 'click':
            return _clickOperate(self.getChild())
        elif self.getClass() == 'leftClick':
            return _leftClickOperate(self.getChild())
        elif self.getClass() == 'rightClick':
            return _rightClickOperate(self.getChild())
        elif self.getClass() == 'doubleClick':
            return _doubleClickOperate(self.getChild())
        elif self.getClass() == 'move':
            return _moveOperate(self.getChild())
        elif self.getClass() == 'drag':
            return _dragOperate(self.getChild())
        elif self.getClass() == 'wheel':
            return _wheelOperate(self.getChild())
        elif self.getClass() == 'key':
            return _keyOperate(self.getChild())
        elif self.getClass() == 'keys':
            return _keysOperate(self.getChild())
        elif self.getClass() == 'copyTo':
            return _copyToOperate(self.getChild())
        else:
            return TestResult(TestResult.ErrorFlag)

    def setConfig(self, data):
        self._configPoint = _returnConfigsValue('point', data)
        self._configOffset = _returnConfigsValue('offset', data)
        self._configTime = _returnConfigsValue('time', data)
        self._configKeys = _returnConfigsValue('keys', data)
        self._configRoll = _returnConfigsValue('roll', data)
        self._configContent = _returnConfigsValue('content', data)

    def getConfig(self):
        return {
            "point": self._configPoint,
            "offset": self._configOffset,
            "time": self._configTime,
            "keys": self._configKeys,
            "roll": self._configRoll,
            "content": self._configContent
        }


def _returnConfigsValue(key: str, data: dict):
    ret = None
    if key == 'point':
        ret = _defaultPoint
        val = data.get(key, ret)
        if isinstance(val, str):
            ret = val
    elif key == 'offset':
        ret = _defaultOffset
        val = data.get(key, ret)
        if isinstance(val, dict):
            ret = val
    elif key == 'time':
        ret = _defaultTime
        val = data.get(key, ret)
        if isinstance(val, int) and 0 < val:
            ret = val
    elif key == 'keys':
        ret = _defaultKeys
        val = data.get(key, ret)
        if isinstance(val, list):
            ret = val
    elif key == 'roll':
        ret = _defaultRoll
        val = data.get(key, ret)
        if isinstance(val, int) and 0 < val:
            ret = val
    elif key == 'content':
        ret = _defaultContent
        val = data.get(key, ret)
        if isinstance(val, str):
            ret = val

    return ret


def _clickOperate(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _leftClickOperate(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _rightClickOperate(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _doubleClickOperate(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _moveOperate(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _dragOperate(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _wheelOperate(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _keyOperate(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _keysOperate(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _copyToOperate(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result

