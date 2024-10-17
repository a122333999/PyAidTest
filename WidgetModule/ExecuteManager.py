from PySide6.QtCore import QDir
from ExecuteModule.Execute import Execute


"""
界面数据结构定义:

-- Base 基础
{
    baseType: str(group);
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
    
    caseStart: str(UUID);
    caseActive: bool(启用);
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
    actionRetry: int(重试);
    actionChild: str(UUID);
}

-- Check Action 测试动作
{
    baseType: str(check);
    baseIden: str(UUID);
    baseName: str(测试动作名称);
    baseDesc: str(测试动作描述);
    
    actionClass: str(分类);
    actionDelay: int(延时);
    actionTimes: int(次数);
    actionRetry: int(重试);
    actionChild: str(UUID);
    
    checkRectTop: str(顶边界);
    checkRectLeft: str(左边界);
    checkRectRight: str(右边界);
    checkRectBottom: str(顶边界);
    checkOffsetTop: int(顶偏移);
    checkOffsetLeft: int(左偏移);
    checkOffsetRight: int(右偏移);
    checkOffsetBottom: int(底偏移);
    checkSource: [str(路径)];
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
    actionRetry: int(重试);
    actionChild: str(UUID);
    
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
    actionRetry: int(重试);
    actionChild: str(UUID);
    
    controlForkGoto: str(UUID);
    controlForkEval: str(表达式);
    controlInputTips: str(输入提示);
    controlInputForm: str(输入表单);
    controlScriptPath: str(脚本路径);
    controlScriptArgs: str(脚本参数);
}

"""

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
        if ret := _executeObj.getHandleInfo(_executeDict[entry]):
            return {
                "baseType": str("group"),
                "baseIden": str(ret["iden"]),
                "baseName": str(ret["name"]),
                "baseDesc": str(ret["desc"]),
            }


def getFileList():
    global _executeObj
    result = list()
    for ret in _executeObj.getHandleList():
        result.append({
            "baseType": str("group"),
            "baseIden": str(ret["iden"]),
            "baseName": str(ret["name"]),
            "baseDesc": str(ret["desc"]),
        })
    return result


def getCaseInfo(entry, index):
    global _executeObj, _executeDict
    if entry in _executeDict:
        if ret := _executeObj.getCaseInfo(_executeDict[entry], index):
            return {
                "baseType": str("case"),
                "baseIden": str(ret["iden"]),
                "baseName": str(ret["name"]),
                "baseDesc": str(ret["desc"]),
                "caseStart": str(ret["start"]),
                "caseActive": bool(ret["active"])
            }


def getCaseList(entry):
    global _executeObj, _executeDict
    result = list()
    if entry in _executeDict:
        for ret in _executeObj.getCaseList(_executeDict[entry]):
            result.append({
                "baseType": str("case"),
                "baseIden": str(ret["iden"]),
                "baseName": str(ret["name"]),
                "baseDesc": str(ret["desc"]),
                "caseStart": str(ret["start"]),
                "caseActive": bool(ret["active"])
            })
    return result


