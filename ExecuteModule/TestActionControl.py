from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult
from ExecuteModule.TestInput import TestInput
from ExecuteModule.TestRuntime import TestRuntime
from ExecuteModule.TestInterpret import TestInterpret


_defaultFork = {"goto": None, "eval": "last:len(rects)==0"}
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

        self._defaultEval = (lambda rects: len(rects) == 0)

    def exec(self):
        if self.getClass() == 'fork':
            return self._forkControl()
        elif self.getClass() == 'input':
            return self._inputControl()
        elif self.getClass() == 'finished':
            return self._finishedControl()
        elif self.getClass() == 'failed':
            return self._failedControl()
        elif self.getClass() == 'script':
            return self._scriptControl()

        return TestResult(TestResult.CriticalFlag, "执行control错误: 没有找到匹配的class")

    def setClass(self, data):
        if data in ['fork', 'input', 'finished', 'failed', 'script']:
            return super().setClass(data)
        return False

    def setConfig(self, data):
        self._configFork = _returnConfigsValue('fork', data)
        self._configInput = _returnConfigsValue('input', data)
        self._configScript = _returnConfigsValue('script', data)
        return True

    def getConfig(self):
        return {
            "fork": self._configFork,
            "input": self._configInput,
            "script": self._configScript,
        }

    def _forkControl(self):
        # 1获取Lambda表达式 2执行表达式 3返回结果
        fun, ret = TestInterpret.fn3(self._configFork["eval"], self._defaultEval)
        if fun is None:
            return TestResult(TestResult.CriticalFlag, "执行fork错误: 解析表达式异常")
        if ret is None:
            return TestResult(TestResult.CriticalFlag, "执行fork错误: 没有找到判断目标")

        try:
            result = TestResult(TestResult.RunningFlag, "执行fork完成")
            result.setNext(self.getChild())
            if fun(ret.getRectList()):
                result.setNext(self._configFork["goto"])
            return result
        except Exception as e:
            return TestResult(TestResult.CriticalFlag, f"执行fork错误: 执行表达式异常({e})")

    def _inputControl(self):
        # 返回等待输入的TestResult(包括设定回调)
        result = TestResult(TestResult.InputtingFlag, "执行input过程: 等待输入")
        result.setNext(self.getChild())
        result.setCallback(_inputHandle)
        return result

    def _finishedControl(self):
        result = TestResult(TestResult.FinishedFlag, "执行finished完成")
        result.setNext(self.getChild())
        return result

    def _failedControl(self):
        result = TestResult(TestResult.FailedFlag, "执行failed完成")
        result.setNext(self.getChild())
        return result

    def _scriptControl(self):
        self.getType()
        return TestResult(TestResult.CriticalFlag, "执行script错误: 功能未开发")


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


def _inputHandle(curr: TestResult, data: TestInput, *args):
    TestRuntime.buffInfo = data.getInputText()
    if data.getBehavior() == TestInput.Continuing:
        result = TestResult(TestResult.RunningFlag, "执行input完成: 继续执行")
        result.setNext(curr.getNext())
        return result
    elif data.getBehavior() == TestInput.Finished:
        result = TestResult(TestResult.FinishedFlag, "执行input完成: 测试完成")
        return result
    elif data.getBehavior() == TestInput.Failed:
        result = TestResult(TestResult.FailedFlag, "执行input完成: 测试失败")
        return result

    return TestResult(TestResult.CriticalFlag, "执行input错误: 输入数据不合法")
