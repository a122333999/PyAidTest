# -*- coding:utf-8 -*-

from ExecuteModule.TestBase import TestBase


class TestGroup(TestBase):

    _type = "group"

    def __init__(self):
        super().__init__()
        self.setName("TestGroup")
        self.setDesc("This TestGroup")
        self._caseList = list()

    def addCaseItem(self, case):
        self._caseList.append(case)

    def getCaseList(self):
        return self._caseList

