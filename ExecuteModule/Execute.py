import pyautogui
from uuid import UUID
from PySide6 import QtCore
from UtilsModule.CommonUtils import CommonUtils
from ExecuteModule.TestGroup import TestGroup
from ExecuteModule.TestResult import TestResult
from ExecuteModule.TestFactory import TestFactory
from ExecuteModule.TestRuntime import TestRuntime
from ExecuteModule.TestInput import TestInput as Input

# TODO: 模块重入限制
# 说明: 测试组里的测试用例是有序的

""" 状态 """
StoppedStatus = 0
RunningStatus = 1
WaitingStatus = 2

""" 流程 """
Test1None = 0
Test1Failed = 1
Test1Finished = 2
Test1Next = 3
Test1Input = 4
Test1Error = 5

""" 初始化pyautogui设置"""
pyautogui.FAILSAFE = False


class Execute(QtCore.QObject):
    # 执行信号 1句柄 2{用例:动作}
    execSignal = QtCore.Signal(dict)
    # 新的记录被添加 1记录的key
    recordAdded = QtCore.Signal(str)

    Input = Input

    def __init__(self):
        super().__init__()
        self._handleList = dict()
        self._handlePath = dict()

    def load(self, path):
        ret = TestFactory.importFile(path)
        if isinstance(ret, TestGroup):
            self._handleList[id(ret)] = ret
            self._handlePath[id(ret)] = path
            return id(ret)
        return 0

    def unload(self, handle):
        self._handleList.pop(handle)
        self._handlePath.pop(handle)

    def save(self, handle):
        if group := _findGroup(self._handleList, handle):
            ret = TestFactory.exportFile(self._handlePath[handle], group)
            if not isinstance(ret, Exception) and ret:
                return True
            else:
                pass  # 输出错误
        return False

    def saveAs(self, handle, path):
        pass

    def start(self, handle, case: int | UUID):  # 启动指定用例
        return self._start(handle, case)

    def startAll(self, handle):  # 启动整个组
        if not TestRuntime.isRunning and not TestRuntime.isWaiting and not TestRuntime.isStopping:
            if search := _findGroup(self._handleList, handle):
                TestRuntime.currentHandle = handle
                for case in search.getCaseList():
                    ret = self._start(handle, case.getIden())
                    if ret is False:
                        return False
        return True

    def stop(self, handle):  # 停止测试
        if handle in self._handleList.keys():
            if TestRuntime.isRunning or TestRuntime.isWaiting:
                TestRuntime.isRunning = False
                TestRuntime.isWaiting = False
                TestRuntime.isStopping = True

    def input(self, handle, data: Input):
        if handle in self._handleList.keys():
            if TestRuntime.isWaiting:
                TestRuntime.inputData = data
                TestRuntime.isRunning = True
                TestRuntime.isWaiting = False
                TestRuntime.isStopping = False

    def getHandleList(self):
        result = list()
        for handle in self._handleList:
            search = _findGroup(self._handleList, handle)
            result.append(TestFactory.formatGroup(search, True))
        return result

    def getHandleInfo(self, handle):
        if search := _findGroup(self._handleList, handle):
            return TestFactory.formatGroup(search, True)

    def setHandleInfo(self, handle, info):
        if search := _findGroup(self._handleList, handle):
            return TestFactory.updateGroup(search, info)
        return False

    def getCaseList(self, handle):
        result = list()
        if search := _findGroup(self._handleList, handle):
            for item in search.getCaseList():
                result.append(TestFactory.formatCase(item, True))
        return result

    def getCaseInfo(self, handle, case: int | UUID):
        if search := _findCase(self._handleList, handle, case):
            return TestFactory.formatCase(search, True)

    def setCaseInfo(self, handle, case: int | UUID, info):
        if search := _findCase(self._handleList, handle, case):
            return TestFactory.updateCase(search, info)
        return False

    def getActionList(self, handle, case: int | UUID):
        result = list()
        if search := _findCase(self._handleList, handle, case):
            for item in search.getActionList():
                result.append(TestFactory.formatAction(item, True))
        return result

    def getActionInfo(self, handle, case: int | UUID, action: UUID):
        if search := _findAction(self._handleList, handle, case, action):
            return TestFactory.formatAction(search, True)

    def setActionInfo(self, handle, case: int | UUID, action: UUID, info):
        if search := _findAction(self._handleList, handle, case, action):
            return TestFactory.updateAction(search, info)
        return False

    def getErrorInfo(self):
        pass  # TODO

    def addPathPrefix(self, key, value):
        self.objectName()  # 无意义 避免警告
        TestRuntime.pathPrefix[key] = value

    def hasHandle(self, handle):
        return handle in self._handleList

    @QtCore.Slot(dict)
    def onCaseStatusChanged(self, data):
        status, schedule = StoppedStatus, Test1None
        if data.get('flag') == TestResult.NoneFlag:
            status, schedule = StoppedStatus, Test1None
        elif data.get('flag') == TestResult.FailedFlag:
            status, schedule = StoppedStatus, Test1Failed
        elif data.get('flag') == TestResult.FinishedFlag:
            status, schedule = StoppedStatus, Test1Finished
        elif data.get('flag') == TestResult.CriticalFlag:
            status, schedule = StoppedStatus, Test1Error
        elif data.get('flag') == TestResult.RunningFlag:
            status, schedule = RunningStatus, Test1Next
        elif data.get('flag') == TestResult.ErrorFlag:
            status, schedule = RunningStatus, Test1Error
        elif data.get('flag') == TestResult.InputtingFlag:
            status, schedule = WaitingStatus, Test1Input

        self.execSignal.emit({
            'status': status,
            'schedule': schedule,
            'iden': data.get('iden', None),
            'msgs': data.get('msg', None),
            'error': None
        })

    def _start(self, handle, case: int | UUID):  # 启动指定用例
        if not TestRuntime.isRunning and not TestRuntime.isWaiting and not TestRuntime.isStopping:
            search = _findCase(self._handleList, handle, case)
            if search and search.getActive():
                TestRuntime.clear()
                TestRuntime.currentHandle = handle
                search.statusChanged.connect(self.onCaseStatusChanged)
                search.exec()
                search.statusChanged.disconnect(self.onCaseStatusChanged)
                TestRuntime.clear()
                return True
        return False


def _findGroup(dataset, handle):
    if handle in dataset:
        return dataset[handle]


def _findCase(dataset, handle, case: int | UUID):
    if group := _findGroup(dataset, handle):
        lis = group.getCaseList()
        if isinstance(case, int) and case < len(lis):
            return lis[case]
        elif CommonUtils.checkUuid(case):
            for item in lis:
                if item.getIden() == case:
                    return item


def _findAction(dataset, handle, case: int | UUID, action: UUID):
    if case := _findCase(dataset, handle, case):
        for item in case.getActionList():
            if item.getIden() == action:
                return item
