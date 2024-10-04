import pyautogui
from uuid import UUID
from PySide6 import QtCore
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

    def load(self, path):
        ret = TestFactory.importFile(path)
        if isinstance(ret, TestGroup):
            self._handleList[id(ret)] = ret
            return id(ret)
        return 0

    def unload(self, handle):
        self._handleList.pop(handle)

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
            result.append({
                "type": self._handleList[handle].getType(),
                "iden": self._handleList[handle].getIden(),
                "name": self._handleList[handle].getName(),
                "desc": self._handleList[handle].getDesc(),
            })
        return result

    def getHandleInfo(self, handle):
        if handle in self._handleList:
            return {
                "type": self._handleList[handle].getType(),
                "iden": self._handleList[handle].getIden(),
                "name": self._handleList[handle].getName(),
                "desc": self._handleList[handle].getDesc(),
            }

    def getCaseList(self, handle):
        result = list()
        search = _findGroup(self._handleList, handle)
        if search is not None:
            for item in search.getCaseList():
                result.append({
                    "type": item.getType(),
                    "iden": item.getIden(),
                    "name": item.getName(),
                    "desc": item.getDesc()
                })
        return result

    def getCaseInfo(self, handle, case: int | UUID):
        search = _findCase(self._handleList, handle, case)
        if search is not None:
            return {
                "type": search.getType(),
                "iden": search.getIden(),
                "name": search.getName(),
                "desc": search.getDesc(),
            }

    def getActionList(self, handle, case: int | UUID):
        result = list()
        search = _findCase(self._handleList, handle, case)
        if search is not None:
            for item in search.getActionList():
                result.append({
                    "type": item.getType(),
                    "iden": item.getIden(),
                    "name": item.getName(),
                    "desc": item.getDesc(),
                    "config": item.getConfig()
                })
        return result

    def getActionInfo(self, handle, case: int | UUID, action: UUID):
        search = _findAction(self._handleList, handle, case, action)
        if search is not None:
            return {
                "type": search.getType(),
                "iden": search.getIden(),
                "name": search.getName(),
                "desc": search.getDesc(),
                "config": search.getConfig()
            }

    def getErrorInfo(self):
        pass  # TODO

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
    group = _findGroup(dataset, handle)
    if group is not None:
        lis = group.getCaseList()
        if isinstance(case, int) and case < len(lis):
            return lis[case]
        elif isinstance(case, UUID):
            for item in lis:
                if item.getIden() == case:
                    return item


def _findAction(dataset, handle, case: int | UUID, action: UUID):
    case = _findCase(dataset, handle, case)
    if case is not None:
        for item in case.getActionList():
            if item.getIden() == action:
                return item
