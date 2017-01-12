#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import abc
from event_handle import EventHandler
from sock_handle import SockHandle
from reactor import Reactor
from event import Event
sys.path.append('../')
from server_logger import logger

class ListenHandle(EventHandler):

    """docstring for ListenHandle"""
    
    def __init__(self, fd):
        super(ListenHandle, self).__init__()
        self._listen_fd = fd
        self._data = str()
        self._max_size = 1024

    def __del__(self):
        super(ListenHandle, self).__del__()
        self._listen_fd.close()

    def getHandle(self):
        return self._listen_fd.fileno()

    def handleRead(self):
        conn, addr = self._listen_fd.accept()
        logger.info("Listen Handler get a new address: %s connected", addr)
        conn.setblocking(0)  
        hander = SockHandle(conn);
        rector = Reactor.getInstance();
        rector.regist(hander, Event.ReadEvent);

    def handleWrite(self):
        pass

    def handleError(self):
        reactor = Reactor.getInstance()
        reactor.remove(self)
        self._listen_fd.close()