# -*- coding:utf-8 -*-

from PySide6.QtCore import Qt

ItemAbcRole = Qt.ItemDataRole.UserRole + 1

BaseTypeItem = 0
BaseIdenItem = 1
BaseNameItem = 3
BaseDescItem = 4

CaseStartItem = 10
CaseActiveItem = 11

ActionClassItem = 20
ActionDelayItem = 21
ActionTimesItem = 22
ActionRetryItem = 23
ActionChildItem = 24

CheckRectTopItem = 100
CheckRectLeftItem = 101
CheckRectRightItem = 102
CheckRectBottomItem = 103
CheckOffsetTopItem = 104
CheckOffsetLeftItem = 105
CheckOffsetRightItem = 106
CheckOffsetBottomItem = 107
CheckSourceItem = 108
CheckTargetsItem = 109
CheckHitItem = 110
CheckCountItem = 111
CheckDurationItem = 112

OperatePointItem = 200
OperateOffsetXItem = 201
OperateOffsetYItem = 202
OperateTimeItem = 203
OperateKeysItem = 204
OperateRollItem = 205
OperateContentItem = 206

ControlForkGotoItem = 300
ControlForkEvalItem = 301
ControlInputTipsItem = 302
ControlInputFormItem = 303
ControlScriptPathItem = 304
ControlScriptArgsItem = 305
