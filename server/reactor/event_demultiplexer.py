#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import abc

class EventDemultiplexer(object):

    def __init__(self):
        pass

    @abc.abstractmethod
    def waitEvent(self, handlers_dict, timeout = 0):
        pass

    @abc.abstractmethod
    def regist(self, handle, event):
        pass

    @abc.abstractmethod
    def remove(self, handle):
        pass

    def __del__(self):
        pass