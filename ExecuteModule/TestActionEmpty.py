from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult


class TestActionEmpty(TestAction):

    _type = "empty"

    def __init__(self):
        super().__init__()

        self.setName("TestEmpty")
        self.setDesc("This TestEmpty")

    def start(self):
        print("start empty", self.getName(), self.getIden())
        return _noneEmpty(self.getChild())

    def stop(self):
        print("stop empty", self.getName(), self.getIden())


def _noneEmpty(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result
