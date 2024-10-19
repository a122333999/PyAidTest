from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem
from WidgetModule.AttrWidget import AttrDefine as AttrDef
from UtilsModule.CommonUtils import CommonUtils


class AttrBaseHeader(QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        self.setText(0, "基础")
        self.setFirstColumnSpanned(True)

        self._baseType = QTreeWidgetItem(self)
        self._baseType.setText(0, "类型")
        self._baseType.setText(1, "测试用例")
        self._baseType.setData(1, AttrDef.ItemAbcRole, AttrDef.BaseTypeItem)
        self._baseIden = QTreeWidgetItem(self)
        self._baseIden.setText(0, "标识")
        self._baseIden.setText(1, "UUID")
        self._baseIden.setData(1, AttrDef.ItemAbcRole, AttrDef.BaseIdenItem)
        self._baseName = QTreeWidgetItem(self)
        self._baseName.setText(0, "名称")
        self._baseName.setText(1, "测试用例名称")
        self._baseName.setData(1, AttrDef.ItemAbcRole, AttrDef.BaseNameItem)
        self._baseName.setFlags(self._baseName.flags() | Qt.ItemFlag.ItemIsEditable)
        self._baseDesc = QTreeWidgetItem(self)
        self._baseDesc.setText(0, "描述")
        self._baseDesc.setText(1, "测试用例描述")
        self._baseDesc.setData(1, AttrDef.ItemAbcRole, AttrDef.BaseDescItem)
        self._baseDesc.setFlags(self._baseDesc.flags() | Qt.ItemFlag.ItemIsEditable)

    def setInfo(self, info):
        typeMap = {
            "group": "测试文件",
            "case": "测试用例",
            "empty": "空动作",
            "check": "检查动作",
            "operate": "操作动作",
            "control": "控制动作",
        }
        baseType = info.get("baseType", "")
        baseType = typeMap.get(baseType, baseType)
        self._baseType.setText(1, baseType)
        self._baseIden.setText(1, info.get("baseIden", ""))
        self._baseName.setText(1, info.get("baseName", ""))
        self._baseDesc.setText(1, info.get("baseDesc", ""))

    def getInfo(self, info):
        baseName = self._baseName.text(1)
        baseName = baseName if len(baseName) else info["baseName"]
        baseDesc = self._baseDesc.text(1)
        info.update({
            "baseName": baseName,
            "baseDesc": baseDesc
        })

    def updateItem(self):
        pass


class AttrCaseHeader(QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        self.setText(0, "测试用例")
        self.setFirstColumnSpanned(True)

        self._caseActive = QTreeWidgetItem(self)
        self._caseActive.setText(0, "启用")
        self._caseActive.setText(1, "False")
        self._caseActive.setData(1, AttrDef.ItemAbcRole, AttrDef.CaseActiveItem)
        self._caseActive.setFlags(self._caseActive.flags() | Qt.ItemFlag.ItemIsEditable)
        self._caseStart = QTreeWidgetItem(self)
        self._caseStart.setText(0, "起始")
        self._caseStart.setText(1, "UUID")
        self._caseStart.setData(1, AttrDef.ItemAbcRole, AttrDef.CaseStartItem)
        self._caseStart.setFlags(self._caseStart.flags() | Qt.ItemFlag.ItemIsEditable)

    def setInfo(self, info):
        caseActive = str(info.get("caseActive", False))
        caseStart = str(info.get("caseStart", None))
        self._caseActive.setText(1, caseActive)
        self._caseStart.setText(1, caseStart)

    def getInfo(self, info):
        caseActive = self._caseActive.text(1)
        caseActive = CommonUtils.strToBool(caseActive, False)
        caseStart = self._caseStart.text(1)
        caseStart = caseStart if CommonUtils.checkUuid(caseStart) else None
        info.update({
            "caseActive": caseActive,
            "caseStart": caseStart,
        })

    def updateItem(self):
        pass


class AttrActionHeader(QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        self.setText(0, "测试动作")
        self.setFirstColumnSpanned(True)

        self._actionClass = QTreeWidgetItem(self)
        self._actionClass.setText(0, "分类")
        self._actionClass.setText(1, "")
        self._actionClass.setData(1, AttrDef.ItemAbcRole, AttrDef.ActionClassItem)
        self._actionDelay = QTreeWidgetItem(self)
        self._actionDelay.setText(0, "延迟")
        self._actionDelay.setText(1, "1000")
        self._actionDelay.setData(1, AttrDef.ItemAbcRole, AttrDef.ActionDelayItem)
        self._actionDelay.setFlags(self._actionDelay.flags() | Qt.ItemFlag.ItemIsEditable)
        self._actionTimes = QTreeWidgetItem(self)
        self._actionTimes.setText(0, "次数")
        self._actionTimes.setText(1, "1")
        self._actionTimes.setData(1, AttrDef.ItemAbcRole, AttrDef.ActionTimesItem)
        self._actionTimes.setFlags(self._actionTimes.flags() | Qt.ItemFlag.ItemIsEditable)
        self._actionRetry = QTreeWidgetItem(self)
        self._actionRetry.setText(0, "重试")
        self._actionRetry.setText(1, "0")
        self._actionRetry.setData(1, AttrDef.ItemAbcRole, AttrDef.ActionRetryItem)
        self._actionRetry.setFlags(self._actionRetry.flags() | Qt.ItemFlag.ItemIsEditable)
        self._actionChild = QTreeWidgetItem(self)
        self._actionChild.setText(0, "后继")
        self._actionChild.setText(1, "UUID")
        self._actionChild.setData(1, AttrDef.ItemAbcRole, AttrDef.ActionChildItem)
        self._actionChild.setFlags(self._actionChild.flags() | Qt.ItemFlag.ItemIsEditable)

    def setInfo(self, info):
        actionClass = info.get("actionClass", "")
        actionDelay = str(info.get("actionDelay", 0))
        actionTimes = str(info.get("actionTimes", 0))
        actionRetry = str(info.get("actionRetry", 0))
        actionChild = str(info.get("actionChild", None))
        self._actionClass.setText(1, actionClass)
        self._actionDelay.setText(1, actionDelay)
        self._actionTimes.setText(1, actionTimes)
        self._actionRetry.setText(1, actionRetry)
        self._actionChild.setText(1, actionChild)

    def getInfo(self, info):
        actionClass = str(self._actionClass.text(1))
        actionDelay = int(self._actionDelay.text(1))
        actionTimes = int(self._actionTimes.text(1))
        actionRetry = int(self._actionRetry.text(1))
        actionChild = str(self._actionChild.text(1))
        actionChild = actionChild if CommonUtils.checkUuid(actionChild) else None
        info.update({
            "actionClass": actionClass,
            "actionDelay": actionDelay,
            "actionTimes": actionTimes,
            "actionRetry": actionRetry,
            "actionChild": actionChild,
        })

    def updateItem(self):
        pass


class AttrEmptyConfig(QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        self.setText(0, "空配置")
        self.setFirstColumnSpanned(True)

        item = QTreeWidgetItem(self)
        item.setFirstColumnSpanned(True)
        item.setText(0, "无配置项")

    def setInfo(self, info):
        pass

    def getInfo(self, info):
        pass

    def updateItem(self):
        pass


class AttrCheckConfig(QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        self.setText(0, "检查配置")
        self.setFirstColumnSpanned(True)

        self._isShowSampleItem = False

        checkRect = QTreeWidgetItem(self)
        checkRect.setText(0, "检查范围")
        checkRect.setFirstColumnSpanned(True)
        self._checkRectTop = QTreeWidgetItem(checkRect)
        self._checkRectTop.setText(0, "顶边界")
        self._checkRectTop.setText(1, "uuid:UUID.topLeft")
        self._checkRectTop.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckRectTopItem)
        self._checkRectTop.setFlags(self._checkRectTop.flags() | Qt.ItemFlag.ItemIsEditable)
        self._checkOffsetTop = QTreeWidgetItem(checkRect)
        self._checkOffsetTop.setText(0, "顶边界偏移")
        self._checkOffsetTop.setText(1, "0")
        self._checkOffsetTop.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckOffsetTopItem)
        self._checkOffsetTop.setFlags(self._checkOffsetTop.flags() | Qt.ItemFlag.ItemIsEditable)
        self._checkRectLeft = QTreeWidgetItem(checkRect)
        self._checkRectLeft.setText(0, "左边界")
        self._checkRectLeft.setText(1, "last::topCenter")
        self._checkRectLeft.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckRectLeftItem)
        self._checkRectLeft.setFlags(self._checkRectLeft.flags() | Qt.ItemFlag.ItemIsEditable)
        self._checkOffsetLeft = QTreeWidgetItem(checkRect)
        self._checkOffsetLeft.setText(0, "左边界偏移")
        self._checkOffsetLeft.setText(1, "0")
        self._checkOffsetLeft.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckOffsetLeftItem)
        self._checkOffsetLeft.setFlags(self._checkOffsetLeft.flags() | Qt.ItemFlag.ItemIsEditable)
        self._checkRectRight = QTreeWidgetItem(checkRect)
        self._checkRectRight.setText(0, "右边界")
        self._checkRectRight.setText(1, "user:(10,10)")
        self._checkRectRight.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckRectRightItem)
        self._checkRectRight.setFlags(self._checkRectRight.flags() | Qt.ItemFlag.ItemIsEditable)
        self._checkOffsetRight = QTreeWidgetItem(checkRect)
        self._checkOffsetRight.setText(0, "右边界偏移")
        self._checkOffsetRight.setText(1, "0")
        self._checkOffsetRight.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckOffsetRightItem)
        self._checkOffsetRight.setFlags(self._checkOffsetRight.flags() | Qt.ItemFlag.ItemIsEditable)
        self._checkRectBottom = QTreeWidgetItem(checkRect)
        self._checkRectBottom.setText(0, "底边界")
        self._checkRectBottom.setText(1, "None")
        self._checkRectBottom.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckRectBottomItem)
        self._checkRectBottom.setFlags(self._checkRectBottom.flags() | Qt.ItemFlag.ItemIsEditable)
        self._checkOffsetBottom = QTreeWidgetItem(checkRect)
        self._checkOffsetBottom.setText(0, "底边界偏移")
        self._checkOffsetBottom.setText(1, "0")
        self._checkOffsetBottom.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckOffsetBottomItem)
        self._checkOffsetBottom.setFlags(self._checkOffsetBottom.flags() | Qt.ItemFlag.ItemIsEditable)

        self._checkSource = QTreeWidgetItem(self)
        self._checkSource.setText(0, "检查来源")
        self._checkSource.setText(1, "shot:none")
        self._checkSource.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckSourceItem)
        self._checkSource.setFlags(self._checkSource.flags() | Qt.ItemFlag.ItemIsEditable)

        self._checkTargets = QTreeWidgetItem(self)
        self._checkTargets.setText(0, "检查目标")
        self._checkTargets.setFirstColumnSpanned(True)
        self._checkTargets.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckTargetsItem)
        self._checkTargets.setFlags(self._checkTargets.flags() | Qt.ItemFlag.ItemIsEditable)

        self._sampleItem = QTreeWidgetItem(self)
        self._sampleItem.setText(0, "采样设置")
        self._sampleItem.setFirstColumnSpanned(True)
        self._checkCount = QTreeWidgetItem(self._sampleItem)
        self._checkCount.setText(0, "采样次数")
        self._checkCount.setText(1, "10")
        self._checkCount.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckCountItem)
        self._checkCount.setFlags(self._checkCount.flags() | Qt.ItemFlag.ItemIsEditable)
        self._checkHit = QTreeWidgetItem(self._sampleItem)
        self._checkHit.setText(0, "命中次数")
        self._checkHit.setText(1, "10")
        self._checkHit.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckHitItem)
        self._checkHit.setFlags(self._checkHit.flags() | Qt.ItemFlag.ItemIsEditable)
        self._checkDuration = QTreeWidgetItem(self._sampleItem)
        self._checkDuration.setText(0, "采样时长")
        self._checkDuration.setText(1, "5000")
        self._checkDuration.setData(1, AttrDef.ItemAbcRole, AttrDef.CheckDurationItem)
        self._checkDuration.setFlags(self._checkDuration.flags() | Qt.ItemFlag.ItemIsEditable)

    def setInfo(self, info):
        actionClass = str(info.get("actionClass", ""))
        checkRectTop = str(info.get("checkRectTop", None))
        checkRectLeft = str(info.get("checkRectLeft", None))
        checkRectRight = str(info.get("checkRectRight", None))
        checkRectBottom = str(info.get("checkRectBottom", None))
        checkOffsetTop = str(info.get("checkOffsetTop", 0))
        checkOffsetLeft = str(info.get("checkOffsetLeft", 0))
        checkOffsetRight = str(info.get("checkOffsetRight", 0))
        checkOffsetBottom = str(info.get("checkOffsetBottom", 0))
        checkSource = info.get("checkSource", "")
        checkHit = str(info.get("checkHit", 0))
        checkCount = str(info.get("checkCount", 0))
        checkDuration = str(info.get("checkDuration", 0))
        self._checkRectTop.setText(1, checkRectTop)
        self._checkRectLeft.setText(1, checkRectLeft)
        self._checkRectRight.setText(1, checkRectRight)
        self._checkRectBottom.setText(1, checkRectBottom)
        self._checkOffsetTop.setText(1, checkOffsetTop)
        self._checkOffsetLeft.setText(1, checkOffsetLeft)
        self._checkOffsetRight.setText(1, checkOffsetRight)
        self._checkOffsetBottom.setText(1, checkOffsetBottom)
        self._checkSource.setText(1, checkSource)
        self._checkTargets.setText(1, "暂无目标")
        self._checkHit.setText(1, checkHit)
        self._checkCount.setText(1, checkCount)
        self._checkDuration.setText(1, checkDuration)

        self._isShowSampleItem = (actionClass == "images")

    def getInfo(self, info):
        checkRectTop = self._checkRectTop.text(1)
        checkRectTop = checkRectTop if checkRectTop.lower() != "none" else None
        checkRectLeft = self._checkRectLeft.text(1)
        checkRectLeft = checkRectLeft if checkRectLeft.lower() != "none" else None
        checkRectRight = self._checkRectRight.text(1)
        checkRectRight = checkRectRight if checkRectRight.lower() != "none" else None
        checkRectBottom = self._checkRectBottom.text(1)
        checkRectBottom = checkRectBottom if checkRectBottom.lower() != "none" else None
        checkOffsetTop = self._checkOffsetTop.text(1)
        checkOffsetTop = int(checkOffsetTop)
        checkOffsetLeft = self._checkOffsetLeft.text(1)
        checkOffsetLeft = int(checkOffsetLeft)
        checkOffsetRight = self._checkOffsetRight.text(1)
        checkOffsetRight = int(checkOffsetRight)
        checkOffsetBottom = self._checkOffsetBottom.text(1)
        checkOffsetBottom = int(checkOffsetBottom)
        checkSource = self._checkSource.text(1)
        checkTargets = self._collectTarget()
        checkHit = self._checkHit.text(1)
        checkHit = int(checkHit)
        checkCount = self._checkCount.text(1)
        checkCount = int(checkCount)
        checkDuration = self._checkDuration.text(1)
        checkDuration = int(checkDuration)
        info.update({
            "checkRectTop": checkRectTop,
            "checkRectLeft": checkRectLeft,
            "checkRectRight": checkRectRight,
            "checkRectBottom": checkRectBottom,
            "checkOffsetTop": checkOffsetTop,
            "checkOffsetLeft": checkOffsetLeft,
            "checkOffsetRight": checkOffsetRight,
            "checkOffsetBottom": checkOffsetBottom,
            "checkSource": checkSource,
            "checkTargets": checkTargets,
            "checkHit": checkHit,
            "checkCount": checkCount,
            "checkDuration": checkDuration,
        })

    def updateItem(self):
        self._sampleItem.setHidden(not self._isShowSampleItem)

    def _collectTarget(self):
        result = list()
        for index in range(self._checkTargets.childCount()):
            child = self._checkTargets.child(index)
            result.append(child.text(1))
        return result


