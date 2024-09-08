

class TestResult:

    def __init__(self):
        super().__init__()
        self._rects = list()

    def isValid(self):
        return bool(len(self._rects))

    def addRectItem(self, rect):
        self._rects.append(rect)

    def getRectSize(self):
        return len(self._rects)

    def getRectList(self):
        return self._rects

    def getRectInfo(self, index):
        return self._rects[index]

    def getCenterPoint(self, index=0, offset=(0, 0)):
        pass

    def getTopCenterPoint(self, index=0, offset=(0, 0)):
        pass

    def getTopRightPoint(self, index=0, offset=(0, 0)):
        pass

    def getTopLeftPoint(self, index=0, offset=(0, 0)):
        pass

    def getBottomCenterPoint(self, index=0, offset=(0, 0)):
        pass

    def getBottomRightPoint(self, index=0, offset=(0, 0)):
        pass

    def getBottomLeftPoint(self, index=0, offset=(0, 0)):
        pass

    def getRightCenterPoint(self, index=0, offset=(0, 0)):
        pass

    def getLeftCenterPoint(self, index=0, offset=(0, 0)):
        pass


