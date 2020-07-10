#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/7/6 2:17 PM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python http.py
# ------------------------------------------------------------
import requests
import json


def api_post(url, headers, data, retry=1, resptype='json'):
    """
    http post
    :param url: url
    :param headers: headers
    :param data: data
    :return: response
    """
    if not url:
        return False, 'api_post url is not allow null'

    if isinstance(data, dict):
        data = json.dumps(data)
    if not isinstance(headers, dict):
        headers = json.dumps(headers)

    try:
        response = requests.post(url=url, headers=headers,
                                 data=data, timeout=5)
    except Exception as e:
        if retry <= 3:
            api_post(url=url,
                     headers=headers,
                     data=data,
                     retry=retry + 1,
                     resptype='json')
        else:
            raise Exception('http api_post error: %s' % e)
    else:
        respcode = response.status_code
        if respcode != 200:
            return False, 'api_post response status code is: %s' % respcode
        elif respcode == 200 and resptype == 'raw':
            return True, response.raw
        elif respcode == 200 and resptype == 'content':
            return True, response.content
        elif respcode == 200 and resptype == 'json':
            return True, response.json()
        else:
            return True, response.text


def api_get(url, headers, data, retry=1, resptype='json'):
    """
    http get
    :param url: url
    :param headers: headers
    :param data: data
    :return: response
    """
    if not url:
        return False, 'api_get url is not allow null'

    if isinstance(data, dict):
        data = json.dumps(data)
    if not isinstance(headers, dict):
        headers = json.dumps(headers)

    try:
        response = requests.get(url=url, headers=headers,
                                data=data, timeout=5)
    except Exception as e:
        if retry <= 3:
            api_get(url, headers, data, retry=retry + 1, resptype='json')
        else:
            raise Exception(u'api_get error: %s' % e)
    else:
        respcode = response.status_code
        if respcode != 200:
            return False, 'api_get response status code is: %s' % respcode
        elif respcode == 200 and resptype == 'raw':
            return True, response.raw
        elif respcode == 200 and resptype == 'content':
            return True, response.content
        elif respcode == 200 and resptype == 'json':
            return True, response.json()
        else:
            return True, response.text
