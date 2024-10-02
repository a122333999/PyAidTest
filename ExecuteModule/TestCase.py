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
        self._header = None
        self._actionList = list()
        self._actionHash = dict()

    def start(self):
        success = False
        if _checkActionList(self._header, self._actionHash):
            current = self._header
            TestRuntime.isRunning = True
            TestRuntime.currentResult = None  # TODO

            while current in self._actionHash:
                action = self._actionHash[current]
                result = action.start()
                if TestRuntime.isStopping:
                    TestRuntime.clear()
                    self.statusChanged.emit(_packInfo1(result, action, '手动停止'))
                    return True

                while True:
                    flag = False
                    if result.getFlags() == TestResult.NoneFlag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, '未知错误'))
                        # 发出运行错误信号
                        return False
                    if result.getFlags() & TestResult.CriticalFlag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, '致命错误'))
                        return False
                    if result.getFlags() & TestResult.FailedFlag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, '测试失败'))
                        return True
                    if result.getFlags() & TestResult.FinishedFlag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, '测试完成'))
                        return True
                    if result.getFlags() & TestResult.ErrorFlag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, '运行错误'))
                        flag = True
                    if result.getFlags() & TestResult.WaitingFlag:
                        TestRuntime.isWaiting = True
                        TestRuntime.isRunning = False
                        self.statusChanged.emit(_packInfo1(result, action, '输入数据'))
                        while True:
                            if TestRuntime.isRunning:
                                result = result.callback(TestRuntime.inputData)
                                break
                            elif TestRuntime.isStopping:
                                TestRuntime.clear()
                                self.statusChanged.emit(_packInfo1(result, action, '手动停止'))
                                return True
                            elif TestRuntime.isWaiting:
                                time.sleep(0.1)
                                time.sleep(0.1)
                            else:
                                TestRuntime.clear()
                                self.statusChanged.emit(_packInfo1(result, action, '未知错误'))
                                return False
                        flag = True
                    if result.getFlags() & TestResult.RunningFlag:
                        self.statusChanged.emit(_packInfo1(result, action, '正在运行'))
                        break
                    if not flag:
                        TestRuntime.clear()
                        self.statusChanged.emit(_packInfo1(result, action, '未知错误'))
                        return False

                TestRuntime.currentResult = result
                TestRuntime.historyResult[action.getIden()] = result
                time.sleep(action.getDelay() / 1000)
                current = result.getNext()
                success = True

        if not success:
            self.statusChanged.emit(_packInfo1(TestResult, None, '流程异常'))
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


def _packInfo1(flag, iden=None, msg=None):
    if isinstance(flag, TestResult):
        flag = flag.getFlags()
    if isinstance(iden, TestAction):
        iden = iden.getIden()
    return {'flag': flag, 'iden': iden, 'msg': msg}
