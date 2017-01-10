#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import select
from event import Event
sys.path.append('../')
from server_logger import logger
from event_demultiplexer import EventDemultiplexer

class EpollDemultiplexer(EventDemultiplexer):

    def __init__(self):
        super(EpollDemultiplexer, self).__init__()
        self._max_fd = 0
        self._epoll_fd = select.epoll()

    def __del__(self):
        super(EpollDemultiplexer, self).__del__()

    def waitEvent(self, handlers_dict, timeout = 10):
        epoll_list = self._epoll_fd.poll(timeout)
        logger.info("Epoll Demultiplexer is waiting event: %s.", epoll_list)
        for fd, event in epoll_list:
            if (select.POLLERR | select.POLLNVAL) & event:
                (handlers_dict[fd]).handleError()
            elif (select.POLLIN | select.POLLPRI) & event:
                (handlers_dict[fd]).handleRead()
            elif select.EPOLLOUT & event:
                (handlers_dict[fd]).handleWrite()
            else:
                pass
        
        return len(epoll_list)

    def regist(self, handle, event): 
        if event & Event.ReadEvent:
            event = event | select.EPOLLIN
        if event & Event.WriteEvent:
            event = event | select.EPOLLOUT
        event = event | select.EPOLLET
        try:
            self._epoll_fd.register(handle, event)
            logger.info("Epoll Demultiplexer register new handle: %s, event: %s success", handle, event)
            self._max_fd += 1
        except IOError, e:
            logger.error('Epoll Demultiplexer register handle: %s error', handle)
            return False
        return True

    def modify(self, handle, event):
        if event & Event.ReadEvent:
            event = event | select.EPOLLIN
        if event & Event.WriteEvent:
            event = event | select.EPOLLOUT
        event = event | select.EPOLLET
        try:
            self._epoll_fd.modify(handle, event)
            logger.info('Epoll Demultiplexer modify handle: %s to event: %s success', handle, event)
        except IOError, e:
            logger.error('Epoll Demultiplexer modify handle: %s to event: %s error', handle, event)
            return False
        return True

    def remove(self, handle):
        try:
            self._epoll_fd.unregister(handle)
            logger.info("Epoll Demultiplexer remove handle: %s success", handle)
            self._max_fd -= 1
        except IOError, e:
            logger.error('Epoll Demultiplexer unregister handle: %s error', handle)
            return False
        return True