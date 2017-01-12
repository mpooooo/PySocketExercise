#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import abc
import socket
import errno
from event_handle import EventHandler
from reactor import Reactor
from event import Event
import threading
sys.path.append('../')
from server_logger import logger


class SockHandle(EventHandler):

    """docstring for SockHandle"""
    
    def __init__(self, fd):
        super(SockHandle, self).__init__()
        self._socket_fd = fd
        self.received_data = str()
        self._ret_data = []
        self._max_size = 1024
        self.rlock = threading.RLock()

    def __del__(self):
        super(SockHandle, self).__del__()
        self._socket_fd.close()

    def getHandler(self):
        return self._socket_fd

    def getHandle(self):
        return self._socket_fd.fileno()

    def handleRead(self):
        logger.info("Socket Hander start reading data...")
        reactor = Reactor.getInstance()
        datas = str()
        while True:
            try:
                data = self._socket_fd.recv(1024)
                if not data and not datas:
                    logger.warning('Socket recv 0 size data, client abort.')
                    reactor.remove(self)
                    self._socket_fd.close()
                    break
                else:
                    datas += data
            except socket.error, msg:
                if msg.errno == errno.EAGAIN:
                    logger.info("Socket [handle:%s, handler:%s] receive data: %s", self._socket_fd.fileno(),
                                self._socket_fd, datas)
                    self.received_data = datas
                    reactor.controller.distribute(self)
                    break

                else:
                    logger.error("Socket receive data failed.")
                    reactor.remove(self)
                    self._socket_fd.close()
                    logger.error(msg)
                    break
        pass

    def asynRetData(self, ret_data):
        self.rlock.acquire()
        logger.info("Socket Async process finish, ret data: %s .", ret_data)
        reactor = Reactor.getInstance()
        self._ret_data.append(ret_data)
        reactor.modify(self, Event.WriteEvent)
        self.rlock.release()

    def handleWrite(self):
        self.rlock.acquire()
        send_len = 0 
        peer_ip, peer_port = self._socket_fd.getpeername()
        write_data = str(self._ret_data)
        reactor = Reactor.getInstance()
        logger.info("Socket write data: %s to %s : %s...", write_data, peer_ip, peer_port)       
        while True:
            try:
                send_len += self._socket_fd.send(write_data[send_len:])
            except socket.error, msg:
                logger.error("Socket write to ip %s, port %s failed.",peer_ip, peer_port)
                reactor.remove(self)
                self._socket_fd.close()
                break
            if send_len == len(write_data):
                try:
                    reactor.modify(self, Event.ReadEvent)
                except:
                    reactor.remove(self)
                    self._socket_fd.close()
                logger.info('write finish.')
                break
        self._ret_data = []
        self.rlock.release()

    def handleError(self):
        reactor = Reactor.getInstance()
        reactor.remove(self)
        self._socket_fd.close()