class AttrOperateConfig(QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        self.setText(0, "操作配置")
        self.setFirstColumnSpanned(True)

        self._isShowTime = False
        self._isShowKeys = False
        self._isShowRoll = False
        self._isShowContent = False

        self._operatePoint = QTreeWidgetItem(self)
        self._operatePoint.setText(0, "操作坐标")
        self._operatePoint.setText(1, "last:center")
        self._operatePoint.setData(1, AttrDef.ItemAbcRole, AttrDef.OperatePointItem)
        self._operatePoint.setFlags(self._operatePoint.flags() | Qt.ItemFlag.ItemIsEditable)
        self._operateOffsetX = QTreeWidgetItem(self)
        self._operateOffsetX.setText(0, "操作坐标偏移X")
        self._operateOffsetX.setText(1, "0")
        self._operateOffsetX.setData(1, AttrDef.ItemAbcRole, AttrDef.OperateOffsetXItem)
        self._operateOffsetX.setFlags(self._operateOffsetX.flags() | Qt.ItemFlag.ItemIsEditable)
        self._operateOffsetY = QTreeWidgetItem(self)
        self._operateOffsetY.setText(0, "操作坐标偏移X")
        self._operateOffsetY.setText(1, "0")
        self._operateOffsetY.setData(1, AttrDef.ItemAbcRole, AttrDef.OperateOffsetYItem)
        self._operateOffsetY.setFlags(self._operateOffsetY.flags() | Qt.ItemFlag.ItemIsEditable)
        self._operateTime = QTreeWidgetItem(self)
        self._operateTime.setText(0, "行为时间")
        self._operateTime.setText(1, "0 ms")
        self._operateTime.setData(1, AttrDef.ItemAbcRole, AttrDef.OperateTimeItem)
        self._operateTime.setFlags(self._operateTime.flags() | Qt.ItemFlag.ItemIsEditable)
        self._operateKeys = QTreeWidgetItem(self)
        self._operateKeys.setText(0, "按键")
        self._operateKeys.setText(1, "[]")
        self._operateKeys.setData(1, AttrDef.ItemAbcRole, AttrDef.OperateKeysItem)
        self._operateKeys.setFlags(self._operateKeys.flags() | Qt.ItemFlag.ItemIsEditable)
        self._operateRoll = QTreeWidgetItem(self)
        self._operateRoll.setText(0, "滚动值")
        self._operateRoll.setText(1, "0")
        self._operateRoll.setData(1, AttrDef.ItemAbcRole, AttrDef.OperateRollItem)
        self._operateRoll.setFlags(self._operateRoll.flags() | Qt.ItemFlag.ItemIsEditable)
        self._operateContent = QTreeWidgetItem(self)
        self._operateContent.setText(0, "输入内容")
        self._operateContent.setText(1, "")
        self._operateContent.setData(1, AttrDef.ItemAbcRole, AttrDef.OperateContentItem)
        self._operateContent.setFlags(self._operateContent.flags() | Qt.ItemFlag.ItemIsEditable)

    def setInfo(self, info):
        actionClass = info.get("actionClass", "")
        operatePoint = info.get("operatePoint", "")
        operateOffsetX = str(info.get("operateOffsetX", 0))
        operateOffsetY = str(info.get("operateOffsetY", 0))
        operateTime = str(info.get("operateTime", 0))
        operateKeys = info.get("operateKeys", [])
        operateKeys = str(", ").join(operateKeys)
        operateRoll = str(info.get("operateRoll", 0))
        operateContent = info.get("operateContent", "")

        self._operatePoint.setText(1, operatePoint)
        self._operateOffsetX.setText(1, operateOffsetX)
        self._operateOffsetY.setText(1, operateOffsetY)
        self._operateTime.setText(1, operateTime)
        self._operateKeys.setText(1, operateKeys)
        self._operateRoll.setText(1, operateRoll)
        self._operateContent.setText(1, operateContent)

        self._isShowTime = False
        self._isShowKeys = False
        self._isShowRoll = False
        self._isShowContent = False
        if actionClass == "leftClick":
            self._isShowTime = False
        elif actionClass == "rightClick":
            self._isShowTime = False
        elif actionClass == "move":
            self._isShowTime = False
        elif actionClass == "drag":
            self._isShowTime = False
        elif actionClass == "wheel":
            self._isShowRoll = True
        elif actionClass == "key":
            self._isShowKeys = True
        elif actionClass == "keys":
            self._isShowKeys = True
        elif actionClass == "copyPaste":
            self._isShowContent = True

    def getInfo(self, info):
        operatePoint = self._operatePoint.text(1)
        operateOffsetX = self._operateOffsetX.text(1)
        operateOffsetX = int(operateOffsetX)
        operateOffsetY = self._operateOffsetY.text(1)
        operateOffsetY = int(operateOffsetY)
        operateTime = self._operateTime.text(1)
        operateTime = int(operateTime)
        operateKeys = self._operateKeys.text(1)
        operateKeys = self._splitKeys()
        operateRoll = self._operateRoll.text(1)
        operateRoll = int(operateRoll)
        operateContent = self._operateContent.text(1)
        info.update({
            "operatePoint": operatePoint,
            "operateOffsetX": operateOffsetX,
            "operateOffsetY": operateOffsetY,
            "operateTime": operateTime,
            "operateKeys": operateKeys,
            "operateRoll": operateRoll,
            "operateContent": operateContent,
        })

    def updateItem(self):
        self._operateTime.setHidden(not self._isShowTime)
        self._operateKeys.setHidden(not self._isShowKeys)
        self._operateRoll.setHidden(not self._isShowRoll)
        self._operateContent.setHidden(not self._isShowContent)

    def _splitKeys(self):
        result = list()
        text = self._operateKeys.text(1)
        text = text.replace(" ", "")
        for key in text.split(","):
            if len(key):
                result.append(key)
        return result


class AttrControlConfig(QTreeWidgetItem):
    def __init__(self):
        super().__init__()
        self.setText(0, "控制配置")
        self.setFirstColumnSpanned(True)

        self._isShowFork = False
        self._isShowInput = False
        self._isShowScript = False

        self._controlForkGoto = QTreeWidgetItem(self)
        self._controlForkGoto.setText(0, "跳转到")
        self._controlForkGoto.setText(1, "None")
        self._controlForkGoto.setData(1, AttrDef.ItemAbcRole, AttrDef.ControlForkGotoItem)
        self._controlForkGoto.setFlags(self._controlForkGoto.flags() | Qt.ItemFlag.ItemIsEditable)
        self._controlForkEval = QTreeWidgetItem(self)
        self._controlForkEval.setText(0, "表达式")
        self._controlForkEval.setText(1, "")
        self._controlForkEval.setData(1, AttrDef.ItemAbcRole, AttrDef.ControlForkEvalItem)
        self._controlForkEval.setFlags(self._controlForkEval.flags() | Qt.ItemFlag.ItemIsEditable)
        self._controlInputTips = QTreeWidgetItem(self)
        self._controlInputTips.setText(0, "输入提示")
        self._controlInputTips.setText(1, "请输入")
        self._controlInputTips.setData(1, AttrDef.ItemAbcRole, AttrDef.ControlInputTipsItem)
        self._controlInputTips.setFlags(self._controlInputTips.flags() | Qt.ItemFlag.ItemIsEditable)
        self._controlInputForm = QTreeWidgetItem(self)
        self._controlInputForm.setText(0, "输入方式")
        self._controlInputForm.setText(1, "")
        self._controlInputForm.setData(1, AttrDef.ItemAbcRole, AttrDef.ControlInputFormItem)
        self._controlInputForm.setFlags(self._controlInputForm.flags() | Qt.ItemFlag.ItemIsEditable)
        self._controlScriptPath = QTreeWidgetItem(self)
        self._controlScriptPath.setText(0, "脚本路径")
        self._controlScriptPath.setText(1, "None")
        self._controlScriptPath.setData(1, AttrDef.ItemAbcRole, AttrDef.ControlScriptPathItem)
        self._controlScriptPath.setFlags(self._controlScriptPath.flags() | Qt.ItemFlag.ItemIsEditable)
        self._controlScriptArgs = QTreeWidgetItem(self)
        self._controlScriptArgs.setText(0, "脚本参数")
        self._controlScriptArgs.setText(1, "")
        self._controlScriptArgs.setData(1, AttrDef.ItemAbcRole, AttrDef.ControlScriptArgsItem)
        self._controlScriptArgs.setFlags(self._controlScriptArgs.flags() | Qt.ItemFlag.ItemIsEditable)

    def setInfo(self, info):
        actionClass = info.get("actionClass", "")
        controlForkGoto = str(info.get("controlForkGoto", None))
        controlForkEval = info.get("controlForkEval", "")
        controlInputTips = info.get("controlInputTips", "")
        controlInputForm = info.get("controlInputForm", "")
        controlScriptPath = info.get("controlScriptPath", "")
        controlScriptArgs = info.get("controlScriptArgs", "")
        self._controlForkGoto.setText(1, controlForkGoto)
        self._controlForkEval.setText(1, controlForkEval)
        self._controlInputTips.setText(1, controlInputTips)
        self._controlInputForm.setText(1, controlInputForm)
        self._controlScriptPath.setText(1, controlScriptPath)
        self._controlScriptArgs.setText(1, controlScriptArgs)

        if actionClass == "fork":
            self._isShowFork = True
        elif actionClass == "input":
            self._isShowInput = True
        elif actionClass == "script":
            self._isShowScript = True

    def getInfo(self, info):
        controlForkGoto = self._controlForkGoto.text(1)
        controlForkGoto = controlForkGoto if CommonUtils.checkUuid(controlForkGoto) else None
        controlForkEval = self._controlForkEval.text(1)
        controlInputTips = self._controlInputTips.text(1)
        controlInputForm = self._controlInputForm.text(1)
        controlScriptPath = self._controlScriptPath.text(1)
        controlScriptArgs = self._controlScriptArgs.text(1)
        info.update({
            "controlForkGoto": controlForkGoto,
            "controlForkEval": controlForkEval,
            "controlInputTips": controlInputTips,
            "controlInputForm": controlInputForm,
            "controlScriptPath": controlScriptPath,
            "controlScriptArgs": controlScriptArgs,
        })

    def updateItem(self):
        self._controlForkGoto.setHidden(not self._isShowFork)
        self._controlForkEval.setHidden(not self._isShowFork)
        self._controlInputTips.setHidden(not self._isShowInput)
        self._controlInputForm.setHidden(not self._isShowInput)
        self._controlScriptPath.setHidden(not self._isShowScript)
        self._controlScriptArgs.setHidden(not self._isShowScript)


