# -*- coding:utf-8 -*-


# 提示: 输入说明 + 按钮组
# 编辑: 输入说明 + 文本输入框 + 确定组


class TestInput:

    Continuing = 0
    Finished = 1
    Failed = 2

    def __init__(self, behavior=Continuing):
        self._behavior = int(behavior)
        self._inputText = None

    def getBehavior(self):
        return self._behavior

    def setInputText(self, text):
        self._inputText = text

    def getInputText(self):
        return self._inputText
