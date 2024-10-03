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

            if not only:
                for item in data.get('cases', list()):
                    if case := TestFactory.parseCase(item, False):
                        result.addCaseItem(case)

            return result

    @staticmethod
    def formatGroup(group: TestGroup, only=True):
        cases = list()
        if not only:
            for item in group.getCaseList():
                cases.append(TestFactory.formatCase(item, only))

        return {
            'type': group.getType(),
            'name': group.getName(),
            'iden': group.getIden(),
            'desc': group.getDesc(),
            'cases': cases,
        }

    @staticmethod
    def parseCase(data: dict, only=False):
        if data['type'] == TestCase.getType():
            result = TestCase()
            result.setName(data['name'])
            result.setIden(data['iden'])
            result.setDesc(data['desc'])
            result.setStart(data['start'])
            result.setActive(data['active'])

            if not only:
                for item in data.get('actions', list()):
                    if action := TestFactory.parseAction(item):
                        result.addActionItem(action)
                if not result.checkActionList():
                    return None

            return result

    @staticmethod
    def formatCase(case: TestCase, only=True):
        actions = list()
        if not only:
            for item in case.getActionList():
                actions.append(TestFactory.formatAction(item, only))

        return {
            'type': case.getType(),
            'name': case.getName(),
            'iden': case.getIden(),
            'desc': case.getDesc(),
            'start': case.getStart(),
            'active': case.getActive(),
            'actions': actions,
        }

    @staticmethod
    def parseAction(data: dict):
        if result := _createTestAction(data):
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
        return {
            'type': action.getType(),
            'name': action.getName(),
            'iden': action.getIden(),
            'desc': action.getDesc(),
            'class': action.getClass(),
            'delay': action.getDelay(),
            'retry': action.getRetry(),
            'child': action.getChild(),
            'config': action.getConfig(),
        }


def _readFile(path):
    try:
        with open(path, "rb") as fp:
            return json.load(fp)
    except Exception as e:
        return e


def _createTestAction(data: dict):
    result = None
    if data['type'] == TestActionCheck.getType():
        result = TestActionCheck()
    elif data['type'] == TestActionOperate.getType():
        result = TestActionOperate()
    elif data['type'] == TestActionControl.getType():
        result = TestActionControl()
    elif data['type'] == TestActionEmpty.getType():
        result = TestActionEmpty()
    return result










