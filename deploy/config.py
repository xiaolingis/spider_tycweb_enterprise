#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    the run configuration information of the project
    use analyse to the config of yaml formatter
    information:
        - SERVER
        - LOG
        - DB
        - FILES: output file or ...

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/7/4 3:23 PM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python config.py
# ------------------------------------------------------------
import os
import sys
import yaml
import inspect
import logging


# logging.basicConfig()
logger = logging.getLogger(__name__)


# get current folder, solve is or not frozen of the script
def _get_cur_folder():
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(__file__))
    else:
        cur_folder = os.path.dirname(inspect.getfile(inspect.currentframe()))
        return os.path.abspath(cur_folder)


# get current run config by mode
def _get_config():
    return os.path.join((os.path.dirname(_get_cur_folder())), 'etc/config.yaml')


# default log dir
def __get_log_dir():
    return os.path.join(os.path.dirname(_get_cur_folder()), 'log')


# default excel dir
def __get_excel_dir():
    return os.path.join(os.path.dirname(_get_cur_folder()), 'excel')


"""
default config
"""
# SERVER
NAME = 'Spider_TYC_Enterprise'
VERSION = '1.0.0'
DEBUG = True
KEYS = None
RUN_MODE = 'single'

# DB(sqlalchemy)，default is mysql
DB_LINK = None

# LOG
LOG_DIR = __get_log_dir()
LOG_LEVEL = "debug"
LOG_FORMATTER = "%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s - %(message)s"
LOG_FILENAME_PREFIX = 'spider_tyc_enterprise'

# files
OUTPUT_BASE_DIR = __get_excel_dir()

# store
STORE_EXCEL = True
STORE_DB = False

#apis
TYC_SEARCH_API = None
TYC_DETAIL_API = None
TYC_COOKIE = None

# proxy
PROXY_API = None
IS_PROXY_RUN = False


"""
enrty: initializate config
"""
_config_file = _get_config()
if not os.path.exists(_config_file):
    logger.critical('====== config file is not exist, exit ======')
    sys.exit(1)

with open(_config_file) as f:
    _config_info = yaml.safe_load(f)
    if not _config_info:
        logger.critical('====== config file is unavail, exit ======')
        sys.exit(1)

    # SERVER
    NAME = _config_info['SERVER']['NAME'] or NAME
    VERSION = _config_info['SERVER']['VERSION'] or VERSION
    DEBUG = _config_info['SERVER']['DEBUG'] or DEBUG
    KEYS = _config_info['SERVER']['KEYS'] or KEYS
    if not KEYS:
        logger.critical('====== config KEYS is not allow NULL... ======')
        sys.exit(1)
    KEYS = KEYS.split(',')
    RUN_MODE = _config_info['SERVER']['RUN_MODE'] or RUN_MODE

    # DB(sqlalchemy)，default is mysql
    DB_LINK = _config_info['DB']['DB_LINK'] or DB_LINK

    # LOG
    LOG_DIR = _config_info['LOG']['LOG_DIR'] or LOG_DIR
    if not os.path.exists(LOG_DIR):
        logger.critical('====== log dir is not exist, create %s... ======' % LOG_DIR)
        os.makedirs(LOG_DIR)
    LOG_LEVEL = _config_info['LOG']['LOG_LEVEL'] or LOG_LEVEL
    LOG_FORMATTER = _config_info['LOG']['LOG_FORMATTER'] or LOG_FORMATTER
    LOG_FILENAME_PREFIX = _config_info['LOG']['LOG_FILENAME_PREFIX'] or LOG_FILENAME_PREFIX

    # files
    OUTPUT_BASE_DIR = _config_info['FILES']['OUTPUT_BASE_DIR'] or OUTPUT_BASE_DIR

    # store
    STORE_EXCEL = _config_info['STORE']['EXCEL'] or STORE_EXCEL
    STORE_DB = _config_info['STORE']['DB'] or STORE_DB

    # api
    TYC_SEARCH_API = _config_info['APIS']['TYC_SEARCH'] or TYC_SEARCH_API
    TYC_DETAIL_API = _config_info['APIS']['TYC_DETAIL'] or TYC_DETAIL_API
    TYC_COOKIE = _config_info['APIS']['TYC_COOKIE'] or TYC_COOKIE

    # proxy
    PROXY_API = _config_info['PROXY']['API'] or PROXY_API
    IS_PROXY_RUN = _config_info['PROXY']['IS_RUN'] or IS_PROXY_RUN