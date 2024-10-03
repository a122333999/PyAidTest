from ExecuteModule.TestRuntime import TestRuntime
from ExecuteModule.TestResult import TestResult
from ExecuteModule.TestRect import TestRect


class TestInterpret:

    @staticmethod
    def fn1(content: str):
        idx = 0
        if "last:" in content:
            if ret := TestRuntime.currentResult:
                return _fn100(content, ret, idx, (0, 0))

        elif "uuid:" in content:
            uuid = "None"
            if ret := TestRuntime.historyResult.get(uuid, None):
                return _fn100(content, ret, idx, (0, 0))

        elif "user:" in content:
            return _fn200(content[5:])

        return None


def _fn100(content: str, ret: TestResult, idx=0, offset=(0, 0)):
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


def _fn200(data: str):
    return 0, 0
