from uuid import UUID
from PySide6 import QtCore
from ExecuteModule.TestGroup import TestGroup
from ExecuteModule.TestFactory import TestFactory


class Execute(QtCore.QObject):
    # 测试信号
    testSignal = QtCore.Signal(str)
    # 执行信号 1句柄 2{用例:动作}
    execSignal = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self._handleList = dict()

    def load(self, path):
        ret = TestFactory.importFile(path)
        if isinstance(ret, TestGroup):
            self._handleList[id(ret)] = ret
            return id(ret)
        return 0

    def unload(self, handle):
        self._handleList.pop(handle)

    def start(self, handle, case: int | UUID):  # 启动指定用例
        search = _findCase(self._handleList, handle, case)
        if search is not None:
            search.start()
            return True
        return False

    def startAll(self, handle):  # 启动整个组
        search = _findGroup(self._handleList, handle)
        if search is not None:
            for case in search.getCaseList():
                ret = case.start()
                if ret is False:
                    return False
        return True

    def stop(self, handle):  # 停止测试
        pass

    def getHandleList(self):
        result = list()
        for handle in self._handleList:
            result.append({
                "type": self._handleList[handle].getType(),
                "iden": self._handleList[handle].getIden(),
                "name": self._handleList[handle].getName(),
                "desc": self._handleList[handle].getDesc(),
            })
        return result

    def getHandleInfo(self, handle):
        if handle in self._handleList:
            return {
                "type": self._handleList[handle].getType(),
                "iden": self._handleList[handle].getIden(),
                "name": self._handleList[handle].getName(),
                "desc": self._handleList[handle].getDesc(),
            }

    def getCaseList(self, handle):
        result = list()
        search = _findGroup(self._handleList, handle)
        if search is not None:
            for item in search.getCaseList():
                result.append({
                    "type": item.getType(),
                    "iden": item.getIden(),
                    "name": item.getName(),
                    "desc": item.getDesc()
                })
        return result

    def getCaseInfo(self, handle, case: int | UUID):
        search = _findCase(self._handleList, handle, case)
        if search is not None:
            return {
                "type": search.getType(),
                "iden": search.getIden(),
                "name": search.getName(),
                "desc": search.getDesc(),
            }

    def getActionList(self, handle, case: int | UUID):
        result = list()
        search = _findCase(self._handleList, handle, case)
        if search is not None:
            for item in search.getActionList():
                result.append({
                    "type": item.getType(),
                    "iden": item.getIden(),
                    "name": item.getName(),
                    "desc": item.getDesc(),
                    "config": item.getConfig()
                })
        return result

    def getActionInfo(self, handle, case: int | UUID, action: UUID):
        search = _findAction(self._handleList, handle, case, action)
        if search is not None:
            return {
                "type": search.getType(),
                "iden": search.getIden(),
                "name": search.getName(),
                "desc": search.getDesc(),
                "config": search.getConfig()
            }


def _findGroup(dataset, handle):
    if handle in dataset:
        return dataset[handle]


def _findCase(dataset, handle, case: int | UUID):
    group = _findGroup(dataset, handle)
    if group is not None:
        lis = group.getCaseList()
        if isinstance(case, int) and case < len(lis):
            return lis[case]
        elif isinstance(case, UUID):
            for item in lis:
                if item.getIden() == case:
                    return item


def _findAction(dataset, handle, case: int | UUID, action: UUID):
    case = _findCase(dataset, handle, case)
    if case is not None:
        for item in case.getActionList():
            if item.getIden() == action:
                return item
