import logging
from logging import Formatter, FileHandler
from flask import Flask
import time

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)  
        return cls._instance  
class LogInfo(Singleton):  
    logInfo = None

    def init_log(self,app):
        log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
        file_handler = FileHandler(log_file_name)
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
        