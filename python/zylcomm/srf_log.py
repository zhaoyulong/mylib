#coding:utf-8
"""
封装logging模块，提供了两种配置方式：
1、利用字典对象初始化: 可以根据需求修改dict，更加灵活；
2、直接编码初始化: 使用起来更加简单
"""

import os
import sys
import traceback
import logging
import logging.config

logger = logging.getLogger("debug")
logger_d = logging.getLogger("daily")
logger_e = logging.getLogger("error")


def init_log(log_path, log_name, log_level = "DEBUG"):
    '''利用dict配置logger对象，更灵活'''
    log_level = log_level.upper()

    LOG_PATH_DEBUG = "%s/%s_debug.log" % (log_path,log_name)
    LOG_PATH_DAILY = "%s/%s_daily.log" % (log_path,log_name)
    LOG_PATH_ERROR = "%s/%s_error.log" % (log_path,log_name)
    #单个日志文件的最大大小
    LOG_FILE_MAX_BYTES = 60 * 1024 * 1024
    #日志文件个数
    LOG_FILE_BACKUP_COUNT = 7

    log_conf = {
        "version" : 1, 
        "formatters" : {
            "format1" : {
                "format" : '%(asctime)-15s [%(thread)d] - [%(filename)s %(lineno)d]' + \
                           ' %(levelname)s %(message)s',
            },
        },

        "handlers" : {
            "handler1": {
                "class" : "logging.handlers.TimedRotatingFileHandler",
                "level" : "INFO",
                "formatter" : "format1",
                "when" : 'midnight',
                "backupCount" : LOG_FILE_BACKUP_COUNT,
                "filename" : LOG_PATH_DAILY
            },
            "handler2": {
                "class" : "logging.handlers.RotatingFileHandler",
                "level" : log_level,
                "formatter" : "format1",
                "maxBytes" :  LOG_FILE_MAX_BYTES,
                "backupCount" : LOG_FILE_BACKUP_COUNT,
                "filename" : LOG_PATH_DEBUG
            },
            "handler3": {
                "class" : "logging.handlers.RotatingFileHandler",
                "level" : "ERROR",
                "formatter" : "format1",
                "maxBytes" :  LOG_FILE_MAX_BYTES,
                "backupCount" : LOG_FILE_BACKUP_COUNT,
                "filename" : LOG_PATH_ERROR
            },
        },

        "loggers" : {
            "daily" : {
                "handlers" : ["handler1"],
                "level" : "INFO", 
            },
            "debug": {
                "handlers" : ["handler2"],
                "level" : log_level
            },
            "error": {
                "handlers" : ["handler3"],
                "level" : "ERROR"
            },
        }
    }
    logging.config.dictConfig(log_conf)


def init_log_s(log_path, log_name, log_level = "DEBUG"):
    LOG_PATH_DEBUG = "%s/%s_debug.log" % (log_path,log_name)
    LOG_PATH_DAILY = "%s/%s_daily.log" % (log_path,log_name)
    LOG_PATH_ERROR = "%s/%s_error.log" % (log_path,log_name)
    LOG_FILE_MAX_BYTES = 102400000 #单个日志文件的最大大小
    LOG_DAILY_COUNT = 30 # 每日log 30个
    LOG_FILE_BACKUP_COUNT = 7 #日志文件个数
    
    LOG_LEVEL = logging.DEBUG
    if log_level.lower() == "debug":
        LOG_LEVEL = logging.DEBUG
    elif log_level.lower() == "info":
        LOG_LEVEL = logging.INFO
    elif log_level.lower() == "warning":
        LOG_LEVEL = logging.WARNING
    elif log_level.lower() == "error":
        LOG_LEVEL = logging.ERROR
    elif log_level.lower() == "critical":
        LOG_LEVEL = logging.CRITICAL
    
    #记录信息按天回滚
    dailyHandler = logging.handlers.TimedRotatingFileHandler(LOG_PATH_DAILY,
                                                             'midnight',
                                                             backupCount = LOG_DAILY_COUNT)
    dailyHandler.setLevel(logging.INFO)
    
    #警告以上信息按文件大小(100M)回滚
    errorHandler = logging.handlers.RotatingFileHandler(LOG_PATH_ERROR,
                                                        maxBytes=LOG_FILE_MAX_BYTES,
                                                        backupCount=LOG_FILE_BACKUP_COUNT)
    errorHandler.setLevel(logging.ERROR)
    
    #警告以上信息按文件大小(100M)回滚
    debugHandler = logging.handlers.RotatingFileHandler(LOG_PATH_DEBUG,
                                                        maxBytes=LOG_FILE_MAX_BYTES,
                                                        backupCount=LOG_FILE_BACKUP_COUNT)
    debugHandler.setLevel(LOG_LEVEL)
    
    #日志格式
    formatter = logging.Formatter(
        '%(asctime)-15s [%(thread)d] - [%(filename)s %(lineno)d] %(levelname)s %(message)s'
    )
    dailyHandler.setFormatter(formatter)
    debugHandler.setFormatter(formatter)
    errorHandler.setFormatter(formatter)
    
    #logger对象
    logger_daily = logging.getLogger(LOG_PATH_DAILY)
    logger_daily.setLevel(logging.INFO)
    logger_daily.addHandler(dailyHandler)
    
    logger_error = logging.getLogger(LOG_PATH_ERROR)
    logger_error.setLevel(logging.ERROR)
    logger_error.addHandler(errorHandler)
    
    logger_debug = logging.getLogger(LOG_PATH_DEBUG)
    logger_debug.setLevel(LOG_LEVEL)
    logger_debug.addHandler(debugHandler)
    
    #TODO 如果创建logger失败需要如何?
    return logger_debug,logger_daily,logger_error
    
    
def close_log():
    logging.shutdown()

