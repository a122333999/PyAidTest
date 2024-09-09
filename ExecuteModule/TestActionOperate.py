from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult
from ExecuteModule.TestResult import ExecStatus


class TestActionOperate(TestAction):
    _type = "operate"

    def __init__(self):
        super().__init__()
        self.setName("TestOperate")
        self.setDesc("This TestOperate")

    def start(self):
        print("start operate", self.getName(), self.getIden())
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
            return TestResult(ExecStatus.ErrorStatus)

    def stop(self):
        print("stop operate", self.getName(), self.getIden())


def _clickOperate(node=None):
    result = TestResult(ExecStatus.RunningStatus)
    result.setNext(node)
    return result


def _leftClickOperate(node=None):
    result = TestResult(ExecStatus.RunningStatus)
    result.setNext(node)
    return result


def _rightClickOperate(node=None):
    result = TestResult(ExecStatus.RunningStatus)
    result.setNext(node)
    return result


def _doubleClickOperate(node=None):
    result = TestResult(ExecStatus.RunningStatus)
    result.setNext(node)
    return result


def _moveOperate(node=None):
    result = TestResult(ExecStatus.RunningStatus)
    result.setNext(node)
    return result


def _dragOperate(node=None):
    result = TestResult(ExecStatus.RunningStatus)
    result.setNext(node)
    return result


def _wheelOperate(node=None):
    result = TestResult(ExecStatus.RunningStatus)
    result.setNext(node)
    return result


def _keyOperate(node=None):
    result = TestResult(ExecStatus.RunningStatus)
    result.setNext(node)
    return result


def _keysOperate(node=None):
    result = TestResult(ExecStatus.RunningStatus)
    result.setNext(node)
    return result


def _copyToOperate(node=None):
    result = TestResult(ExecStatus.RunningStatus)
    result.setNext(node)
    return result