def getActionInfo(entry, index, uuid):
    global _executeObj, _executeDict
    if entry in _executeDict:
        if ret := _executeObj.getActionInfo(_executeDict[entry], index, uuid):
            temp = {
                "baseType": str("empty"),
                "baseIden": str(ret["iden"]),
                "baseName": str(ret["name"]),
                "baseDesc": str(ret["desc"]),
                "actionClass": str(ret["class"]),
                "actionDelay": str(ret["delay"]),
                "actionTimes": str(ret["times"]),
                "actionRetry": str(ret["retry"]),
                "actionChild": str(ret["child"]) if ret["child"] else None,
            }
            config = ret["config"]
            if "check" == ret["type"]:
                temp.update({
                    "baseType": str("check"),
                    "checkRectTop": str(config["rect"]["top"]) if config["rect"]["top"] else None,
                    "checkRectLeft": str(config["rect"]["left"]) if config["rect"]["left"] else None,
                    "checkRectRight": str(config["rect"]["right"]) if config["rect"]["right"] else None,
                    "checkRectBottom": str(config["rect"]["bottom"]) if config["rect"]["bottom"] else None,
                    "checkOffsetTop": int(config["offset"]["top"]),
                    "checkOffsetLeft": int(config["offset"]["left"]),
                    "checkOffsetRight": int(config["offset"]["right"]),
                    "checkOffsetBottom": int(config["offset"]["bottom"]),
                    "checkSource": [str(item) for item in config["source"]],
                    "checkTargets": [str(item) for item in config["targets"]],
                    "checkHit": int(config["hit"]),
                    "checkCount": int(config["count"]),
                    "checkDuration": int(config["duration"]),
                })
            if "operate" == ret["type"]:
                temp.update({
                    "baseType": str("operate"),
                    "operatePoint": str(config["point"]),
                    "operateOffsetX": int(config["offset"]["x"]),
                    "operateOffsetY": int(config["offset"]["y"]),
                    "operateTime": int(config["time"]),
                    "operateRoll": int(config["roll"]),
                    "operateKeys": [str(item) for item in config["keys"]],
                    "operateContent": str(config["content"]),
                })
            if "control" == ret["type"]:
                temp.update({
                    "baseType": str("control"),
                    "controlForkGoto": str(config["fork"]["goto"]),
                    "controlForkEval": str(config["fork"]["eval"]),
                    "controlInputTips": str(config["input"]["tips"]),
                    "controlInputForm": str(config["input"]["form"]),
                    "controlScriptPath": str(config["script"]["path"]),
                    "controlScriptArgs": str(config["script"]["args"]),
                })
            return temp


def getActionList(entry, index):
    global _executeObj, _executeDict
    result = list()
    if entry in _executeDict:
        for ret in _executeObj.getActionList(_executeDict[entry], index):
            result.append({
                "baseType": str("empty"),
                "baseIden": str(ret["iden"]),
                "baseName": str(ret["name"]),
                "baseDesc": str(ret["desc"]),
                "actionClass": str(ret["class"]),
                "actionDelay": str(ret["delay"]),
                "actionTimes": str(ret["times"]),
                "actionRetry": str(ret["retry"]),
                "actionChild": str(ret["child"]) if ret["child"] else None,
            })
            config = ret["config"]
            if "check" == ret["type"]:
                result[-1].update({
                    "baseType": str("check"),
                    "checkRectTop": str(config["rect"]["top"]) if config["rect"]["top"] else None,
                    "checkRectLeft": str(config["rect"]["left"]) if config["rect"]["left"] else None,
                    "checkRectRight": str(config["rect"]["right"]) if config["rect"]["right"] else None,
                    "checkRectBottom": str(config["rect"]["bottom"]) if config["rect"]["bottom"] else None,
                    "checkOffsetTop": int(config["offset"]["top"]),
                    "checkOffsetLeft": int(config["offset"]["left"]),
                    "checkOffsetRight": int(config["offset"]["right"]),
                    "checkOffsetBottom": int(config["offset"]["bottom"]),
                    "checkSource": [str(item) for item in config["source"]],
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
                    "operateContent": str(config["content"]),
                })
            if "control" == ret["type"]:
                result[-1].update({
                    "baseType": str("control"),
                    "controlForkGoto": str(config["fork"]["goto"]),
                    "controlForkEval": str(config["fork"]["eval"]),
                    "controlInputTips": str(config["input"]["tips"]),
                    "controlInputForm": str(config["input"]["form"]),
                    "controlScriptPath": str(config["script"]["path"]),
                    "controlScriptArgs": str(config["script"]["args"]),
                })
    return result


def hasHandle(entry):
    global _executeObj, _executeDict
    if entry in _executeDict:
        return _executeObj.hasHandle(_executeDict[entry])
