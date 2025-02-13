# -*- coding:utf-8 -*-

from ExecuteModule2.Executor.TestBase import TestBase
from UtilsModule.CommonUtils import CommonUtils


class TestFile(TestBase):

    typeValue = 'file'

    fileCasesKey = 'cases'

    def __init__(self):
        super().__init__()

    
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
        if not isinstance(data[cls.fileCasesKey], list):
            return False
        return True

    @classmethod
    def copyData(cls, testFile: dict, onlyHeader=True):
        return {
            cls.baseTypeKey: testFile[cls.baseTypeKey],
            cls.baseIdenKey: testFile[cls.baseIdenKey],
            cls.baseNameKey: testFile[cls.baseNameKey],
            cls.baseDescKey: testFile[cls.baseDescKey],
            cls.fileCasesKey: list(),
        }
    
    @classmethod
    def updateData(cls, testData: dict, info: dict):
        if cls.validJsoninfo(info, True):
            testData[cls.baseNameKey] = info[cls.baseNameKey]
            testData[cls.baseDescKey] = info[cls.baseDescKey]
            return True
        return False



