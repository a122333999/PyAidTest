# -*- coding:utf-8 -*-

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

        return TestResult(TestResult.CriticalFlag, "执行check错误: 没有找到匹配的class")

    def setClass(self, data):
        if data in ["text", "image", "texts", "images"]:
            return super().setClass(data)
        return False

    def setConfig(self, data):
        self._configRect = _returnConfigsValue('rect', data)
        self._configOffset = _returnConfigsValue('offset', data)
        self._configSource = _returnConfigsValue('source', data)
        self._configTargets = _returnConfigsValue('targets', data)
        self._configHit = _returnConfigsValue('hit', data)
        self._configCount = _returnConfigsValue('count', data)
        self._configDuration = _returnConfigsValue('duration', data)
        return True

    def getConfig(self):
        return {
            "rect": self._configRect,
            "offset": self._configOffset,
            "source": self._configSource,
            "targets": self._configTargets,
            "hit": self._configHit,
            "count": self._configCount,
            "duration": self._configDuration,
        }

    def _textCheck(self):
        self.getChild()
        return TestResult(TestResult.CriticalFlag, "执行texts错误: 功能未实现")

    def _imageCheck(self):
        # 1截取图片 2限定图片 3搜索子图(重试次数) 4返回结果
        src = TestInterpret.fn4(self._configSource, pyscreeze.screenshot())
        box = _limitRegion(src, self._configRect, self._configOffset)
        cts = _transTargets(self._configTargets, 'img')
        rects = list()
        for index in range(self.getRetry() + 1):
            rects = _searchImages(src, cts, box.toTupleRect())
            if len(rects):
                break

        # 没找到目标可以正常返回
        result = TestResult(TestResult.RunningFlag, "执行image完成")
        result.setNext(self.getChild())
        result.setRectsList(rects)
        result.addImage(src)
        result.addImage(pyscreeze.screenshot())
        return result

    def _textsCheck(self):
        self.getChild()
        return TestResult(TestResult.CriticalFlag, "执行texts错误: 功能未实现")

    def _imagesCheck(self):
        # TODO: duration未实现
        # 1截取图片 2限定图片 3搜索子图(重试次数) 4返回结果
        src = TestInterpret.fn4(self._configSource, pyscreeze.screenshot())
        box = _limitRegion(src, self._configRect, self._configOffset)
        cts = _transTargets(self._configTargets, 'img')
        rects, hit = list(), 0
        for _ in range(self._configCount):
            for _ in range(self.getRetry() + 1):
                ret = _searchImages(src, cts, box.toTupleRect())
                if len(ret):
                    hit += 1
                    rects.extend(ret)
                    break
            if hit >= self._configHit:
                break

        result = TestResult(TestResult.RunningFlag, "执行images完成")
        result.setNext(self.getChild())
        result.addImage(src)
        result.addImage(pyscreeze.screenshot())
        if hit >= self._configHit:
            result.setRectsList(rects)
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


def _limitRegion(img, limit, offset):
    rect = TestRect(0, 0, img.width, img.height)

    if limit["top"]:
        if topPoint := TestInterpret.fn1(limit["top"], (0, offset["top"])):
            rect.limitTopLine(topPoint)
    if limit["left"]:
        if leftPoint := TestInterpret.fn1(limit["left"], (offset["left"], 0)):
            rect.limitLeftLine(leftPoint)
    if limit["right"]:
        if rightPoint := TestInterpret.fn1(limit["right"], (offset["right"], 0)):
            rect.limitRightLine(rightPoint)
    if limit["bottom"]:
        if bottomPoint := TestInterpret.fn1(limit["bottom"], (0, offset["bottom"])):
            rect.limitBottomLine(bottomPoint)

    return rect


def _transTargets(targets, only=None):
    """ only='str'时仅返回text only='img'时仅返回图片 """
    for target in targets:
        print(target)
    return ['./Docs/testimg1.png']


def _searchImages(img, targets, region):
    for target in targets:
        try:
            gen = pyscreeze.locateAll(target, img, region=region)
            rects = [TestRect(box.left, box.top, box.width, box.height) for box in gen]
            if len(rects):
                return rects
        except pyscreeze.ImageNotFoundException:
            continue

    return []







