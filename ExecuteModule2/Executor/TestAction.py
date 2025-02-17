# -*- coding:utf-8 -*-

from ExecuteModule2.Executor.TestBase import TestBase
from UtilsModule.CommonUtils import CommonUtils

emptyActionClass = None
searchActionClass = None
operateActionClass = None
controlActionClass = None


class TestAction(TestBase):

    actionClassKey = 'class'
    actionDelayKey = 'delay'
    actionTimesKey = 'times'
    actionForceKey = 'force'
    actionValidKey = 'valid'
    actionConfigKey = 'config'

    def __init__(self):
        super().__init__()

    @classmethod
    def exec(self) :
        pass

    @classmethod
    def validJson(cls, data: dict, onlyHeader=True):
        if subActionCls := _returnSubAction(data):
            return subActionCls.validJson(data, onlyHeader)
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
    if emptyActionClass and emptyActionClass.typeValue == at:
        return emptyActionClass
    elif searchActionClass and searchActionClass.typeValue == at:
        return searchActionClass
    elif operateActionClass and operateActionClass.typeValue == at:
        return operateActionClass
    elif controlActionClass and controlActionClass.typeValue == at:
        return controlActionClass
    else:
        return None
    

