# -*- coding:utf-8 -*-

from ExecuteModule2.Executor.TestFile import TestFile
from ExecuteModule2.Executor.TestCase import TestCase
from ExecuteModule2.Executor.TestAction import TestAction
from ExecuteModule2.Executor.TestActionEmpty import TestActionEmpty
from ExecuteModule2.Executor.TestActionSearch import TestActionSearch
from ExecuteModule2.Executor.TestActionOperate import TestActionOperate
from ExecuteModule2.Executor.TestActionControl import TestActionControl


class TestFactory:

    caseKey = TestFile.fileCasesKey
    actionKey = TestCase.caseActionsKey

    @classmethod
    def validJson(cls, testFile: dict):
        if not TestFile.validJson(testFile):
            return False
        for testCase in testFile.get(cls.caseKey, list()):
            if not TestCase.validJson(testCase):
                return False
            for testAction in testCase.get(cls.actionKey, list()):
                if not TestAction.validJson(testAction):
                    return False
        return True
    
    @classmethod
    def copyTestFileHeader(cls, testFile: dict):
        return TestFile.copyData(testFile, True)
    
    @classmethod
    def copyTestCaseHeader(cls, testCase: dict):
        return TestCase.copyData(testCase, True)
    
    @classmethod
    def copyTestActionData(cls, testAction: dict):
        return {
            cls.baseTypeKey: testAction[cls.baseTypeKey],
            cls.baseIdenKey: testAction[cls.baseTypeKey],
            cls.baseNameKey: testAction[cls.baseTypeKey],
            cls.baseDescKey: testAction[cls.baseTypeKey],
            #TODO: Add more keys
        }
    
    @classmethod
    def updateTestFileHeader(cls, testFile: dict, info: dict):
        return False
    
    @classmethod
    def updateTestCaseHeader(cls, testCase: dict, info: dict):
        return False
    
    @classmethod
    def updateTestActionData(cls, testAction: dict, info: dict):
        return False
