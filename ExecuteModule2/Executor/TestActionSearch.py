# -*- coding:utf-8 -*-

import ExecuteModule2.Executor.TestAction as TestAction
from UtilsModule.CommonUtils import CommonUtils


class TestActionSearch(TestAction.TestAction):

    typeValue = 'search'
    classValues = ['text', 'image', 'texts', 'images']  
    
    def __init__(self):
        super().__init__()

    def exec(self) :
        print("TestActionSearch exec")

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
        if not isinstance(config['rect'], dict):
            return False
        if not isinstance(config['rect']['top'], str) and config['rect']['top'] is not None:
            return False
        if not isinstance(config['rect']['left'], str) and config['rect']['left'] is not None:
            return False
        if not isinstance(config['rect']['right'], str) and config['rect']['right'] is not None:
            return False
        if not isinstance(config['rect']['bottom'], str) and config['rect']['bottom'] is not None:
            return False
        if not isinstance(config['offset'], dict):
            return False
        if not isinstance(config['offset']['top'], int):
            return False
        if not isinstance(config['offset']['left'], int):
            return False
        if not isinstance(config['offset']['right'], int):
            return False
        if not isinstance(config['offset']['bottom'], int):
            return False
        if not isinstance(config['targets'], list):
            return False
        for target in config['targets']:
            if not isinstance(target, str):
                return False
        if not isinstance(config['hit'], int) or config['hit'] < 0:
            return False
        if not isinstance(config['count'], int) or config['count'] < 0:
            return False
        if not isinstance(config['duration'], int) or config['duration'] < 0:
            return False

        return True

    @classmethod
    def copyData(cls, testAction: dict, onlyHeader=True):
        pass

    @classmethod
    def updateData(cls, testAction: dict, info: dict):
        pass

TestAction.searchActionClass = TestActionSearch