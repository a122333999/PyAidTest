# -*- coding:utf-8 -*-

import time

"""
Msg {
    type: trace|debug|info|warning|error|critical
    time: 10-int-timestamp + float
    text: str message
}
"""


def trace(msg, mod=None):
    global _sink

    for item in _sink.values():
        item({"type": "trace", "time": time.time(), "text": msg})


def debug(msg, mod=None):
    global _sink
    for item in _sink.values():
        item({"type": "debug", "time": time.time(), "text": msg})


def info(msg, mod=None):
    global _sink
    for item in _sink.values():
        item({"type": "info", "time": time.time(), "text": msg})


def warn(msg, mod=None):
    global _sink
    for item in _sink.values():
        item({"type": "warning", "time": time.time(), "text": msg})


def error(msg, mod=None):
    global _sink
    for item in _sink.values():
        item({"type": "error", "time": time.time(), "text": msg})


def critical(msg, mod=None):
    print({"type": "critical", "time": time.time(), "text": msg})


def addHandle(name, func):
    """ func 是可调用对象 """
    global _sink
    _sink[name] = func


def rmvHandle(name):
    global _sink
    _sink.pop(name)


def _stdSink(msg: dict):
    """ 标准输出 """
    at = time.localtime(msg['time'])
    st = time.strftime("%Y-%m-%d %H:%M:%S", at)
    print(f"{st} [{msg['type']}] - {msg['text']}")


_sink = {"std": _stdSink}
