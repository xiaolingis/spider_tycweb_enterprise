#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/7/9 3:22 PM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python utils.py
# ------------------------------------------------------------
import random
import time
import os
import hashlib
import sys
import inspect
from datetime import datetime
from deploy.config import OUTPUT_BASE_DIR


# 随机sleep
def random_sleep(min=3, max=5):
    return time.sleep(random.uniform(min, max))


# md5加密
def md5(v):
    return hashlib.md5(v).hexdigest()


# 字符串转日期
def s2d(s, fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(s, fmt)


# 日期转字符串
def d2s(d, fmt="%Y-%m-%d %H:%M:%S"):
    return d.strftime(fmt)


# 日期转ts
def d2ts(d):
    return time.mktime(d.timetuple())


# 字符串转ts
def s2ts(s, format="%Y-%m-%d %H:%M:%S"):
    d = s2d(s, format)
    return d2ts(d)


# 获取日期差额
def dura_date(d1, d2, need_d=False):
    if type(d1) is str:
        d1 = s2d(d1)
    if type(d2) is str:
        d2 = s2d(d2)
    d = d2 - d1
    if need_d is False:
        seconds = d.seconds
        mins = seconds / 60.00
        hours = mins / 60.00
        return seconds, mins, hours
    return d


# 获取当前时间
def get_now_date():
    return datetime.now()


# 获取当前时间str
def get_now(format="%Y-%m-%d %H:%M:%S"):
    return d2s(datetime.now(), format)


# 获取weekday
def get_week_day(date):
    weekdaylist = ('星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天')
    weekday = weekdaylist[date.weekday()]
    return weekday


# get excel folder
def get_excel_folder():
    if getattr(sys, "frozen", False):
        root_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
    else:
        cur_folder = os.path.dirname(inspect.getfile(inspect.currentframe()))
        root_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(cur_folder)
            )
        )

    return os.path.join(root_dir, OUTPUT_BASE_DIR)


