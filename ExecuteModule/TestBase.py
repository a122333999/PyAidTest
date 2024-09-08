import uuid


def _isUuidStr(text):
    try:
        uuid.UUID(text)
        return True
    except ValueError:
        return False


class TestBase(object):

    _type = "base"

    def __init__(self):
        super().__init__()
        self._iden = uuid.uuid4()
        self._name = "BaseTest"
        self._desc = "This BaseTest"

    def setIden(self, iden):
        if isinstance(iden, str) and _isUuidStr(iden):
            self._iden = uuid.UUID(iden)
        elif isinstance(iden, uuid.UUID):
            self._iden = iden
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

