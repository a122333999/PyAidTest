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
        return TestResult()

    def stop(self):
        print("stop operate", self.getName(), self.getIden())
