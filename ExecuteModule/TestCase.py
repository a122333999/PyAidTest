import time
from PySide6 import QtCore
from ExecuteModule.TestBase import TestBase
from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult
from ExecuteModule.TestRuntime import TestRuntime
from UtilsModule.CommonUtils import CommonUtils


class TestCase(TestBase):

    _type = "case"

    """ { flag:int, iden:UUID, message:str } """
    statusChanged = QtCore.Signal(dict)

    def __init__(self):
        super().__init__()
        self.setName("TestCase")
        self.setDesc("This TestCase")
        self._start = None
        self._active = True
        self._actionList = list()
        self._actionHash = dict()

    def exec(self):
        # TODO: times未实现 有些Action没实现retry 有些Action没实现把前后截图放到TestResult
        success = False
        if _checkActionList(self._start, self._actionHash) and self._active:
            current = self._start
            TestRuntime.isRunning = True
            TestRuntime.currentResult = None  # TODO

            while current in self._actionHash:
                action = self._actionHash[current]
                result = action.exec()

                while True:
                    flag = False
                    if result.getFlags() == TestResult.NoneFlag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, result.getMessage()))
                        # 发出运行错误信号
                        return False
                    if result.getFlags() & TestResult.CriticalFlag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, result.getMessage()))
                        return False
                    if result.getFlags() & TestResult.FailedFlag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, result.getMessage()))
                        return True
                    if result.getFlags() & TestResult.FinishedFlag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, result.getMessage()))
                        return True
                    if result.getFlags() & TestResult.ErrorFlag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, result.getMessage()))
                        flag = True
                    if result.getFlags() & TestResult.InputtingFlag:
                        TestRuntime.isWaiting = True
                        TestRuntime.isRunning = False
                        self.statusChanged.emit(_packInfo1(result, action, result.getMessage()))
                        while True:
                            if TestRuntime.isRunning:
                                result = result.callback(TestRuntime.inputData)
                                break
                            elif TestRuntime.isStopping:
                                TestRuntime.clear()
                                self.statusChanged.emit(_packInfo1(TestResult.NoneFlag, None, '外部停止'))
                                return True
                            elif TestRuntime.isWaiting:
                                time.sleep(0.1)
                                time.sleep(0.1)
                            else:
                                TestRuntime.clear()
                                self.statusChanged.emit(_packInfo1(TestResult.CriticalFlag, None, '未知错误'))
                                return False
                        flag = True
                    if result.getFlags() & TestResult.RunningFlag:
                        self.statusChanged.emit(_packInfo1(result, action, result.getMessage()))
                        break
                    if not flag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, '未知错误'))
                        return False

                TestRuntime.currentResult = result
                TestRuntime.historyResult[action.getIden()] = result
                if TestRuntime.isStopping:
                    TestRuntime.clear()
                    self.statusChanged.emit(_packInfo1(TestResult.NoneFlag, None, '外部停止'))
                    return True

                time.sleep(action.getDelay() / 1000)
                current = result.getNext()
                success = True

        if not self._active:
            self.statusChanged.emit(_packInfo1(TestResult.CriticalFlag, None, '测试用例未激活'))
            return False

        if not success:
            self.statusChanged.emit(_packInfo1(TestResult.CriticalFlag, None, '测试流程异常'))
            return False

    def setStart(self, start):
        if CommonUtils.checkUuid(start) or start is None:
            self._start = start
            return True
        return False

    def getStart(self):
        return self._start

    def setActive(self, active: bool):
        self._active = bool(active)
        return True

    def getActive(self):
        return self._active

    def addActionItem(self, action):
        if isinstance(action, TestAction):
            self._actionList.append(action)
            self._actionHash[action.getIden()] = action

    def rmvActionItem(self, action):
        pass

    def getActionList(self):
        return self._actionList

    def checkActionList(self):
        return _checkActionList(self._start, self._actionHash)


def _checkActionList(header, actions):
    # TODO: 叶子节点是控制节点
    if CommonUtils.checkUuid(header):
        if header in actions.keys():
            return True
    return False


def _packInfo1(flag, iden=None, msg=None):
    if isinstance(flag, TestResult):
        flag = flag.getFlags()
    if isinstance(iden, TestAction):
        iden = iden.getIden()
    return {'flag': flag, 'iden': iden, 'msg': msg}
