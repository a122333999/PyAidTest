# -*- coding:utf-8 -*-

from ProjectModule.Project import Project


# TODO: 打开任意文件都成功


_projectObj = Project()
_projectModified = False


def load(file):
    global _projectObj
    return _projectObj.load(file)


def save(file):
    global _projectObj
    return _projectObj.save(file)


def clear():
    global _projectObj
    _projectObj = Project()


def isEmpty():
    global _projectObj
    return _projectObj.isEmpty()


def isModified():
    global _projectModified
    return _projectModified


def setModified(flag):
    global _projectModified
    _projectModified = flag


def getEntryList():
    global _projectObj
    return _projectObj.getEntryList()


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


def getProjectPath():
    global _projectObj
    return _projectObj.getProjectPath()


def getProjectDirectory():
    global _projectObj
    return _projectObj.getProjectDirectory()


def createProject(path, name):
    return Project.createProject(path, name)


def addObserver(name, func):
    pass


