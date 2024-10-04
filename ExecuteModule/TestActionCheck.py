import copy
import pyautogui
import pyscreeze
from ExecuteModule.TestRect import TestRect
from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestResult import TestResult
from ExecuteModule.TestRuntime import TestRuntime
from ExecuteModule.TestInterpret import TestInterpret

_defaultRect = {'top': None, 'left': None, 'right': None, 'bottom': None}
_defaultOffset = {'top': 0, 'left': 0, 'right': 0, 'bottom': 0}
_defaultSource = 'shot:none'
_defaultTargets = []

_defaultHit = 3
_defaultCount = 15
_defaultDuration = 3000


class TestActionCheck(TestAction):
    _type = "check"

    def __init__(self):
        super().__init__()
        self.setName("TestCheck")
        self.setDesc("This TestCheck")
        self._configRect = _defaultRect
        self._configOffset = _defaultOffset
        self._configSource = _defaultSource
        self._configTargets = _defaultTargets
        self._configDuration = _defaultDuration
        self._configCount = _defaultCount
        self._configHit = _defaultHit

    def exec(self):
        if self.getClass() == 'text':
            return self._textCheck()
        elif self.getClass() == 'image':
            return self._imageCheck()
        elif self.getClass() == 'texts':
            return self._textsCheck()
        elif self.getClass() == 'images':
            return self._imagesCheck()

        return TestResult(TestResult.CriticalFlag, "没有找到匹配的class")

    def setConfig(self, data):
        self._configRect = _returnConfigsValue('rect', data)
        self._configOffset = _returnConfigsValue('offset', data)
        self._configSource = _returnConfigsValue('source', data)
        self._configTargets = _returnConfigsValue('targets', data)
        self._configHit = _returnConfigsValue('hit', data)
        self._configCount = _returnConfigsValue('count', data)
        self._configDuration = _returnConfigsValue('duration', data)

    def getConfig(self):
        return {
            "rect": self._configRect,
            "offset": self._configOffset,
            "source": self._configSource,
            "targets": self._configTargets,
            "hit": self._configHit,
            "time": self._configDuration,
            "count": self._configCount,
        }

    def _textCheck(self):
        self.getChild()
        return TestResult(TestResult.CriticalFlag)

    def _imageCheck(self):

        # 1截取图片
        # 2裁剪图片
        # 3搜索子图
        # 4转换绝对坐标

        img1 = pyscreeze.screenshot()

        rect1 = TestRect(0, 0, img1.width, img1.height)
        rect2 = _qiege(rect1, self._configRect, self._configOffset)
        img2 = img1.crop((rect2.getXpos(), rect2.getYpos(), rect2.getXpos(), rect2.getYpos()))
        miss = rect1.miss(rect2)

        # pyscreeze.locateAll("target", "screen")
        # rects = _searchImages(img2, self._configTargets)

        # rects = _toAbsRects(rects)

        result = TestResult(TestResult.RunningFlag, "")
        result.setNext(self.getChild())
        # result.set
        return result

    def _textsCheck(self):
        result = TestResult(TestResult.CriticalFlag, "")
        result.setNext(self.getChild())
        return result

    def _imagesCheck(self):
        result = TestResult(TestResult.CriticalFlag, "")
        result.setNext(self.getChild())
        return result


def _returnConfigsValue(key: str, data: dict):
    ret = None
    if key == 'rect':
        ret = _defaultRect
        val = data.get(key, ret)
        if isinstance(val, dict):
            ret = val
    elif key == 'offset':
        ret = _defaultOffset
        val = data.get(key, ret)
        if isinstance(val, dict):
            ret = val
    elif key == 'source':
        ret = _defaultSource
        val = data.get(key, ret)
        if isinstance(val, str):
            ret = val
    elif key == 'targets':
        ret = _defaultTargets
        val = data.get(key, ret)
        if isinstance(val, list):
            ret = val
    elif key == 'hit':
        ret = _defaultHit
        val = data.get(key, ret)
        if isinstance(val, int) and 0 < val:
            ret = val
    elif key == 'count':
        ret = _defaultCount
        val = data.get(key, ret)
        if isinstance(val, int) and 0 < val:
            ret = val
    elif key == 'duration':
        ret = _defaultDuration
        val = data.get(key, ret)
        if isinstance(val, int) and 0 < val:
            ret = val

    return ret


def _qiege(rect, limit, offset):
    result = copy.copy(rect)

    if limit["top"]:
        if topPoint := TestInterpret.fn1(limit["top"]):
            result.limitTopLine(topPoint)
    if limit["left"]:
        if leftPoint := TestInterpret.fn1(limit["left"]):
            result.limitLeftLine(leftPoint)
    if limit["right"]:
        if rightPoint := TestInterpret.fn1(limit["right"]):
            result.limitRightLine(rightPoint)
    if limit["bottom"]:
        if bottomPoint := TestInterpret.fn1(limit["bottom"]):
            result.limitBottomLine(bottomPoint)

    return result








