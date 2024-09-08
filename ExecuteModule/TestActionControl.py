from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult


class TestActionControl(TestAction):

    _type = "control"

    def __init__(self):
        super().__init__()
        self.setName("TestControl")
        self.setDesc("This TestControl")

    def start(self, rtd):
        print("start control", rtd, self.getName(), self.getIden())
        if self.getClass() == 'fork':
            return _forkControl()
        elif self.getClass() == 'finished':
            return _finishedControl()
        elif self.getClass() == 'failed':
            return _failedControl()
        elif self.getClass() == 'waiting':
            return _waitingControl()
        else:
            return TestResult()

    def stop(self):
        print("stop control", self.getName(), self.getIden())


def _forkControl():
    return TestResult()


def _finishedControl():
    return TestResult()


def _failedControl():
    return TestResult()


def _waitingControl():
    return TestResult()

