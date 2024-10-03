from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult


class TestActionEmpty(TestAction):

    _type = "empty"

    def __init__(self):
        super().__init__()

        self.setName("TestEmpty")
        self.setDesc("This TestEmpty")

    def exec(self):
        return _noneEmpty(self.getChild())


def _noneEmpty(node=None):
    result = TestResult(TestResult.RunningFlag)
    result.setNext(node)
    return result
