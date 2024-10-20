# -*- coding:utf-8 -*-


class TestRuntime:
    isRunning = False
    isWaiting = False
    isStopping = False

    currentHandle = 0
    currentResult = None
    historyResult = dict()

    buffInfo = None
    inputData = None
    errorList = list()

    pathPrefix = {
        "${app}": "",
        "${pro}": "",
        "${case}": ""
    }

    @classmethod
    def clear(cls):
        cls.isRunning = False
        cls.isWaiting = False
        cls.isStopping = False
        cls.currentHandle = 0
        cls.currentResult = None
        cls.historyResult = dict()
        cls.inputData = None
        cls.errorInfo = list()

    @classmethod
    def toAbsPath(cls):
        """把路径转换成绝对路径 也就是替换 ${app} ${pro} ${case} """
        pass

