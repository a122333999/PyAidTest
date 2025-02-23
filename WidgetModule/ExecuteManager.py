# -*- coding:utf-8 -*-

from PySide6.QtCore import QObject, QDir
from ExecuteModule2.Execute import Execute


"""
界面数据结构定义:

-- Base 基础
{
    baseType: str(file);
    baseIden: str(UUID);
    baseName: str(测试组名称);
    baseDesc: str(测试组描述);
}

-- Case 测试用例
{
    baseType: str(case);
    baseIden: str(UUID);
    baseName: str(测试用例名称);
    baseDesc: str(测试用例描述);
    
    caseTimes: int(测试次数);
    caseActive: bool(启用测试);
}

-- Empty Action 空动作
{
    baseType: str(empty);
    baseIden: str(UUID);
    baseName: str(测试动作名称);
    baseDesc: str(测试动作描述);
    
    actionClass: str(分类);
    actionDelay: int(延时);
    actionTimes: int(次数);
    actionForce: bool(强制);
    actionValid: bool(有效);
}

-- Search Action 测试动作
{
    baseType: str(search);
    baseIden: str(UUID);
    baseName: str(测试动作名称);
    baseDesc: str(测试动作描述);
    
    actionClass: str(分类);
    actionDelay: int(延时);
    actionTimes: int(次数);
    actionForce: bool(强制);
    actionValid: bool(有效);
    
    checkRectTop: str(顶边界)|None;
    checkRectLeft: str(左边界)|None;
    checkRectRight: str(右边界)|None;
    checkRectBottom: str(顶边界)|None;
    checkOffsetTop: int(顶偏移);
    checkOffsetLeft: int(左偏移);
    checkOffsetRight: int(右偏移);
    checkOffsetBottom: int(底偏移);
    checkSource: str(路径);
    checkTargets: [str(路径)];
    checkHit: int(命中次数);
    checkCount: int(总共次数);
    checkDuration: int(持续时间);
    
}

-- Operate Action 操作动作
{
    baseType: str(operate);
    baseIden: str(UUID);
    baseName: str(测试动作名称);
    baseDesc: str(测试动作描述);
    
    actionClass: str(分类);
    actionDelay: int(延时);
    actionTimes: int(次数);
    actionForce: bool(强制);
    actionValid: bool(有效);
    
    operatePoint: str(操作点);
    operateOffsetX: int(X偏移);
    operateOffsetY: int(Y偏移);
    operateTime: int(时间);
    operateKeys: [str(按键)];
    operateRoll: int(滚动);
    operateContent: str(内容);
}

-- Control Action 操作动作
{
    baseType: str(control);
    baseIden: str(UUID);
    baseName: str(测试动作名称);
    baseDesc: str(测试动作描述);
    
    actionClass: str(分类);
    actionDelay: int(延时);
    actionTimes: int(次数);
    actionForce: bool(强制);
    actionValid: bool(有效);
    
    controlForkGoto: str(UUID)|None;
    controlForkEval: str(表达式);
    controlInputTips: str(输入提示);
    controlInputForm: str(输入表单);
    controlScriptPath: str(脚本路径);
    controlScriptArgs: str(脚本参数);
}

"""



