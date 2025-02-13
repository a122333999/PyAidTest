# -*- coding:utf-8 -*-

from ExecuteModule2.Executor.TestBase import TestBase
from UtilsModule.CommonUtils import CommonUtils

print("TestAction")

class TestAction(TestBase):

    actionClassKey = 'class'
    actionDelayKey = 'delay'
    actionTimesKey = 'times'
    actionForceKey = 'force'
    actionValidKey = 'valid'
    actionConfigKey = 'config'

    emptyAction = None
    searchAction = None
    operateAction = None
    controlAction = None

    def __init__(self):
        super().__init__()

    @classmethod
    def exec(self) :
        pass

    @classmethod
    def validJson(cls, data: dict, onlyHeader=True):
        if subActionCls := _returnSubAction(data):
            return subActionCls.copyData(data, onlyHeader)
        return False

    @classmethod
    def copyData(cls, testAction: dict, onlyHeader=True):
        if subActionCls := _returnSubAction(testAction):
            return subActionCls.copyData(testAction, onlyHeader)
        return False

    @classmethod
    def updateData(cls, testAction: dict, info: dict):
        if subActionCls := _returnSubAction(testAction):
            return subActionCls.updateData(testAction, info)
        return False


def _returnSubAction(testAction):
    at = testAction[TestAction.baseTypeKey]
    if TestAction.emptyAction and TestAction.emptyAction.classValue == at:
        return TestAction.emptyAction
    elif TestAction.searchAction and TestAction.searchAction.classValue == at:
        return TestAction.searchAction
    elif TestAction.operateAction and TestAction.operateAction.classValue == at:
        return TestAction.operateAction
    elif TestAction.controlAction and TestAction.controlAction.classValue == at:
        return TestAction.controlAction
    else:
        return None
    

