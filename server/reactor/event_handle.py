#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import abc

class EventHandler(object):
    '''
        handle is a int data  
    '''

    def __init__(self):
        pass

    @abc.abstractmethod
    def getHandle(self):
        pass

    @abc.abstractmethod
    def handleRead(self):
        pass

    @abc.abstractmethod 
    def handleWrite(self):
        pass

    @abc.abstractmethod 
    def handleError(self):
        pass

    def __del__(self):
        pass