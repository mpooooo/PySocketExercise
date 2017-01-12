#!/usr/bin/env python2.7
#coding=utf-8
import os, sys
import logging

class ServerLogger(object):
    '''
       @summary:日志处理对象,对logging的封装
    '''
    def __init__(self, name = 'Logger'):
        self.logger = logging.getLogger(name)
        self.log_file = 'server.log'
        self.initConsoleLogger()
        self.initFileLogger()
        self.logger.setLevel(logging.DEBUG)

    def initFileLogger(self):
        file_hander = logging.FileHandler(self.log_file)
        formatter = logging.Formatter("[%(levelname)s  %(threadName)s(%(thread)d)] [%(asctime)s %(myfn)s:%(mylno)d:%(myfunc)s] %(message)s", 
                                    datefmt = "%y-%m-%d %H:%M:%S")
        file_hander.setFormatter(formatter)
        file_hander.setLevel(logging.DEBUG)
        self.logger.addHandler(file_hander)

    def initConsoleLogger(self): 
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s %(threadName)s(%(thread)d)] [%(asctime)s %(myfn)s:%(mylno)d:%(myfunc)s%(mymodule)s] %(message)s", 
                                    datefmt = "%y-%m-%d %H:%M:%S",
                                    )
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)
 
    def updateKwargs(self, kwargs):
        try:
            fn, lno, func = self.logger.findCaller()
            fn = os.path.basename(fn)
        except Exception as ddd:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
 
        if not "extra" in kwargs:
            kwargs["extra"] = {}
 
        kwargs["extra"]["myfn"] = fn
        kwargs["extra"]["mylno"] = lno
        kwargs["extra"]["myfunc"] = func
        kwargs["extra"]["mymodule"] = ""
 
    def debug(self, msg, *args, **kwargs):
        self.updateKwargs(kwargs)
        self.logger.debug(msg, *args, **kwargs)
 
    def info(self, msg, *args, **kwargs):
        self.updateKwargs(kwargs)
        self.logger.info(msg, *args, **kwargs)
 
    def warning(self, msg, *args, **kwargs):
        self.updateKwargs(kwargs)
        self.logger.warning(msg, *args, **kwargs)
 
    def error(self, msg, *args, **kwargs):
        self.updateKwargs(kwargs)
        self.logger.error(msg, *args, **kwargs)
 
    def critical(self, msg, *args, **kwargs):
        self.updateKwargs(kwargs)
        self.logger.critical(msg, *args, **kwargs)

logger = ServerLogger()

# if __name__ == '__main__':
#     logger.info('hello')