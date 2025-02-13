# -*- coding:utf-8 -*-

from ExecuteModule2.Executor.TestBase import TestBase
from UtilsModule.CommonUtils import CommonUtils


class TestCase(TestBase):

    typeValue = 'case'

    caseTimesKey = 'times'
    caseActiveKey = 'active'
    caseActionsKey = 'actions'

    def __init__(self):
        super().__init__()

    def exec(self) :
        pass

    @classmethod
    def validJson(cls, data: dict, onlyHeader=True):
        if not isinstance(data[cls.baseTypeKey], str) or data[cls.baseTypeKey] != cls.typeValue:
            return False
        if not CommonUtils.checkUuid(data[cls.baseIdenKey]):
            return False
        if not isinstance(data[cls.baseNameKey], str):
            return False
        if not isinstance(data[cls.baseDescKey], str):
            return False
        if not isinstance(data[cls.caseTimesKey], int):
            return False
        if not isinstance(data[cls.caseActiveKey], bool):
            return False
        if not isinstance(data[cls.caseActionsKey], list):
            return False
        return True

    @classmethod
    def copyData(cls, testCase: dict, onlyHeader=True):
        return {
            cls.baseTypeKey: testCase[cls.baseTypeKey],
            cls.baseIdenKey: testCase[cls.baseIdenKey],
            cls.baseNameKey: testCase[cls.baseNameKey],
            cls.baseDescKey: testCase[cls.baseDescKey],
            cls.caseTimesKey: testCase[cls.caseTimesKey],
            cls.caseActiveKey: testCase[cls.caseActiveKey],
            cls.caseActionsKey: list(),
        }
    
    @classmethod
    def updateData(cls, testData: dict, info: dict):
        if cls.validJsoninfo(info, True):
            testData[cls.baseNameKey] = info[cls.baseNameKey]
            testData[cls.baseDescKey] = info[cls.baseDescKey]
            testData[cls.caseTimesKey] = info[cls.caseTimesKey]
            testData[cls.caseActiveKey] = info[cls.caseActiveKey]
            return True
        return False
