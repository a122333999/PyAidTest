from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult


class TestActionEmpty(TestAction):

    _type = "empty"

    def __init__(self):
        super().__init__()

        self.setName("TestEmpty")
        self.setDesc("This TestEmpty")

    def start(self, rtd):
        print("start empty", rtd, self.getName(), self.getIden())
        return _noneEmpty()

    def stop(self):
        print("stop empty", self.getName(), self.getIden())


def _noneEmpty():
    return TestResult()
