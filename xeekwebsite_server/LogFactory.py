import logging
from logging import Formatter, FileHandler
from flask import Flask
import time

def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton

@Singleton
class LogInfo(object):  
    logger = None

    def init_log(self,app):
        self.logger = app.logger
        log_file_name = './log/logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
        #输出到文件
        file_handler = FileHandler(log_file_name,encoding='utf-8')
        #输出到控制台
        handler = logging.StreamHandler()
        
        file_handler.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(handler)
        app.logger.addHandler(file_handler)
        app.logger.info('初始化日志配置成功...')
    