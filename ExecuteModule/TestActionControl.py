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
        return TestResult()

    def stop(self):
        print("stop control", self.getName(), self.getIden())
