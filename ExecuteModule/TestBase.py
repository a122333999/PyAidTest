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
        if ret := CommonUtils.checkUuid(iden):
            self._iden = ret
        else:
            raise TypeError("设置的的UUID不被支持", iden)

    def setName(self, name):
        self._name = name

    def setDesc(self, desc):
        self._desc = desc

    def getIden(self):
        return self._iden

    def getName(self):
        return self._name

    def getDesc(self):
        return self._desc

    @classmethod
    def getType(cls):
        return cls._type




