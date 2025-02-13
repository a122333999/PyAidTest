# -*- coding:utf-8 -*-

import uuid
from UtilsModule.CommonUtils import CommonUtils


class TestBase():

    baseTypeKey = 'type'
    baseIdenKey = 'iden'
    baseNameKey = 'name'
    baseDescKey = 'desc'

    class CheckResult:
        pass

    def __init__(self):
        super().__init__()

    @classmethod
    def exec(self) :
        return False

    @classmethod
    def validJson(cls, data: dict, onlyHeader=True):
        return False

    @classmethod
    def copyData(cls, testData: dict, onlyHeader=True):
        return False

    @classmethod
    def updateData(cls, testData: dict, info: dict):
        return False





