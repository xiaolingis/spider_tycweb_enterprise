#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/7/6 1:21 PM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python tianyancha.py
# ------------------------------------------------------------
from urllib import parse
from bs4 import BeautifulSoup

from deploy.config import RUN_MODE, TYC_DETAIL_API, \
    TYC_SEARCH_API, TYC_COOKIE
from deploy.utils.http import api_get
from deploy.utils.logger import logger as LOG
from deploy.utils.utils import random_sleep


class TianYanChaClient(object):
    """
    tianyancha client
    """
    def __init__(self):
        super(object, self).__init__()
        self.MAX_PAGE = 5
        self._init_header()

    def _init_header(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "version": "TYC-XCX-WX",
            "Host": "www.tianyancha.com",
            "Cookie": TYC_COOKIE,
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "document",
            # "X-Forwarded-For":
        }

    def work_by_key(self, key):
        ret_res = list()
        if not key:
            LOG.error("【%s】key is null, no work." % RUN_MODE)
            return ret_res

        # page
        for page in range(0, self.MAX_PAGE, 1):
            url = TYC_SEARCH_API + '/p%s?key=' % page + parse.quote(key)
            is_ok, search_resp = api_get(url=url,
                                  headers=self.headers,
                                  data={},
                                  resptype='text')
            if not is_ok:
                return []

            soup = BeautifulSoup(search_resp, 'lxml')
            tags = soup.find_all('a',attrs={"tyc-event-ch": "CompanySearch.Company"})
            for tag in tags:
                if not tag or not tag.attrs.get('href'):
                    continue

                res_dict = dict()
                res_dict['tyt_url'] = tag.get('href').strip()
                res_dict['name'] = tag.get_text().strip()

                detail_res = self.detail_by_url(res_dict.get('tyt_url'))
                res_dict.update(detail_res)
                print(res_dict['name'], res_dict['tyt_url'], True if res_dict else False)
                ret_res.append(res_dict)
                random_sleep()

        return ret_res


    def detail_by_url(self, comp_url: str):
        detail_res = dict()
        if not comp_url:
            return detail_res

        is_ok, search_resp = api_get(url=comp_url,
                              headers=self.headers,
                              data={},
                              resptype='text')
        if not is_ok:
            return detail_res

        soup = BeautifulSoup(search_resp, 'lxml')

        # detail: 电话 邮箱 公司官网 地址 简介
        detail_div = soup.find_all('div', class_="detail")
        if not detail_div:
            return detail_res

        for div in detail_div[0].find_all('div'):
            if not div:
                continue

            # f0 电话 && 邮箱
            if div.get('class') == ['f0']:
                for big_index, big_child in enumerate(div):
                    if big_index == 0:
                        for index, child in enumerate(big_child.children):
                            if index == 1:
                                detail_res['phone'] = child.get_text().strip() or '-'
                                break
                    elif big_index == 1:
                        for index, child in enumerate(big_child.children):
                            if index == 1:
                                detail_res['email'] = child.get_text().strip() or '-'
                                break
                    else:
                        break
            # 公司官网 && 地址
            elif div.get('class') == ['f0', 'clearfix']:
                for big_index, big_child in enumerate(div):
                    if big_index == 0:
                        for index, child in enumerate(big_child.children):
                            if index == 1:
                                detail_res['company_url'] = child.get_text().strip() or '-'
                                break
                    elif big_index == 1:
                        for index, child in enumerate(big_child.children):
                            if index == 1:
                                for small_index, small_child in enumerate(child.children):
                                    if small_index == 0:
                                        detail_res['address'] = small_child.get_text().strip() or '-'
                                        break
                                break
                    else:
                        break
            # 简介
            elif div.get('class') == ['summary']:
                for big_index, big_child in enumerate(div):
                    if big_index == 0:
                        resume = big_child.string
                        if resume:
                            resume = resume.strip()
                        detail_res['resume'] = resume or '-'
                        break
                    else:
                        break
            else:
                continue

        # detail-list:
        detail_list_div = soup.find_all('div', class_="detail-list")
        if not detail_list_div:
            return detail_res

        for div in detail_list_div[0].find_all('div'):
            if not div:
                continue

            if div.get('tyc-event-ch') == 'CompangyDetail.gongshangxinxin':
                for index_1, child_1 in enumerate(div.find_all('div', recursive=False)):
                    if index_1 == 1:
                        for index_1_1, child_1_1 in enumerate(child_1):
                            if index_1_1 == 2:
                                for index_tr, tr in enumerate(child_1_1.find_all('tr')):
                                    if index_tr == 0:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:   # 注册资本
                                                detail_res['register_funds'] = td.get_text().strip() or '-'
                                            elif index_td == 3: # 实缴资金
                                                detail_res['paidin_funds'] =  td.get_text().strip() or '-'
                                    elif index_tr == 1:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:   # 注册资本
                                                detail_res['establish_date'] = td.get_text().strip() or '-'
                                            elif index_td == 3: # 经营状态
                                                detail_res['status'] =  td.get_text().strip() or '-'
                                    elif index_tr == 2:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:   # 注册资本
                                                detail_res['credit_code'] = td.get_text().strip() or '-'
                                    elif index_tr == 4:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:   # 公司类型
                                                detail_res['company_type'] = td.get_text().strip() or '-'
                                            elif index_td == 3: # 行业
                                                detail_res['industry'] =  td.get_text().strip() or '-'
                                    elif index_tr == 6:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:   # 营业期限
                                                detail_res['business_term'] = td.get_text().strip() or '-'
                                    elif index_tr == 10:
                                        for index_td, td in enumerate(tr.find_all('td')):
                                            if index_td == 1:   # 经营范围
                                                detail_res['business_scope'] = td.get_text().strip() or '-'

                        break
                break

        return detail_res







