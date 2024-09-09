import time
from ExecuteModule.TestBase import TestBase
from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import ExecStatus
from ExecuteModule.TestResult import TestResult
from ExecuteModule.TestRuntime import TestRuntime
from UtilsModule.CommonUtils import CommonUtils


class TestCase(TestBase):

    _type = "case"

    def __init__(self):
        super().__init__()
        self.setName("TestCase")
        self.setDesc("This TestCase")
        self._header = None
        self._actionList = list()
        self._actionHash = dict()

    def start(self):
        if _checkActionList(self._header, self._actionHash):
            current = self._header
            TestRuntime.clear()
            TestRuntime.isRunning = True
            TestRuntime.currResult = None  # TODO

            while current in self._actionHash:
                action = self._actionHash[current]
                result = action.start()
                if TestRuntime.isStopping:
                    TestRuntime.clear()
                    # 发出运行停止信号
                    return True

                while True:
                    if result.getStatus() == ExecStatus.NoneStatus:
                        TestRuntime.clear()
                        # 发出运行错误信号
                        return False
                    elif result.getStatus() == ExecStatus.ErrorStatus:
                        TestRuntime.clear()
                        # 发出运行错误信号
                        return False
                    elif result.getStatus() == ExecStatus.FailedStatus:
                        TestRuntime.clear()
                        # 发出测试失败信号
                        return True
                    elif result.getStatus() == ExecStatus.FinishedStatus:
                        TestRuntime.clear()
                        # 发出测试完成信号
                        return True
                    elif result.getStatus() == ExecStatus.WaitingStatus:
                        TestRuntime.isWaiting = True
                        TestRuntime.isRunning = False
                        # 发出等待输入信号
                        while True:
                            if TestRuntime.isRunning:
                                result = result.callback(TestRuntime.inputData)
                                break
                            elif TestRuntime.isStopping:
                                TestRuntime.clear()
                                # 发出运行停止信号
                                return True
                            elif TestRuntime.isWaiting:
                                time.sleep(0.1)
                                time.sleep(0.1)
                            else:
                                TestRuntime.clear()
                                # 发出运行错误信号
                                return False
                    elif result.getStatus() == ExecStatus.RunningStatus:
                        # 发出运行信息信号
                        break
                    else:
                        TestRuntime.clear()
                        # 发出运行错误信号
                        return False

                TestRuntime.currResult = result
                TestRuntime.bufferResult[action.getIden()] = result
                current = result.getNext()
        else:
            # 发出运行错误信号
            return False

    def setHeader(self, header):
        if ret := CommonUtils.checkUuid(header):
            self._header = ret

    def getHeader(self):
        return self._header

    def addActionItem(self, action):
        if isinstance(action, TestAction):
            self._actionList.append(action)
            self._actionHash[action.getIden()] = action

    def rmvActionItem(self, action):
        pass

    def getActionList(self):
        return self._actionList

    def checkActionList(self):
        return _checkActionList(self._header, self._actionHash)


def _checkActionList(header, actions):
    # TODO: 叶子节点是控制节点
    if CommonUtils.checkUuid(header) is not None:
        if header not in actions.keys():
            return False
    return True

