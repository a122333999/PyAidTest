# -*- coding:utf-8 -*-


class TestRect:
    def __init__(self, xpos=0, ypos=0, width=100, height=100):
        self._xpos = int(xpos)
        self._ypos = int(ypos)
        self._width = int(width)
        self._height = int(height)
        if not self._checkRect():
            self._clearRect()

    def __str__(self):
        return f"Rect: xpos={self._xpos}, ypos={self._ypos}, width={self._width}, height={self._height}"

    def isValid(self):
        return self._checkRect()

    def getXpos(self):
        return self._xpos

    def setXpos(self, x):
        self._xpos = int(x)
        if not self._checkRect():
            self._clearRect()

    def getYpos(self):
        return self._ypos

    def setYpos(self, y):
        self._ypos = int(y)
        if not self._checkRect():
            self._clearRect()

    def getWidth(self):
        return self._width

    def setWidth(self, w):
        self._width = int(w)
        if not self._checkRect():
            self._clearRect()

    def getHeight(self):
        return self._height

    def setHeight(self, h):
        self._height = int(h)
        if not self._checkRect():
            self._clearRect()

    def getCenterPoint(self, offset=(0, 0)):
        hp = self._xpos + (self._width // 2)
        vp = self._ypos + (self._height // 2)
        return tuple([hp + offset[0], vp + offset[1]])

    def getTopCenterPoint(self, offset=(0, 0)):
        hp = self._xpos + (self._width // 2)
        vp = self._ypos
        return tuple([hp + offset[0], vp + offset[1]])

    def getTopRightPoint(self, offset=(0, 0)):
        hp = self._xpos + self._width
        vp = self._ypos
        return tuple([hp + offset[0], vp + offset[1]])

    def getTopLeftPoint(self, offset=(0, 0)):
        hp = self._xpos
        vp = self._ypos
        return tuple([hp + offset[0], vp + offset[1]])

    def getBottomCenterPoint(self, offset=(0, 0)):
        hp = self._xpos + (self._width // 2)
        vp = self._ypos + self._height
        return tuple([hp + offset[0], vp + offset[1]])

    def getBottomRightPoint(self, offset=(0, 0)):
        hp = self._xpos + self._width
        vp = self._ypos + self._height
        return tuple([hp + offset[0], vp + offset[1]])

    def getBottomLeftPoint(self, offset=(0, 0)):
        hp = self._xpos
        vp = self._ypos + self._height
        return tuple([hp + offset[0], vp + offset[1]])

    def getLeftCenterPoint(self, offset=(0, 0)):
        hp = self._xpos
        vp = self._ypos + (self._height // 2)
        return tuple([hp + offset[0], vp + offset[1]])

    def getRightCenterPoint(self, offset=(0, 0)):
        hp = self._xpos + self._width
        vp = self._ypos + (self._height // 2)
        return tuple([hp + offset[0], vp + offset[1]])

    def toTupleRect(self):
        return tuple([self._xpos, self._ypos, self._xpos+self._width, self._ypos+self._height])

    def limitTopLine(self, limit: tuple):
        xpos, ypos = _checkLimit(limit)
        differ = ypos - self._ypos  # 差值
        # 限定顶侧边界
        self._ypos = ypos
        self._height -= differ
        if not self._checkRect():
            self._clearRect()

    def limitLeftLine(self, limit: tuple):
        xpos, ypos = _checkLimit(limit)
        differ = xpos - self._xpos  # 差值
        # 限定左侧边界
        self._xpos = xpos
        self._width -= differ
        if not self._checkRect():
            self._clearRect()

    def limitRightLine(self, limit: tuple):
        xpos, ypos = _checkLimit(limit)
        differ = xpos - (self._xpos + self._width)  # 差值
        # 限定右侧边界
        self._width += differ
        if not self._checkRect():
            self._clearRect()

    def limitBottomLine(self, limit: tuple):
        xpos, ypos = _checkLimit(limit)
        differ = ypos - (self._ypos + self._height)  # 差值
        # 限定底侧边界
        self._height += differ
        if not self._checkRect():
            self._clearRect()

    def miss(self, rect):
        """表示自身位置距离rect位置缺少的x和y偏移量"""
        return rect.getXpos() - self._xpos, rect.getYpos() - self._ypos

    def move(self, x, y):
        """表示把自身移动指定的x和y偏移量(相对移动)"""
        self._xpos += x
        self._ypos += y
        if not self._checkRect():
            self._clearRect()

    def moveTo(self, x, y):
        """表示把自身移动到指定的x和y位置(绝对移动)"""
        self._xpos = x
        self._ypos = y
        if not self._checkRect():
            self._clearRect()

    def _clearRect(self):
        self._xpos = -1
        self._ypos = -1
        self._width = -1
        self._height = -1

    def _checkRect(self):
        if self._xpos < 0 or self._ypos < 0 or self._width < 0 or self._height < 0:
            return False
        return True


def _checkLimit(limit: tuple) -> tuple:
    if not isinstance(limit, tuple):
        return -1, -1
    if len(limit) < 2:
        return -1, -1
    if not isinstance(limit[0], int) or not isinstance(limit[1], int):
        return -1, -1
    return limit




