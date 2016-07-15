#coding:utf-8
"""
��װloggingģ�飬�ṩ���������÷�ʽ��
1�������ֵ�����ʼ��: ���Ը��������޸�dict��������
2��ֱ�ӱ����ʼ��: ʹ���������Ӽ�
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
    '''����dict����logger���󣬸����'''
    log_level = log_level.upper()

    LOG_PATH_DEBUG = "%s/%s_debug.log" % (log_path,log_name)
    LOG_PATH_DAILY = "%s/%s_daily.log" % (log_path,log_name)
    LOG_PATH_ERROR = "%s/%s_error.log" % (log_path,log_name)
    #������־�ļ�������С
    LOG_FILE_MAX_BYTES = 60 * 1024 * 1024
    #��־�ļ�����
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
    LOG_FILE_MAX_BYTES = 102400000 #������־�ļ�������С
    LOG_DAILY_COUNT = 30 # ÿ��log 30��
    LOG_FILE_BACKUP_COUNT = 7 #��־�ļ�����
    
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
    
    #��¼��Ϣ����ع�
    dailyHandler = logging.handlers.TimedRotatingFileHandler(LOG_PATH_DAILY,
                                                             'midnight',
                                                             backupCount = LOG_DAILY_COUNT)
    dailyHandler.setLevel(logging.INFO)
    
    #����������Ϣ���ļ���С(100M)�ع�
    errorHandler = logging.handlers.RotatingFileHandler(LOG_PATH_ERROR,
                                                        maxBytes=LOG_FILE_MAX_BYTES,
                                                        backupCount=LOG_FILE_BACKUP_COUNT)
    errorHandler.setLevel(logging.ERROR)
    
    #����������Ϣ���ļ���С(100M)�ع�
    debugHandler = logging.handlers.RotatingFileHandler(LOG_PATH_DEBUG,
                                                        maxBytes=LOG_FILE_MAX_BYTES,
                                                        backupCount=LOG_FILE_BACKUP_COUNT)
    debugHandler.setLevel(LOG_LEVEL)
    
    #��־��ʽ
    formatter = logging.Formatter(
        '%(asctime)-15s [%(thread)d] - [%(filename)s %(lineno)d] %(levelname)s %(message)s'
    )
    dailyHandler.setFormatter(formatter)
    debugHandler.setFormatter(formatter)
    errorHandler.setFormatter(formatter)
    
    #logger����
    logger_daily = logging.getLogger(LOG_PATH_DAILY)
    logger_daily.setLevel(logging.INFO)
    logger_daily.addHandler(dailyHandler)
    
    logger_error = logging.getLogger(LOG_PATH_ERROR)
    logger_error.setLevel(logging.ERROR)
    logger_error.addHandler(errorHandler)
    
    logger_debug = logging.getLogger(LOG_PATH_DEBUG)
    logger_debug.setLevel(LOG_LEVEL)
    logger_debug.addHandler(debugHandler)
    
    #TODO �������loggerʧ����Ҫ���?
    return logger_debug,logger_daily,logger_error
    
    
def close_log():
    logging.shutdown()

