from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult


class TestActionOperate(TestAction):
    _type = "operate"

    def __init__(self):
        super().__init__()
        self.setName("TestOperate")
        self.setDesc("This TestOperate")

    def start(self, rtd):
        print("start operate", rtd, self.getName(), self.getIden())
        if self.getClass() == 'click':
            return _clickOperate()
        elif self.getClass() == 'leftClick':
            return _leftClickOperate()
        elif self.getClass() == 'rightClick':
            return _rightClickOperate()
        elif self.getClass() == 'doubleClick':
            return _doubleClickOperate()
        elif self.getClass() == 'move':
            return _moveOperate()
        elif self.getClass() == 'drag':
            return _dragOperate()
        elif self.getClass() == 'wheel':
            return _wheelOperate()
        elif self.getClass() == 'key':
            return _keyOperate()
        elif self.getClass() == 'keys':
            return _keysOperate()
        elif self.getClass() == 'copyTo':
            return _copyToOperate()
        else:
            return TestResult()

    def stop(self):
        print("stop operate", self.getName(), self.getIden())


def _clickOperate():
    return TestResult()


def _leftClickOperate():
    return TestResult()


def _rightClickOperate():
    return TestResult()


def _doubleClickOperate():
    return TestResult()


def _moveOperate():
    return TestResult()


def _dragOperate():
    return TestResult()


def _wheelOperate():
    return TestResult()


def _keyOperate():
    return TestResult()


def _keysOperate():
    return TestResult()


def _copyToOperate():
    return TestResult()

