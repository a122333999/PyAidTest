from ExecuteModule.TestRuntime import TestRuntime
from ExecuteModule.TestResult import TestResult
from ExecuteModule.TestRect import TestRect
from UtilsModule.CommonUtils import CommonUtils


class TestInterpret:

    @classmethod
    def fn1(cls, content: str, offset: dict | tuple = (0, 0)):
        idx, offset = 0, _transOffset(offset)
        if "last:" in content:
            if ret := TestRuntime.currentResult:
                return cls._fn100(content, ret, idx, offset)

        elif "uuid:" in content:
            if ret := TestRuntime.historyResult.get(_extractUuid(content[5:]), None):
                return cls._fn100(content, ret, idx, offset)

        elif "user:" in content:
            if ret := _extractPoint(content[5:]):
                return ret[0]+offset[0], ret[1]+offset[1]

        return None

    @classmethod
    def fn2(cls, content: str):
        if "user:" in content:
            return content[5:]
        elif "buff:" in content:
            if ret := TestRuntime.buffInfo:
                if "clear:" in content:
                    TestRuntime.buffInfo = None
                return ret
        return None

    @classmethod
    def _fn100(cls, content: str, ret: TestResult, idx=0, offset=(0, 0)):
        if idx < ret.getRectSize():
            rect = ret.getRectList()[idx]
            if "center" in content:
                return rect.getCenterPoint(offset)
            elif "topCenter" in content:
                return rect.getTopCenterPoint(offset)
            elif "leftCenter" in content:
                return rect.getLeftCenterPoint(offset)
            elif "rightCenter" in content:
                return rect.getRightCenterPoint(offset)
            elif "bottomCenter" in content:
                return rect.getBottomCenterPoint(offset)
            elif "topLeft" in content:
                return rect.getTopLeftPoint(offset)
            elif "topRight" in content:
                return rect.getTopRightPoint(offset)
            elif "bottomLeft" in content:
                return rect.getBottomLeftPoint(offset)
            elif "bottomRight" in content:
                return rect.getBottomRightPoint(offset)
        return None


def _transOffset(offset: dict | tuple):
    if isinstance(offset, dict):
        return offset.get("x", 0), offset.get("y", 0)
    return offset


def _extractPoint(data: str):
    try:
        ret = eval(data)
        return ret[0], ret[1]
    except IndexError:
        return None
    except SyntaxError:
        return None


def _extractUuid(data: str):
    idx = data.find(".")
    return CommonUtils.checkUuid(data[:idx])

