#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import event
import event_handle
import event_demultiplexer
from epoll_demultiplexer import EpollDemultiplexer
from reactor_impl import ReactorImplementation
from control.controller import Controller
from control.operation import Operation

class Reactor(object):

    __instance = None

    def __init__(self):
        self.impl = ReactorImplementation(); 
        self.controller = Controller()
        
    # warn
    @classmethod
    def getInstance(cls):
        if(cls.__instance == None):
            cls.__instance = Reactor()
        return cls.__instance

    def regist(self, event_handler, event):
        return self.impl.regist(event_handler, event)

    def remove(self, event_handler):
        self.controller.disconnect(event_handler)
        return self.impl.remove(event_handler)
    
    def modify(self, event_handler, event):
        return self.impl.modify(event_handler, event)

    def eventLoop(self, timeout = 0):
        return self.impl.eventLoop(timeout)
    
    def close(self):
        event_handlers = self.impl.getHandlerDict().values()
        for handler in event_handlers:
            self.controller.disconnect(handler)

if __name__ == '__main__':
     foo1 = Reactor.getInstance()
