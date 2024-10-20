# -*- coding:utf-8 -*-

from ProjectModule.Project import Project


# TODO: 打开任意文件都成功


_projectObj = Project()


def load(file):
    global _projectObj
    return _projectObj.load(file)


def save(file):
    global _projectObj
    return _projectObj.save(file)


def isEmpty():
    global _projectObj
    return _projectObj.isEmpty()


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




