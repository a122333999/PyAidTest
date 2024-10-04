from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult


class TestActionEmpty(TestAction):

    _type = "empty"

    def __init__(self):
        super().__init__()

        self.setName("TestEmpty")
        self.setDesc("This TestEmpty")

    def exec(self):
        if self.getClass() == 'empty':
            return self._empty()
        return TestResult(TestResult.CriticalFlag, "执行empty错误: 没有找到匹配的class")

    def _empty(self):
        result = TestResult(TestResult.RunningFlag, "执行empty完成")
        result.setNext(self.getChild())
        return result



