#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import socket
import signal
from reactor.event import Event
from reactor.reactor import Reactor
from reactor.listen_handle import ListenHandle
from context.hall import Hall
from server_logger import logger
try:
    import stacktracer 
    stacktracer.trace_start("trace.html")
except:
    pass

host = '127.0.0.2'
port = 2003

class Server(object):

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._listen_fd = None

    def create(self):
        try:
            self._listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            logger.info('Server create socket fd success.')
        except socket.error, msg:
            logger.error("Server create socket failed, the error msg : %s.",msg)
            raise socket.error
        try:
            self._listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            logger.info('Server set sock opt success')
        except socket.error, msg:
            logger.error("setsocketopt SO_REUSEADDR failed")
            raise socket.error

    def bind(self):
        try:
            self._listen_fd.bind((self._host, self._port))
            logger.info('Server bind host %s port %s success.',self._host, self._port)
        except socket.error, msg:
            logger.error("Server bind host %s port %s failed, the msg: %s.",self._host, self._port, msg)
            raise socket.error


    def listen(self, max_listen = 100):
        try:
            self._listen_fd.listen(max_listen)
            logger.info('Server set max listen [%d] success.', max_listen)
        except socket.error, msg:
            logger.error('Server set max listen [%d] failed, the msg: %s.', max_listen, msg)
            raise socket.error

    def getFileDescriptor(self):
        return self._listen_fd

    def getHost(self):
        return self._host

    def getPort(self):
        return self._port

def quit(signum, frame):
    logger.info('server closing...')
    reactor = Reactor.getInstance()
    reactor.close()
    sys.exit()
    
if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    server = Server(host, port)
    server.create()
    server.bind()
    server.listen()

    reactor = Reactor.getInstance()
    handle = ListenHandle(server.getFileDescriptor())
    reactor.regist(handle, Event.ReadEvent)
    
    hall = Hall.getInstance()
    hall.create()

    while True: 
        reactor.eventLoop(-1)