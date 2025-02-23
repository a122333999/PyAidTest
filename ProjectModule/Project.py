# -*- coding:utf-8 -*-

import json
import uuid

from PySide6.QtCore import QFileInfo, QDir, QObject
from ProjectModule import ProjectTemplate

# TODO: 打开任意文件都成功

class Project(QObject):

    ProjectModifiedEvent = 0
    ProjectLoadedEvent = 1
    ProjectSavedEvent = 2

    def __init__(self):
        super().__init__()
        self._data = None
        self._dirPath = None
        self._filePath = None
        self._modified = False

    def load(self, file):
        try:
            with open(file, 'rb') as fp:
                self._data = json.load(fp)
                self._dirPath = QFileInfo(file).absolutePath()
                self._filePath = QFileInfo(file).absoluteFilePath()
                return True
            pass
        except Exception as e:
            print("打开项目文件失败", e)
        return False

    def save(self, file):
        try:
            with open(file, 'w', encoding="utf8") as fp:
                json.dump(self._data, fp, indent=4, ensure_ascii=False)
                return True
        except Exception as e:
            print("保存项目文件失败", e)
        return False

    def unload(self):
        pass

    def isEmpty(self):
        return self._isEmpty()
    
    def isModified(self):
        return self._modified
    
    def setModified(self, modified):
        self._modified = modified

    def hasEntry(self, entry):
        return self._hasEntry(entry)

    def getEntryInfo(self, entry):
        if self._data:
            for item in self._data.get("entry", []):
                if item["file"] == entry:
                    return tuple(item.values())
        return None

    def getEntryList(self):
        result = []
        if self._data:
            for item in self._data.get("entry", []):
                result.append(tuple(item.values()))
        return result

    def getTestEntryList(self):
        result = []
        if self._data:
            for item in self._data.get("entry", []):
                if item["type"] == "test":
                    result.append(tuple(item.values()))
        return result

    def getScriptEntryList(self):
        result = []
        if self._data:
            for item in self._data.get("entry", []):
                if item["type"] == "script":
                    result.append(tuple(item.values()))
        return result

    def getResourceEntryList(self):
        result = []
        if self._data:
            for item in self._data.get("entry", []):
                if item["type"] == "resource":
                    result.append(tuple(item.values()))
        return result

    def entryToPath(self, entry):
        if ret := _entryToPath(entry, self._dirPath):
            if self._hasEntry(entry):
                return ret
        return None

    def pathToEntry(self, path):
        path = QFileInfo(path).absoluteFilePath()
        if ret := _pathToEntry(path, self._dirPath):
            if self._hasEntry(ret):
                return ret
        return None

    def addTestFile(self, path):
        path = QFileInfo(path).absoluteFilePath()
        entry = _pathToEntry(path, self._dirPath)
        if self._isEmpty():
            return False
        if self._hasEntry(entry):
            return False  # 已存在
        self._data["entry"].append({"file": entry, "type": "test"})
        return True

    def rmvEntry(self, entry):
        if self._hasEntry(entry):
            for item in self._data["entry"]:
                if item["file"] == entry:
                    self._data["entry"].remove(item)
                    return True
        return False

    def clearProject(self):
        pass

    def getProjectDirPath(self):
        return self._dirPath

    def getProjectFilePath(self):
        return self._filePath

    @classmethod
    def createProject(cls, path, name):
        qtDir = QDir(path)
        fileName = name + ProjectTemplate.getExt()
        # 当前目录不存在则创建
        if not qtDir.exists():
            qtDir.mkpath(path)
        # # 项目目录已存在
        if qtDir.exists(name):
            return None
        # # 创建项目目录失败
        if not qtDir.mkdir(name):
            return None
        # 进入项目目录失败
        if not qtDir.cd(name):
            return None
        # 把项目模板写入文件
        with open(qtDir.filePath(fileName), 'w', encoding="utf8") as fp:
            if fp.write(ProjectTemplate.getPt()) != len(ProjectTemplate.getPt()):
                return None
        # 验证是否成功
        info = QFileInfo(qtDir.filePath(fileName))
        if info.exists():
            return info.absoluteFilePath()
        # TODO: 创建Test/Script/Resource三个目录

    @classmethod
    def createTestFile(cls, path, name):
        qtDir = QDir(path)
        if not qtDir.exists():
            return None
        if qtDir.exists(name):
            return None
        temp = ProjectTemplate.getTft()
        dic = json.loads(temp)
        dic["iden"] = str(uuid.uuid4())
        dic["name"] = name
        dic["desc"] = "新建测试文件"
        with open(qtDir.filePath(name), 'w', encoding="utf8") as fp:
            text = json.dumps(dic, indent=4, ensure_ascii=False)
            if fp.write(text) != len(text):
                return None
        # 验证是否成功
        info = QFileInfo(qtDir.filePath(name))
        if info.exists():
            return info.absoluteFilePath()

    def _isEmpty(self):
        return self._dirPath is None or self._filePath is None or self._data is None

    def _hasEntry(self, entry):
        if self._data:
            for item in self._data.get("entry", []):
                if item["file"] == entry:
                    return True
        return False


def _entryToPath(entry, absBaseDir):
    absBaseDirInfo = QFileInfo(absBaseDir)
    if not absBaseDirInfo.isDir() or not absBaseDirInfo.isAbsolute():
        return None
    return QDir(absBaseDir).filePath(entry)


def _pathToEntry(absPath, absBaseDir):
    absPathInfo = QFileInfo(absPath)
    if not absPathInfo.isFile() or not absPathInfo.isAbsolute():
        return None
    absBaseDirInfo = QFileInfo(absBaseDir)
    if not absBaseDirInfo.isDir() or not absBaseDirInfo.isAbsolute():
        return None
    if absPath.find(absBaseDir) < 0:
        return None
    result = absPath.removeprefix(absBaseDir)
    if result.find("/") == 0:
        result = result.removeprefix("/")
    if len(result) == 0:
        return None
    return result
