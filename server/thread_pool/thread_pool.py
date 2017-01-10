#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import threading
from worker_task import WorkerTask
from worker_thread import WorkerThread
  
class ThreadPool(object):    
    def __init__(self, max_pool_size=10):  
        self.max_pool_size = max_pool_size  
        self._threads = []  
        self._tasks = []   
  
    def _addTask(self, task):  
        self._tasks.append(task)  
  
        worker_thread = None  
        for thread in self._threads:  
            if thread.busy is False:  
                worker_thread = thread  
                break  
  
        if worker_thread is None and len(self._threads) <= self.max_pool_size:  
            worker_thread = WorkerThread(self)  
            self._threads.append(worker_thread)  
  
        if worker_thread is not None:  
            worker_thread.work()  
  
    def addTask(self, function, args=(), kwargs={}):  
        self._addTask(WorkerTask(function, args, kwargs))  
