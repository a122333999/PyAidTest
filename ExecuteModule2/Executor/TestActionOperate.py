# -*- coding:utf-8 -*-

import ExecuteModule2.Executor.TestAction as TestAction
from UtilsModule.CommonUtils import CommonUtils


class TestActionOperate(TestAction.TestAction):

    typeValue = 'operate'
    classValues = ['click', 'leftClick', 'rightClick', 'doubleClick', 'move', 'drag', 'wheel', 'key', 'hotKey', 'copyPaste']

    def __init__(self):
        super().__init__()

    def exec(self) :
        print("TestActionOperate exec")

    @classmethod
    def validJson(cls, data: dict, onlyHeader=True):
        if not isinstance(data[cls.baseTypeKey], str) or data[cls.baseTypeKey] != cls.typeValue:
            return False
        if not CommonUtils.checkUuid(data[cls.baseIdenKey]):
            return False
        if not isinstance(data[cls.baseNameKey], str):
            return False
        if not isinstance(data[cls.baseDescKey], str):
            return False
        if not isinstance(data[cls.actionClassKey], str) or data[cls.actionClassKey] not in cls.classValues:
            return False
        if not isinstance(data[cls.actionDelayKey], int) or data[cls.actionDelayKey] < 0:
            return False
        if not isinstance(data[cls.actionTimesKey], int) or data[cls.actionTimesKey] < 1:
            return False
        if not isinstance(data[cls.actionForceKey], bool):
            return False
        if not isinstance(data[cls.actionConfigKey], dict):
            return False
        
        config:dict = data[cls.actionConfigKey]
        if not isinstance(config['point'], str):
            return False
        if not isinstance(config['offset'], dict):
            return False
        if not isinstance(config['offset']['x'], int):
            return False
        if not isinstance(config['offset']['y'], int):
            return False
        if not isinstance(config['time'], int) or config['time'] < 0:
            return False
        if not isinstance(config['keys'], list):
            return False
        for key in config['keys']:
            if not isinstance(key, str):
                return False
        if not isinstance(config['roll'], int) or config['roll'] < 0:
            return False
        if not isinstance(config['copy'], str):
            return False
        return True

    @classmethod
    def copyData(cls, testAction: dict, onlyHeader=True):
        return {
            cls.baseTypeKey: testAction[cls.baseTypeKey],
            cls.baseIdenKey: testAction[cls.baseIdenKey],
            cls.baseNameKey: testAction[cls.baseNameKey],
            cls.baseDescKey: testAction[cls.baseDescKey],
            cls.actionClassKey: testAction[cls.actionClassKey],
            cls.actionDelayKey: testAction[cls.actionDelayKey],
            cls.actionTimesKey: testAction[cls.actionTimesKey],
            cls.actionForceKey: testAction[cls.actionForceKey],
            cls.actionValidKey: testAction[cls.actionValidKey],
            cls.actionConfigKey: {
                'point': testAction[cls.actionConfigKey]['point'],
                'offset': {
                    'x': testAction[cls.actionConfigKey]['offset']['x'],
                    'y': testAction[cls.actionConfigKey]['offset']['y']
                },
                'time': testAction[cls.actionConfigKey]['time'],
                'keys': list(testAction[cls.actionConfigKey]['keys']),
                'roll': testAction[cls.actionConfigKey]['roll'],
                'copy': testAction[cls.actionConfigKey]['copy']
            }
        }

    @classmethod
    def updateData(cls, testAction: dict, info: dict):
        pass


TestAction.operateActionClass = TestActionOperate
