#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
from event import Event
from epoll_demultiplexer import EpollDemultiplexer
sys.path.append('../')
from server_logger import logger

class ReactorImplementation(object):

    def __init__(self):
        self.demultiplexer = EpollDemultiplexer()
        self.handers_dict = dict()

    def __del__(self):
        del self.demultiplexer
        del self.handers_dict

    def getHandlerDict(self):
        return self.handers_dict

    def regist(self, event_handler,  event):
        handle = event_handler.getHandle()
        logger.info("Reactor register handle key: %s, hander value: %s, hander type: %s.",
                    handle, event_handler, type(event_handler))
        if not self.handers_dict.has_key(handle):
            self.handers_dict[handle] = event_handler
            logger.info('Reactor handlers dict add key: %s, value: %s', handle, event_handler)
        else:
            logger.info("Reactor handler dict has handle key.")
        logger.info("Reactor handler dict is: %s.", self.handers_dict)
        return self.demultiplexer.regist(handle, event)

    def remove(self, event_handler):
        handle = event_handler.getHandle()
        logger.info("Reactor remove handle key: %s, hander value: %s, hander type: %s.",
                    handle, event_handler, type(event_handler))
        if self.handers_dict.has_key(handle):
            logger.info("Reactor remove dict key: %s, value: %s.",handle, self.handers_dict[handle])
            del self.handers_dict[handle]
        else:
            logger.error("Reactor removing dict key_value pair, but can not find the key: %s.",handle)
            return False
        logger.info("Reactor handler dict is: %s.", self.handers_dict)
        return self.demultiplexer.remove(handle)

    def modify(self, event_handler, event):
        handle = event_handler.getHandle()
        logger.info("Reactor modify handle key: %s, hander value: %s, hander type: %s.",
                    handle, event_handler, type(event_handler))
        if not self.handers_dict.has_key(handle):
            logger.error("Reactor modify dict key_value pair, but can not find the key: %s.",handle)
            return False
        return self.demultiplexer.modify(handle, event)

    def eventLoop(self,timeout = 0):
        self.demultiplexer.waitEvent(self.handers_dict, timeout)