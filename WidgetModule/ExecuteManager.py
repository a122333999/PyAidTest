from PySide6.QtCore import QDir
from ExecuteModule.Execute import Execute


_executeObj = Execute()
_executeDir = QDir.current()
_executeDict = dict()


def init(execPath=""):
    dir_ = QDir(execPath)
    if dir_.exists():
        global _executeDir
        _executeDir = dir_
        return True
    return False


def uninit():
    global _executeObj, _executeDir, _executeDict
    _executeDir = QDir.current()
    for item in _executeDict:
        _executeObj.unload(item)
    _executeDict.clear()


def load(entry):
    global _executeDict
    if entry in _executeDict:
        return True

    path = _executeDir.filePath(entry)
    handle = _executeObj.load(path)
    if 0 < handle:
        _executeDict[entry] = handle
        return True

    return False


def unload(entry):
    global _executeObj, _executeDict
    _executeObj.unload(_executeDict["entry"])
    _executeDict.pop("entry")


def start(entry, index):
    global _executeObj, _executeDict
    if entry in _executeDict:
        return _executeObj.start(_executeDict[entry], index)


def getFileInfo(entry):
    global _executeObj, _executeDict
    if entry in _executeDict:
        return _executeObj.getHandleInfo(_executeDict[entry])


def getFileList():
    global _executeObj
    return _executeObj.getHandleList()


def getCaseInfo(entry, index):
    global _executeObj, _executeDict
    if entry in _executeDict:
        return _executeObj.getCaseInfo(_executeDict[entry], index)


def getCaseList(entry):
    global _executeObj, _executeDict
    if entry in _executeDict:
        return _executeObj.getCaseList(_executeDict[entry])


def getActionInfo(entry, index, uuid):
    global _executeObj, _executeDict
    if entry in _executeDict:
        return _executeObj.getActionInfo(_executeDict[entry], index, uuid)


def getActionList(entry, index):
    global _executeObj, _executeDict
    if entry in _executeDict:
        return _executeObj.getActionList(_executeDict[entry], index)


def hasHandle(entry):
    global _executeObj, _executeDict
    if entry in _executeDict:
        return _executeObj.hasHandle(_executeDict[entry])
