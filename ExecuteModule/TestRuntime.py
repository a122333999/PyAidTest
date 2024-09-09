

class TestRuntime:
    isRunning = False
    isWaiting = False
    isStopping = False

    currHandle = 0
    currResult = None
    bufferResult = dict()

    inputData = object()
    errorInfo = list()

    @classmethod
    def clear(cls):
        cls.isRunning = False
        cls.isWaiting = False
        cls.isStopping = False
        cls.currHandle = 0
        cls.currResult = None
        cls.bufferResult = dict()
        cls.inputData = object()
        cls.errorInfo = list()
