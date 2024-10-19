import json
from ExecuteModule.TestGroup import TestGroup
from ExecuteModule.TestCase import TestCase
from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestActionCheck import TestActionCheck
from ExecuteModule.TestActionControl import TestActionControl
from ExecuteModule.TestActionOperate import TestActionOperate
from ExecuteModule.TestActionEmpty import TestActionEmpty
from UtilsModule.CommonUtils import CommonUtils


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
        data: dict = TestFactory.formatGroup(data, False)
        return _writeFile(path, data)

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
    def updateGroup(group: TestGroup, data):
        count = 2
        if "name" in data:
            val = data["name"]
            if group.setName(val):
                count -= 1
        if "desc" in data:
            val = data["desc"]
            if group.setDesc(val):
                count -= 1
        return not bool(count)

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
    def updateCase(case: TestCase, data):
        count = 4
        if "name" in data:
            val = data["name"]
            if case.setName(val):
                count -= 1
        if "desc" in data:
            val = data["desc"]
            if case.setDesc(val):
                count -= 1
        if "start" in data:
            val = data["start"]
            if case.setStart(val):
                count -= 1
        if "active" in data:
            val = data["active"]
            if case.setActive(val):
                count -= 1
        return not bool(count)

    @staticmethod
    def parseAction(data: dict):
        if result := _createTestAction(data):
            result.setName(data['name'])
            result.setIden(data['iden'])
            result.setDesc(data['desc'])
            result.setClass(data['class'])
            result.setDelay(data['delay'])
            result.setTimes(data['times'])
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
            'times': action.getTimes(),
            'retry': action.getRetry(),
            'child': action.getChild(),
            'config': action.getConfig(),
        }

    @staticmethod
    def updateAction(action: TestAction, data):
        count = 8
        if "name" in data:
            val = data["name"]
            if action.setName(val):
                count -= 1
        if "desc" in data:
            val = data["desc"]
            if action.setDesc(val):
                count -= 1
        if "class" in data:
            val = data['class']
            if action.setClass(val):
                count -= 1
        if "delay" in data:
            val = data['delay']
            if action.setDelay(val):
                count -= 1
        if "times" in data:
            val = data['times']
            if action.setTimes(val):
                count -= 1
        if "retry" in data:
            val = data["retry"]
            if action.setRetry(val):
                count -= 1
        if "child" in data:
            val = data["child"]
            if action.setChild(val):
                count -= 1
        if "config" in data:
            val = data['config']
            if action.setConfig(val):
                count -= 1
        return not bool(count)


def _readFile(path):
    try:
        with open(path, "rb") as fp:
            return json.load(fp)
    except Exception as e:
        print(path)
        return e


def _writeFile(path, data):
    try:
        with open(path, "w", encoding="utf8") as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)
            return True
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










