# -*- coding:utf-8 -*-
import json
from ExecuteModule2.Executor.TestFactory import TestFactory

print("Execute")

class Execute():


    def __init__(self):
        super().__init__()
        self._handleList = dict(
            # handle: {
            #     path: str,
            #     lock: bool,
            #     data: dict,
            # }
        )


    def load(self, path):
        ret: dict = _readFile(path)
        if isinstance(ret, dict) and TestFactory.validJson(ret):
            handleValue = { 'data': ret, 'path': path, 'lock': False }
            self._handleList[id(handleValue)] = handleValue
            return id(handleValue)
        return 0

    def unload(self, handle):
        # TODO: 判断运行状态 其他函数也是
        self._handleList.pop(handle)
        return True


    def save(self, handle, path):
        if handleValue := self._handleList.get(handle, None):
            ret = _writeFile(path, handleValue['data'])
            if not isinstance(ret, Exception) and ret:
                return True
            else:
                pass  # 输出错误
        return False

    def start(self, handle, caseId):  # 启动指定用例
        return False

    def startAll(self, handle):  # 启动整个组
        # if not TestRuntime.isRunning and not TestRuntime.isWaiting and not TestRuntime.isStopping:
        #     if search := _findGroup(self._handleList, handle):
        #         TestRuntime.currentHandle = handle
        #         for case in search.getCaseList():
        #             ret = self._start(handle, case.getIden())
        #             if ret is False:
        #                 return False
        return True

    def stop(self, handle):  # 停止测试
        # if handle in self._handleList.keys():
        #     if TestRuntime.isRunning or TestRuntime.isWaiting:
        #         TestRuntime.isRunning = False
        #         TestRuntime.isWaiting = False
        #         TestRuntime.isStopping = True
        pass

    def input(self, handle, data):
        # if handle in self._handleList.keys():
        #     if TestRuntime.isWaiting:
        #         TestRuntime.inputData = data
        #         TestRuntime.isRunning = True
        #         TestRuntime.isWaiting = False
        #         TestRuntime.isStopping = False
        pass

    def getHandleList(self):
        result = list()
        for handle in self._handleList:
            if testFile := _findTestFile(self._handleList, handle):
                if header := TestFactory.copyTestFileHeader(testFile):
                    result.append(header)
        return result

    def getHandleInfo(self, handle):
        if testFile := _findTestFile(self._handleList, handle):
            if header := TestFactory.copyTestFileHeader(testFile):
                return header
        return None

    def setHandleInfo(self, handle, info):
        if testFile := _findTestFile(self._handleList, handle):
            return TestFactory.updateTestFileHeader(testFile, info)
        return False

    def getCaseList(self, handle):
        result = list()
        if testFile := _findTestFile(self._handleList, handle):
            for testCase in testFile.get(TestFactory.caseKey, list()):
                result.append(TestFactory.copyTestCaseHeader(testCase))
        return result

    def getCaseInfo(self, handle, caseId):
        if testCase := _findTestCase(self._handleList, handle, caseId):
            return TestFactory.copyTestCaseHeader(testCase)
        return None

    def setCaseInfo(self, handle, caseId, info):
        if testCase := _findTestCase(self._handleList, handle, caseId):
            return TestFactory.updateTestCaseHeader(testCase, info)
        return False

    def getActionList(self, handle, caseId):
        result = list()
        if testCase := _findTestCase(self._handleList, handle, caseId):
            for testAction in testCase.get(TestFactory.actionKey, list()):
                result.append(TestFactory.copyTestActionData(testAction))
        return result

    def getActionInfo(self, handle, caseId, actionId):
        if testAction := _findTestAction(self._handleList, handle, caseId, actionId):
            return TestFactory.copyTestActionData(testAction)
        return None

    def setActionInfo(self, handle, caseId, actionId, info):
        if testAction := _findTestAction(self._handleList, handle, caseId, actionId):
            return TestFactory.updateTestActionData(testAction, info)
        return False

    def getErrorInfo(self):
        pass  # TODO

    def addPathPrefix(self, key, value):
        # self.objectName()  # 无意义 避免警告
        # TestRuntime.pathPrefix[key] = value
        pass

    def hasHandle(self, handle):
        return handle in self._handleList

    #@QtCore.Slot(dict)
    def onCaseStatusChanged(self, data):
        # status, schedule = StoppedStatus, Test1None
        # if data.getPt('flag') == TestResult.NoneFlag:
        #     status, schedule = StoppedStatus, Test1None
        # elif data.getPt('flag') == TestResult.FailedFlag:
        #     status, schedule = StoppedStatus, Test1Failed
        # elif data.getPt('flag') == TestResult.FinishedFlag:
        #     status, schedule = StoppedStatus, Test1Finished
        # elif data.getPt('flag') == TestResult.CriticalFlag:
        #     status, schedule = StoppedStatus, Test1Error
        # elif data.getPt('flag') == TestResult.RunningFlag:
        #     status, schedule = RunningStatus, Test1Next
        # elif data.getPt('flag') == TestResult.ErrorFlag:
        #     status, schedule = RunningStatus, Test1Error
        # elif data.getPt('flag') == TestResult.InputtingFlag:
        #     status, schedule = WaitingStatus, Test1Input

        # self.execSignal.emit({
        #     'status': status,
        #     'schedule': schedule,
        #     'iden': data.getPt('iden', None),
        #     'msgs': data.getPt('msg', None),
        #     'error': None
        # })
        pass

    def _start(self, handle, caseId):  # 启动指定用例
        # if not TestRuntime.isRunning and not TestRuntime.isWaiting and not TestRuntime.isStopping:
        #     search = _findCase(self._handleList, handle, case)
        #     if search and search.getActive():
        #         TestRuntime.clear()
        #         TestRuntime.currentHandle = handle
        #         search.statusChanged.connect(self.onCaseStatusChanged)
        #         search.exec()
        #         search.statusChanged.disconnect(self.onCaseStatusChanged)
        #         TestRuntime.clear()
        #         return True
        return False


def _readFile(path):
    try:
        with open(path, "rb") as fp:
            return json.load(fp)
    except Exception as e:
        print(path)
        return e


def _writeFile(path, data):
    try:
        with open(path, "w", encoding="utf8") as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)
            return True
    except Exception as e:
        return e



def _findTestFile(dataset, handle):
    if handleValue := dataset.get(handle, None):
        return handleValue['data']


def _findTestCase(dataset, handle, caseId):
    if testFile := _findTestFile(dataset, handle):
        for testCase in testFile.get(TestFactory.caseKey, list()):
            if testCase[TestFactory.baseIdenKey] == caseId:
                return testCase


def _findTestAction(dataset, handle, caseId, actionId):
    if testCase := _findTestCase(dataset, handle, caseId):
        for testAction in testCase.get(TestFactory.actionKey, list()):
            if testAction[TestFactory.baseIdenKey] == actionId:
                return testAction
