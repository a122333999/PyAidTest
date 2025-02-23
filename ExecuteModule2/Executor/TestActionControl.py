# -*- coding:utf-8 -*-

import ExecuteModule2.Executor.TestAction as TestAction
from UtilsModule.CommonUtils import CommonUtils


class TestActionControl(TestAction.TestAction):

    typeValue = 'control'
    classValues = ['if', 'for', 'input', 'pause', 'assert', 'finished', 'failed', 'script']

    def __init__(self):
        super().__init__()

    @classmethod
    def exec(self) :
        print("TestActionControl exec")

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
        return {
            cls.baseTypeKey: testAction[cls.baseTypeKey],
            cls.baseIdenKey: testAction[cls.baseIdenKey],
            cls.baseNameKey: testAction[cls.baseNameKey],
            cls.baseDescKey: testAction[cls.baseDescKey],
            cls.actionClassKey: testAction[cls.actionClassKey],
            cls.actionDelayKey: testAction[cls.actionDelayKey],
            cls.actionTimesKey: testAction[cls.actionTimesKey],
            cls.actionForceKey: testAction[cls.actionForceKey],
            cls.actionValidKey: testAction[cls.actionValidKey],
            cls.actionConfigKey: dict()
            #TODO: Add more keys
        }

    @classmethod
    def updateData(cls, testAction: dict, info: dict):
        return False


TestAction.controlActionClass = TestActionControl