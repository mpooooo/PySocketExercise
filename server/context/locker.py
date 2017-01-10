#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import threading

def rlock(cls):  
    def _deco(func):
        def __deco(*args, **kwargs):
            cls.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                cls.release()
        return __deco  
    return _deco

class Locker(object):

    lock = threading.RLock()

    def __init__(self):
        pass
         
    @staticmethod
    def acquire():
        Locker.lock.acquire()
         
    @staticmethod
    def release():
        Locker.lock.release()