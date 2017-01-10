#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import threading

class WorkerThread(threading.Thread):  
  
    def __init__(self, pool):  
        threading.Thread.__init__(self)  
        self.setDaemon(True)  
        self.pool = pool  
        self.busy = False  
        self._started = False  
        self._event = None  
  
    def work(self):  
        if self._started is True:  
            if self._event is not None and not self._event.isSet():  
                self._event.set()  
        else:  
            self._started = True  
            self.start()  
  
    def run(self):  
        while True:  
            self.busy = True  
            while len(self.pool._tasks) > 0:  
                try:  
                    task = self.pool._tasks.pop()  
                    task()  
                except IndexError:  
                    pass  
  
            self.busy = False  
            if self._event is None:  
                self._event = threading.Event()  
            else:  
                self._event.clear()  
            self._event.wait()  