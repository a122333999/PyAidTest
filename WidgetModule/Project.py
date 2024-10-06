import json
from PySide6.QtCore import QDir, QFileInfo


def load(file):
    return _projectObj.load(file)


def save(file):
    return _projectObj.save(file)


def isEmpty():
    return _projectObj.isEmpty()


def getProjectPath():
    return _projectObj.getProjectPath()


def getFileList():
    return _projectObj.getFileList()


def instance():
    return _projectObj


def createProject(path, name):
    return _projectObj.createProject(path, name)


class Project:

    def __init__(self):
        self._path = None
        self._data = None

    def load(self, file):
        try:
            with open(file, 'rb') as fp:
                self._data = json.load(fp)
                self._path = file
                return True
        except Exception as e:
            print("打开项目文件失败", e)
            return False

    def save(self, file):
        try:
            with open(file, 'w') as fp:
                json.dump(self._data, fp)
        except Exception as e:
            print("保存项目文件失败", e)
            return False

    def isEmpty(self):
        return self._path is None and self._data is None

    def getProjectPath(self):
        return self._path

    def getFileList(self):
        result = []
        if isinstance(self._data, dict):
            for item in self._data.get("file", []):
                if ("path" in item) and len(item["path"]):
                    result.append(item["path"])

        return result

    @classmethod
    def instance(cls):
        return _projectObj

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
        with open(qtDir.filePath(name + _projectExt), 'w') as fp:
            if fp.write(_projectTemp) != len(_projectTemp):
                return None
        # 验证是否成功
        info = QFileInfo(qtDir.filePath(name + _projectExt))
        if info.exists():
            return info.absoluteFilePath()


_projectObj = Project()
_projectExt = ".json"
_projectTemp = \
"""
{
    "info": {
         "version": 0,
         "prefix": {}
    },
    "file": []
}
"""
