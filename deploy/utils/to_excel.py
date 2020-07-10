#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/7/10 9:27 AM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python to_excel.py
# ------------------------------------------------------------
import xlwt
import os


from deploy.utils.logger import logger as LOG
from deploy.utils.utils import get_now, get_excel_folder

class ToExcel(object):

    def __init__(self):
        super(ToExcel, self).__init__()

    @classmethod
    def set_style(name, height, bold=False):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style

    # 写Excel
    def to_excel(self, datas, columns: dict, exlname=None):
        if not datas:
            LOG.error('to excel datas is null')
            return False
        if not columns:
            LOG.error('to excel columns is null')
            return False
        if not isinstance(columns, dict):
            LOG.error('to excel columns is need dict')
            return False
        if not exlname:
            exlname = os.path.join(get_excel_folder(), '%s.xls' % get_now())

        f = xlwt.Workbook(encoding='utf-8')
        sheet = f.add_sheet('sheet', cell_overwrite_ok=True)
        row0 = list(columns.keys())
        row0.insert(0, 'ID')
        columns.update({'ID':'序号'})

        style_title = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = True
        font.color_index = 4
        font.height = 220
        style_title.font = font

        style_content = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = False
        font.color_index = 4
        font.height = 220
        style_content.font = font

        # 标题
        for i in range(0, len(row0)):
            sheet.write(0, i, columns.get(row0[i]), style_title)

        row = 1
        for line in datas:
            if not line:
                continue
            for index, data in enumerate(row0):
                if index == 0:
                    sheet.write(row, index, row, style_title)
                else:
                    sheet.write(row, index, line.get(row0[index]), style_content)

            row += 1

        f.save(exlname)
        return exlname