class ExecuteManager(QObject):

    def __init__(self):
        super().__init__()
        self._executeObj = Execute()
        self._executeDir = QDir.current()
        self._executeDict = dict()

    def init(self, execPath=""):
        if  QDir(execPath).exists():
            self.uninit()
            self._executeDir = QDir(execPath)
            return True
        return False



    def uninit(self):
        for handle in self._executeDict.values():
            self._executeObj.unload(handle)
        self._executeDir = QDir.current()
        self._executeDict.clear()


    def load(self, entry):
        if entry not in self._executeDict:
            path = self._executeDir.filePath(entry)
            handle = self._executeObj.load(path)
            if 0 < handle:
                self._executeDict[entry] = handle
                return True
        return False


    def unload(self, entry):
        if handle := self._executeDict.get(entry, None):
            self._executeObj.unload(handle)
            self._executeDict.pop(entry)


    def save(self, entry):
        if handle := self._executeDict.get(entry, None):
            return self._executeObj.save(handle)
        return False


    def saveAs(entry, path):
        pass


    def start(entry, index):
        pass


    def getFileList(self):
        result = list()
        for ret in self._executeObj.getHandleList():
            result.append({
                "baseType": str("group"),
                "baseIden": str(ret["iden"]),
                "baseName": str(ret["name"]),
                "baseDesc": str(ret["desc"]),
            })
        return result


    def getFileInfo(self, entry):
        if handle := self._executeDict.get(entry, None):
            if ret := self._executeObj.getHandleInfo(handle):
                return {
                    "baseType": str("group"),
                    "baseIden": str(ret["iden"]),
                    "baseName": str(ret["name"]),
                    "baseDesc": str(ret["desc"]),
                }


    def setFileInfo(self, entry, info):
        if handle := self._executeDict.get(entry, None):
            return self._executeObj.setHandleInfo(handle, {
                "type": "group",
                "iden": str(info["baseIden"]),
                "name": str(info["baseName"]),
                "desc": str(info["baseDesc"]),
            })
        return False


    def getCaseList(self, entry):
        result = list()
        if handle := self._executeDict.get(entry, None):
            for ret in self._executeObj.getCaseList(handle):
                result.append({
                    "baseType": str("case"),
                    "baseIden": str(ret["iden"]),
                    "baseName": str(ret["name"]),
                    "baseDesc": str(ret["desc"]),
                    "caseTimes": int(ret["times"]),
                    "caseActive": bool(ret["active"])
                })
        return result


    def getCaseInfo(self, entry, caseId):
        if handle := self._executeDict.get(entry, None):
            if ret := self._executeObj.getCaseInfo(handle, caseId):
                return {
                    "baseType": str("case"),
                    "baseIden": str(ret["iden"]),
                    "baseName": str(ret["name"]),
                    "baseDesc": str(ret["desc"]),
                    "caseTimes": int(ret["times"]),
                    "caseActive": bool(ret["active"])
                }


    def setCaseInfo(self, entry, caseId, info):
        if handle := self._executeDict.get(entry, None):
            return self._executeObj.setCaseInfo(handle, caseId, {
                "type": "case",
                "iden": str(info["baseIden"]),
                "name": str(info["baseName"]),
                "desc": str(info["baseDesc"]),
                "times": int(info["caseTimes"]),
                "active": bool(info["caseActive"])
            })
        return False


    def getActionList(self, entry, caseId):
        result = list()
        if handle := self._executeDict.get(entry, None):
            for ret in self._executeObj.getActionList(handle, caseId):
                result.append({
                    "baseType": str("empty"),
                    "baseIden": str(ret["iden"]),
                    "baseName": str(ret["name"]),
                    "baseDesc": str(ret["desc"]),
                    "actionClass": str(ret["class"]),
                    "actionDelay": int(ret["delay"]),
                    "actionTimes": int(ret["times"]),
                    "actionForce": bool(ret["force"]),
                    "actionValid": bool(ret["valid"]),
                })
                config = ret["config"]
                if "search" == ret["type"]:
                    result[-1].update({
                        "baseType": str("search"),
                        "checkRectTop": str(config["rect"]["top"]) if config["rect"]["top"] else None,
                        "checkRectLeft": str(config["rect"]["left"]) if config["rect"]["left"] else None,
                        "checkRectRight": str(config["rect"]["right"]) if config["rect"]["right"] else None,
                        "checkRectBottom": str(config["rect"]["bottom"]) if config["rect"]["bottom"] else None,
                        "checkOffsetTop": int(config["offset"]["top"]),
                        "checkOffsetLeft": int(config["offset"]["left"]),
                        "checkOffsetRight": int(config["offset"]["right"]),
                        "checkOffsetBottom": int(config["offset"]["bottom"]),
                        "checkSource": str(config["source"]),
                        "checkTargets": [str(item) for item in config["targets"]],
                        "checkHit": int(config["hit"]),
                        "checkCount": int(config["count"]),
                        "checkDuration": int(config["duration"]),
                    })
                if "operate" == ret["type"]:
                    result[-1].update({
                        "baseType": str("operate"),
                        "operatePoint": str(config["point"]),
                        "operateOffsetX": int(config["offset"]["x"]),
                        "operateOffsetY": int(config["offset"]["y"]),
                        "operateTime": int(config["time"]),
                        "operateRoll": int(config["roll"]),
                        "operateKeys": [str(item) for item in config["keys"]],
                        "operateContent": str(config["copy"]),
                    })
                if "control" == ret["type"]:
                    result[-1].update({
                        "baseType": str("control"),
                    })
        return result

    def getActionInfo(self, entry, caseId, actionId):
        if handle := self._executeDict.get(entry, None):
            if ret := self._executeObj.getActionInfo(handle, caseId, actionId):
                result = {
                    "baseType": str("empty"),
                    "baseIden": str(ret["iden"]),
                    "baseName": str(ret["name"]),
                    "baseDesc": str(ret["desc"]),
                    "actionClass": str(ret["class"]),
                    "actionDelay": int(ret["delay"]),
                    "actionTimes": int(ret["times"]),
                    "actionForce": bool(ret["force"]),
                    "actionValid": bool(ret["valid"]),
                }
                config = ret["config"]
                if "search" == ret["type"]:
                    result.update({
                        "baseType": str("search"),
                        "checkRectTop": str(config["rect"]["top"]) if config["rect"]["top"] else None,
                        "checkRectLeft": str(config["rect"]["left"]) if config["rect"]["left"] else None,
                        "checkRectRight": str(config["rect"]["right"]) if config["rect"]["right"] else None,
                        "checkRectBottom": str(config["rect"]["bottom"]) if config["rect"]["bottom"] else None,
                        "checkOffsetTop": int(config["offset"]["top"]),
                        "checkOffsetLeft": int(config["offset"]["left"]),
                        "checkOffsetRight": int(config["offset"]["right"]),
                        "checkOffsetBottom": int(config["offset"]["bottom"]),
                        "checkSource": str(config["source"]),
                        "checkTargets": [str(item) for item in config["targets"]],
                        "checkHit": int(config["hit"]),
                        "checkCount": int(config["count"]),
                        "checkDuration": int(config["duration"]),
                    })
                if "operate" == ret["type"]:
                    result.update({
                        "baseType": str("operate"),
                        "operatePoint": str(config["point"]),
                        "operateOffsetX": int(config["offset"]["x"]),
                        "operateOffsetY": int(config["offset"]["y"]),
                        "operateTime": int(config["time"]),
                        "operateRoll": int(config["roll"]),
                        "operateKeys": [str(item) for item in config["keys"]],
                        "operateContent": str(config["copy"]),
                    })
                if "control" == ret["type"]:
                    result.update({
                        "baseType": str("control"),
                    })
                return result

    def setActionInfo(self, entry, caseId, actionId, info):
        if handle := self._executeDict.get(entry, None):
            temp = {
                "type": str("empty"),
                "iden": str(info["baseIden"]),
                "name": str(info["baseName"]),
                "desc": str(info["baseDesc"]),
                "class": str(info["actionClass"]),
                "delay": int(info["actionDelay"]),
                "times": int(info["actionTimes"]),
                "force": bool(info["actionForce"]),
                "valid": bool(info["actionValid"]),
                "config": {}  # 不能删除
            }
            if "search" == info["baseType"]:
                temp.update({
                    "type": str("search"),
                    "config": {
                        "rect": {
                            "top": str(info["checkRectTop"]) if isinstance(info["checkRectTop"], str) else None,
                            "left": str(info["checkRectLeft"]) if isinstance(info["checkRectLeft"], str) else None,
                            "right": str(info["checkRectRight"]) if isinstance(info["checkRectRight"], str) else None,
                            "bottom": str(info["checkRectBottom"]) if isinstance(info["checkRectBottom"], str) else None,
                        },
                        "offset": {
                            "top": int(info["checkOffsetTop"]),
                            "left": int(info["checkOffsetLeft"]),
                            "right": int(info["checkOffsetRight"]),
                            "bottom": int(info["checkOffsetBottom"])
                        },
                        "source": str(info["checkSource"]),
                        "targets": [str(item) for item in info["checkTargets"]],
                        "hit": int(info["checkHit"]),
                        "count": int(info["checkCount"]),
                        "duration": int(info["checkDuration"])
                    }
                })
            elif "operate" == info["baseType"]:
                temp.update({
                    "type": str("operate"),
                    "config": {
                        "point": str(info["operatePoint"]),
                        "offset": {
                            "x": int(info["operateOffsetX"]),
                            "y": int(info["operateOffsetY"]),
                        },
                        "time": int(info["operateTime"]),
                        "roll": int(info["operateRoll"]),
                        "keys": [str(item) for item in info["operateKeys"]],
                        "copy": str(info["operateContent"]),
                    }
                })
            elif "control" == info["baseType"]:
                temp.update({
                    "type": str("control"),
                    "config": {}
                })

            return self._executeObj.setActionInfo(handle, caseId, actionId, temp)
        return False

    def hasHandle(self, entry):
        if handle := self._executeDict.get(entry, None):
            return self._executeObj.hasHandle(handle)
