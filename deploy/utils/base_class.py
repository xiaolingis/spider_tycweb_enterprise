#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/7/4 3:43 PM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python base_class.py
# ------------------------------------------------------------
import threading


class BASECLASS(object):

    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        super(BASECLASS, self).__init__()
        self.init_run()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with BASECLASS._instance_lock:
                cls._instance = object.__new__(cls)
        return cls._instance

    def init_run(self):
        pass



