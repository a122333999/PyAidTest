# -*- coding:utf-8 -*-
import json


def getPt():
    return _projectTemp


def getExt():
    return _projectExt


def getTft():
    return _testFileTemp


# 项目文件扩展名
_projectExt = ".json"


# 项目文件模板
_projectTemp = \
    """
{
    "info": {
         "version": 0,
         "prefix": {}
    },
    "entry": []
}
"""


# 测试文件模板
_testFileTemp = \
"""
{
    "type": "group",
    "iden": "",
    "name": "",
    "desc": "",
    "cases": []
}
"""
