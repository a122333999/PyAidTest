# -*- coding:utf-8 -*-

import uuid
from PySide6.QtCore import QObject
from UtilsModule.CommonUtils import CommonUtils


class TestBase(QObject):

    _type = "base"

    def __init__(self):
        super().__init__()
        self._iden = uuid.uuid4()
        self._name = "BaseTest"
        self._desc = "This BaseTest"

    def setIden(self, iden):
        if CommonUtils.checkUuid(iden):
            self._iden = iden
            return True
        return False

    def setName(self, name):
        if len(name):
            self._name = name
            return True
        return False

    def setDesc(self, desc):
        self._desc = desc
        return True

    def getIden(self):
        return self._iden

    def getName(self):
        return self._name

    def getDesc(self):
        return self._desc

    @classmethod
    def getType(cls):
        return cls._type




