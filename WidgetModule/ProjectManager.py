# -*- coding:utf-8 -*-

from ProjectModule.Project import Project


# TODO: 打开任意文件都成功


_projectObj = Project()
_projectModified = False
_projectObserver = dict()


def load(file):
    global _projectObj
    return _projectObj.load(file)


def save(file):
    global _projectObj
    return _projectObj.save(file)


def clear():
    global _projectObj, _projectModified, _projectObserver
    _projectObj = Project()
    _projectModified = False
    # _projectObserver.clear()  # 不清理


def isEmpty():
    global _projectObj
    return _projectObj.isEmpty()


def isModified():
    global _projectModified
    return _projectModified


def setModified(flag: bool):
    global _projectModified, _projectObserver
    if _projectModified != flag:
        _projectModified = flag
        for func in _projectObserver.values():
            func(ProjectModifiedEvent, {"modified": flag})
        return True
    return False


def getEntryList():
    global _projectObj
    return _projectObj.getEntryList()


def getEntryInfo(entry):
    global _projectObj
    return _projectObj.getEntryInfo(entry)


def getTestEntryList():
    global _projectObj
    return _projectObj.getTestEntryList()


def getScriptEntryList():
    global _projectObj
    return _projectObj.getScriptEntryList()


def getResourceEntryList():
    global _projectObj
    return _projectObj.getResourceEntryList()


def pathToEntry(path):
    global _projectObj
    return _projectObj.pathToEntry(path)


def entryToPath(entry):
    global _projectObj
    return _projectObj.entryToPath(entry)


def addTestFile(path):
    global _projectObj
    return _projectObj.addTestFile(path)


def rmvEntry(entry):
    global _projectObj
    return _projectObj.rmvEntry(entry)


def getProjectDirPath():
    global _projectObj
    return _projectObj.getProjectDirPath()


def getProjectFilePath():
    global _projectObj
    return _projectObj.getProjectFilePath()


def createProject(path, name):
    return Project.createProject(path, name)


def createTestFile(path, name):
    return Project.createTestFile(path, name)


# 事件类型
ProjectModifiedEvent = 0
ProjectLoadedEvent = 1
ProjectSavedEvent = 2
"""
# 事件数据
{
    # ProjectModifiedEvent
    "modified": bool,
}
"""


def addObserver(name, func):
    """ 回调函数 def func(event, data) """
    global _projectObserver
    if name in _projectObserver:
        return False  # 已存在
    _projectObserver[name] = func
    return True


def rmvObserver(name):
    global _projectObserver
    if name in _projectObserver:
        _projectObserver.pop(name)
        return True
    return False

