import json
from ExecuteModule.TestGroup import TestGroup
from ExecuteModule.TestCase import TestCase
from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestActionCheck import TestActionCheck
from ExecuteModule.TestActionControl import TestActionControl
from ExecuteModule.TestActionOperate import TestActionOperate
from ExecuteModule.TestActionEmpty import TestActionEmpty


# TODO: 验证UUID是否有效

class TestFactory:

    @staticmethod
    def importFile(path):
        data: dict = _readFile(path)
        if isinstance(data, Exception):
            raise data
        return TestFactory.parseGroup(data)

    @staticmethod
    def exportFile(path, data):
        pass

    @staticmethod
    def parseGroup(data: dict, only=False):
        if data['type'] == TestGroup.getType():
            result = TestGroup()
            result.setName(data['name'])
            result.setIden(data['iden'])
            result.setDesc(data['desc'])
            if only is False:
                cases: list = data.get('cases', list())
                for item in cases:
                    case = TestFactory.parseCase(item, False)
                    if isinstance(case, TestCase):
                        result.addCaseItem(case)

            return result

    @staticmethod
    def formatGroup(group: TestGroup, only=True):
        pass

    @staticmethod
    def parseCase(data: dict, only=False):
        if data['type'] == TestCase.getType():
            result = TestCase()
            result.setName(data['name'])
            result.setIden(data['iden'])
            result.setDesc(data['desc'])
            result.setHeader(data['header'])
            if only is False:
                actions: list = data.get('actions', list())
                for item in actions:
                    action = TestFactory.parseAction(item)
                    if isinstance(action, TestAction):
                        result.addActionItem(action)
                if result.checkActionList() is False:
                    return None
            return result

    @staticmethod
    def formatCase(case: TestCase, only=True):
        pass

    @staticmethod
    def parseAction(data: dict):
        result: TestAction | None = None
        if data['type'] == TestActionCheck.getType():
            result = TestActionCheck()
        elif data['type'] == TestActionOperate.getType():
            result = TestActionOperate()
        elif data['type'] == TestActionControl.getType():
            result = TestActionControl()
        elif data['type'] == TestActionEmpty.getType():
            result = TestActionEmpty()

        if result is not None:
            result.setName(data['name'])
            result.setIden(data['iden'])
            result.setDesc(data['desc'])
            result.setClass(data['class'])
            result.setDelay(data['delay'])
            result.setRetry(data['retry'])
            result.setChild(data['child'])
            result.setConfig(data['config'])

        return result

    @staticmethod
    def formatAction(action: TestAction, only=True):
        pass


def _readFile(path):
    try:
        with open(path, "rb") as fp:
            return json.load(fp)
    except Exception as e:
        return e
