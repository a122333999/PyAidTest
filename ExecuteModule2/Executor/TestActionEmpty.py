# -*- coding:utf-8 -*-

import ExecuteModule2.Executor.TestAction as TestAction
from UtilsModule.CommonUtils import CommonUtils


class TestActionEmpty(TestAction.TestAction):

    typeValue = 'empty'
    classValues = ['empty']

    def __init__(self):
        super().__init__()

    def exec(self) :
        print("TestActionEmpty exec")

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
        if not isinstance(data[cls.actionClassKey], str) or data[cls.actionClassKey] not in cls.classValues:
            return False
        if not isinstance(data[cls.actionDelayKey], int) or data[cls.actionDelayKey] < 0:
            return False
        if not isinstance(data[cls.actionTimesKey], int) or data[cls.actionTimesKey] < 1:
            return False
        if not isinstance(data[cls.actionForceKey], bool):
            return False
        if not isinstance(data[cls.actionConfigKey], dict):
            return False
        return True

    @classmethod
    def copyData(cls, testAction: dict, onlyHeader=True):
        pass

    @classmethod
    def updateData(cls, testAction: dict, info: dict):
        pass


TestAction.emptyActionClass = TestActionEmpty
