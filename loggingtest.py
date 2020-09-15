'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 
Date: 2020-09-15 21:44:35
LastEditTime: 2020-09-15 21:45:01
'''
# coding utf-8

import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

logger.info('1111111111')