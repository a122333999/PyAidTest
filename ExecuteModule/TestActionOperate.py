import time
import math
import pyautogui
import pyperclip

from ExecuteModule.TestAction import TestAction
from ExecuteModule.TestRect import TestRect
from ExecuteModule.TestResult import TestResult
from ExecuteModule.TestInterpret import TestInterpret


_defaultPoint = "user:(16, 16)"
_defaultOffset = {"x": 0, "y": 0}
_defaultTime = 10
_defaultKeys = ["ctrl"]
_defaultRoll = 0
_defaultContent = "buff:clear"


class TestActionOperate(TestAction):
    _type = "operate"

    def __init__(self):
        super().__init__()
        self.setName("TestOperate")
        self.setDesc("This TestOperate")
        self._configPoint = _defaultPoint
        self._configOffset = _defaultOffset
        self._configTime = _defaultTime
        self._configKeys = _defaultKeys
        self._configRoll = _defaultRoll
        self._configContent = _defaultContent

    def exec(self):
        if self.getClass() == 'click':
            return self._clickOperate()
        elif self.getClass() == 'leftClick':
            return self._leftClickOperate()
        elif self.getClass() == 'rightClick':
            return self._rightClickOperate()
        elif self.getClass() == 'doubleClick':
            return self._doubleClickOperate()
        elif self.getClass() == 'move':
            return self._moveOperate()
        elif self.getClass() == 'drag':
            return self._dragOperate()
        elif self.getClass() == 'wheel':
            return self._wheelOperate()
        elif self.getClass() == 'key':
            return self._keyOperate()
        elif self.getClass() == 'keys':
            return self._keysOperate()
        elif self.getClass() == 'copyPaste':
            return self._copyPasteOperate()

        return TestResult(TestResult.CriticalFlag, "执行operate错误: 没有找到匹配的class")

    def setClass(self, data):
        if data in ["click", "leftClick", "rightClick", "doubleClick",
                    "move", "drag", "wheel", "key", "keys", "copyPaste"]:
            return super().setClass(data)
        return False

    def setConfig(self, data):
        self._configPoint = _returnConfigsValue('point', data)
        self._configOffset = _returnConfigsValue('offset', data)
        self._configTime = _returnConfigsValue('time', data)
        self._configKeys = _returnConfigsValue('keys', data)
        self._configRoll = _returnConfigsValue('roll', data)
        self._configContent = _returnConfigsValue('content', data)
        return True

    def getConfig(self):
        return {
            "point": self._configPoint,
            "offset": self._configOffset,
            "time": self._configTime,
            "keys": self._configKeys,
            "roll": self._configRoll,
            "content": self._configContent
        }

    def _clickOperate(self):
        # 1计算出点击坐标 2移动到点击坐标 3点击
        if point := TestInterpret.fn1(self._configPoint, self._configOffset):
            curr = pyautogui.position()
            duration = math.dist(list([curr.x, curr.y]), list(point)) / 2000

            pyautogui.moveTo(point[0], point[1], duration=duration)
            pyautogui.click(point[0], point[1])

            result = TestResult(TestResult.RunningFlag, "执行click完成")
            result.addRectItem(TestRect(point[0], point[1], 0, 0))
            result.setNext(self.getChild())
            return result

        return TestResult(TestResult.CriticalFlag, "执行click错误: 缺少坐标点")

    def _leftClickOperate(self):
        # 1计算出点击坐标 2移动到点击坐标 3左击
        # TODO: 持续时间未实现
        if point := TestInterpret.fn1(self._configPoint, self._configOffset):
            curr = pyautogui.position()
            duration = math.dist(list([curr.x, curr.y]), list(point)) / 2000

            pyautogui.moveTo(point[0], point[1], duration=duration)
            pyautogui.leftClick(point[0], point[1])

            result = TestResult(TestResult.RunningFlag, "执行leftClick完成")
            result.addRectItem(TestRect(point[0], point[1], 0, 0))
            result.setNext(self.getChild())
            return result

        return TestResult(TestResult.CriticalFlag, "执行leftClick错误: 缺少坐标点")

    def _rightClickOperate(self):
        # 1计算出点击坐标 2移动到点击坐标 3右击
        # TODO: 持续时间未实现
        if point := TestInterpret.fn1(self._configPoint, self._configOffset):
            curr = pyautogui.position()
            duration = math.dist(list([curr.x, curr.y]), list(point)) / 2000

            pyautogui.moveTo(point[0], point[1], duration=duration)
            pyautogui.rightClick(point[0], point[1])

            result = TestResult(TestResult.RunningFlag, "执行rightClick完成")
            result.addRectItem(TestRect(point[0], point[1], 0, 0))
            result.setNext(self.getChild())
            return result

        return TestResult(TestResult.CriticalFlag, "执行rightClick错误: 缺少坐标点")

    def _doubleClickOperate(self):
        # 1计算出点击坐标 2移动到点击坐标 3双击
        if point := TestInterpret.fn1(self._configPoint, self._configOffset):
            curr = pyautogui.position()
            duration = math.dist(list([curr.x, curr.y]), list(point)) / 2000

            pyautogui.moveTo(point[0], point[1], duration=duration)
            pyautogui.doubleClick(point[0], point[1])

            result = TestResult(TestResult.RunningFlag, "执行doubleClick完成")
            result.addRectItem(TestRect(point[0], point[1], 0, 0))
            result.setNext(self.getChild())
            return result

        return TestResult(TestResult.CriticalFlag, "执行doubleClick错误: 缺少坐标点")

    def _moveOperate(self):
        # 1计算出目的坐标 2移动到坐标
        if point := TestInterpret.fn1(self._configPoint, self._configOffset):
            curr = pyautogui.position()
            duration = math.dist(list([curr.x, curr.y]), list(point)) / 2000

            pyautogui.moveTo(point[0], point[1], duration=duration)

            result = TestResult(TestResult.RunningFlag, "执行move完成")
            result.addRectItem(TestRect(point[0], point[1], 0, 0))
            result.setNext(self.getChild())
            return result

        return TestResult(TestResult.CriticalFlag, "执行move错误: 缺少坐标点")

    def _dragOperate(self):
        # 1计算出目的坐标 2拖动到坐标
        if point := TestInterpret.fn1(self._configPoint, self._configOffset):
            curr = pyautogui.position()
            duration = math.dist(list([curr.x, curr.y]), list(point)) / 2000

            pyautogui.dragTo(point[0], point[1], duration=duration)

            result = TestResult(TestResult.RunningFlag, "执行drag完成")
            result.addRectItem(TestRect(point[0], point[1], 0, 0))
            result.setNext(self.getChild())
            return result

        return TestResult(TestResult.CriticalFlag, "执行drag错误: 缺少坐标点")

    def _wheelOperate(self):
        # 1计算出目的坐标 2移动到目的坐标 3滚动(不管前面2步是否完成)
        if point := TestInterpret.fn1(self._configPoint, self._configOffset):
            curr = pyautogui.position()
            duration = math.dist(list([curr.x, curr.y]), list(point)) / 2000
            pyautogui.moveTo(point[0], point[1], duration=duration)

        pyautogui.scroll(self._configRoll * -120)

        pos = pyautogui.position()
        result = TestResult(TestResult.RunningFlag, "执行wheel完成")
        result.addRectItem(TestRect(pos.x, pos.y, 0, 0))
        result.setNext(self.getChild())
        return result

    def _keyOperate(self):
        # 1计算出目的坐标 2移动到目的坐标 3不管是否移动都按下按键
        if point := TestInterpret.fn1(self._configPoint, self._configOffset):
            curr = pyautogui.position()
            duration = math.dist(list([curr.x, curr.y]), list(point)) / 2000
            pyautogui.moveTo(point[0], point[1], duration=duration)

        if _checkKeyValid(self._configKeys):
            pyautogui.keyDown(self._configKeys[0])
            time.sleep(self._configTime/1000)
            pyautogui.keyUp(self._configKeys[0])

            pos = pyautogui.position()
            result = TestResult(TestResult.RunningFlag, "执行key完成")
            result.addRectItem(TestRect(pos.x, pos.y, 0, 0))
            result.setNext(self.getChild())
            return result

        return TestResult(TestResult.CriticalFlag, "执行key失败: 按键序列不合法")

    def _keysOperate(self):
        # 1计算出目的坐标 2移动到目的坐标 3不管是否移动都按下按键
        if point := TestInterpret.fn1(self._configPoint, self._configOffset):
            curr = pyautogui.position()
            duration = math.dist(list([curr.x, curr.y]), list(point)) / 2000
            pyautogui.moveTo(point[0], point[1], duration=duration)

        if _checkKeyValid(self._configKeys):
            pyautogui.hotkey(*self._configKeys)

            pos = pyautogui.position()
            result = TestResult(TestResult.RunningFlag, "执行keys完成")
            result.addRectItem(TestRect(pos.x, pos.y, 0, 0))
            result.setNext(self.getChild())
            return result

        return TestResult(TestResult.CriticalFlag, "执行keys错误: 按键序列不合法")

    def _copyPasteOperate(self):
        # 1计算出目的坐标 2移动到目的坐标 3点击输入框 4复制缓存区内容 5粘贴快捷键
        if point := TestInterpret.fn1(self._configPoint, self._configOffset):
            curr = pyautogui.position()
            duration = math.dist(list([curr.x, curr.y]), list(point)) / 2000
            pyautogui.moveTo(point[0], point[1], duration=duration)
            pyautogui.click(point[0], point[1])

        if text := TestInterpret.fn2(self._configContent):
            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")

            result = TestResult(TestResult.RunningFlag, "执行copyPaste完成")
            result.setNext(self.getChild())
            return result

        return TestResult(TestResult.CriticalFlag, "执行copyPaste错误: 缓存区没有找到数据")


def _returnConfigsValue(key: str, data: dict):
    ret = None
    if key == 'point':
        ret = _defaultPoint
        val = data.get(key, ret)
        if isinstance(val, str):
            ret = val
    elif key == 'offset':
        ret = _defaultOffset
        val = data.get(key, ret)
        if isinstance(val, dict):
            ret = val
    elif key == 'time':
        ret = _defaultTime
        val = data.get(key, ret)
        if isinstance(val, int) and 0 < val:
            ret = val
    elif key == 'keys':
        ret = _defaultKeys
        val = data.get(key, ret)
        if isinstance(val, list):
            ret = val
    elif key == 'roll':
        ret = _defaultRoll
        val = data.get(key, ret)
        if isinstance(val, int) and 0 < val:
            ret = val
    elif key == 'content':
        ret = _defaultContent
        val = data.get(key, ret)
        if isinstance(val, str):
            ret = val

    return ret


def _checkKeyValid(keys: list):
    # TODO: 完善检查按键是否合法
    return len(keys)



