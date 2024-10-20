# -*- coding:utf-8 -*-

import json
from PySide6.QtCore import QFileInfo, QDir
from ProjectModule import ProjectTemplate


class Project:

    # 项目文件扩展名
    _ext = ".json"

    def __init__(self):
        self._path = None
        self._data = None

    def load(self, file):
        try:
            with open(file, 'rb') as fp:
                self._data = json.load(fp)
                self._path = QFileInfo(file).absoluteFilePath()
                return True
            pass
        except Exception as e:
            print("打开项目文件失败", e)
            return False

    def save(self, file):
        try:
            with open(file, 'w', encoding="utf8") as fp:
                json.dump(self._data, fp, indent=4, ensure_ascii=False)
        except Exception as e:
            print("保存项目文件失败", e)
            return False

    def isEmpty(self):
        return self._path is None or self._data is None

    def hasEntry(self, entry):
        return self.hasEntry_(entry)

    def getEntryInfo(self, entry):
        if self._data:
            for item in self._data.get("entry", []):
                if item["file"] == entry:
                    return item
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
        if self.hasEntry_(entry):
            dir_ = QFileInfo(self._path).absoluteDir()
            return dir_.filePath(entry)
        return None

    def pathToEntry(self, path):
        if self._path and self._data:
            dir_ = QFileInfo(self._path).absoluteDir()
            info = QFileInfo(path)
            for item in self._data.get("entry", []):
                if dir_.filePath(item["file"]) == info.absoluteFilePath():
                    return tuple(item.values())
        return None

    def clearProject(self):
        pass

    def getProjectPath(self):
        return self._path

    def getProjectDirectory(self):
        return QFileInfo(self._path).absolutePath()

    @classmethod
    def createProject(cls, path, name):
        qtDir = QDir(path)
        # 当前目录不存在则创建
        if not qtDir.exists():
            qtDir.mkpath(path)
        # # 项目目录已存在
        # if qtDir.exists(name):
        #     return None
        # # 创建项目目录失败
        # if not qtDir.mkdir(name):
        #     return None
        # 进入项目目录失败
        if not qtDir.cd(name):
            return None
        # 把项目模板写入文件
        with open(qtDir.filePath(name + cls._ext), 'w', encoding="utf8") as fp:
            if fp.write(ProjectTemplate.get()) != len(ProjectTemplate.get()):
                return None
        # 验证是否成功
        info = QFileInfo(qtDir.filePath(name + cls._ext))
        if info.exists():
            return info.absoluteFilePath()

    def hasEntry_(self, entry):
        if self._data:
            for item in self._data.get("entry", []):
                if item["file"] == entry:
                    return True
        return False
