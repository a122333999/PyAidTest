from ExecuteModule.TestBase import TestBase


class TestCase(TestBase):

    _type = "case"

    def __init__(self):
        super().__init__()
        self.setName("TestCase")
        self.setDesc("This TestCase")
        self._actionList = list()
        self._currentRet = None    # 记录上个Action的返回结果
        self._historyRet = dict()  # 记录各个Action的返回结果

    def start(self):

        # 检查动作链是否完整
        self._currentRet = (0, 0)
        for action in self._actionList:
            self._currentRet = action.start(self._currentRet)
            self._historyRet[action.getIden()] = self._currentRet

    def stop(self):
        pass

    def addActionItem(self, action):
        self._actionList.append(action)

    def rmvActionItem(self, action):
        pass

    def getActionList(self):
        return self._actionList
