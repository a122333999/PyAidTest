from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult


class TestActionControl(TestAction):

    _type = "control"

    def __init__(self):
        super().__init__()
        self.setName("TestControl")
        self.setDesc("This TestControl")

    def start(self):
        print("start control", self.getName(), self.getIden())
        if self.getClass() == 'fork':
            return _forkControl(self.getChild())
        elif self.getClass() == 'pause':
            return _pauseControl(self.getChild())
        elif self.getClass() == 'finished':
            return _finishedControl(self.getChild())
        elif self.getClass() == 'failed':
            return _failedControl(self.getChild())
        elif self.getClass() == 'script':
            return _scriptControl(self.getChild())
        else:
            return TestResult()

    def stop(self):
        print("stop control", self.getName(), self.getIden())



def _forkControl(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _inputControl(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _finishedControl(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _failedControl(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result


def _scriptControl(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result

