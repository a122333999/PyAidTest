# -*- coding:utf-8 -*-

from ExecuteModule2.Executor.TestAction import TestAction
from UtilsModule.CommonUtils import CommonUtils


class TestActionControl(TestAction):

    classValue = 'control'

    def __init__(self):
        super().__init__()

    @classmethod
    def exec(self) :
        pass

    @classmethod
    def validJson(cls, data: dict, onlyHeader=True):
        pass

    @classmethod
    def copyData(cls, testAction: dict, onlyHeader=True):
        pass

    @classmethod
    def updateData(cls, testAction: dict, info: dict):
        pass


TestAction.controlAction = TestActionControl