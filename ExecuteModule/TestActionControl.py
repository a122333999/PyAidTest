from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult


_defaultFork = {"goto": None, "exec": ""}
_defaultInput = {"form": "none", "tips": "请选择下一步动作:"}
_defaultScript = {"path": "", "args": ""}


class TestActionControl(TestAction):

    _type = "control"

    def __init__(self):
        super().__init__()
        self.setName("TestControl")
        self.setDesc("This TestControl")
        self._configFork = _defaultFork
        self._configInput = _defaultInput
        self._configScript = _defaultScript

    def exec(self):
        if self.getClass() == 'fork':
            return _forkControl(self.getChild())
        elif self.getClass() == 'input':
            return _inputControl(self.getChild())
        elif self.getClass() == 'finished':
            return _finishedControl(self.getChild())
        elif self.getClass() == 'failed':
            return _failedControl(self.getChild())
        elif self.getClass() == 'script':
            return _scriptControl(self.getChild())

        return TestResult(TestResult.CriticalFlag, "没有找到匹配的class")

    def setConfig(self, data):
        self._configFork = _returnConfigsValue('fork', data)
        self._configInput = _returnConfigsValue('input', data)
        self._configScript = _returnConfigsValue('script', data)

    def getConfig(self):
        return {
            "fork": self._configFork,
            "input": self._configInput,
            "script": self._configScript,
        }


def _returnConfigsValue(key: str, data: dict):
    ret = None
    if key == 'fork':
        ret = _defaultFork
        val = data.get(key, ret)
        if isinstance(val, dict):
            ret = val
    elif key == 'input':
        ret = _defaultInput
        val = data.get(key, ret)
        if isinstance(val, dict):
            ret = val
    elif key == 'script':
        ret = _defaultScript
        val = data.get(key, ret)
        if isinstance(val, dict):
            ret = val

    return ret



def _forkControl(node=None):
    result = TestResult(TestResult.RunningFlag, "")
    result.setNext(node)
    return result


def _inputControl(node=None):
    result = TestResult(TestResult.RunningFlag, "")
    result.setNext(node)
    return result


def _finishedControl(node=None):
    result = TestResult(TestResult.RunningFlag, "")
    result.setNext(node)
    return result


def _failedControl(node=None):
    result = TestResult(TestResult.RunningFlag, "")
    result.setNext(node)
    return result


def _scriptControl(node=None):
    result = TestResult(TestResult.RunningFlag, "")
    result.setNext(node)
    return result

