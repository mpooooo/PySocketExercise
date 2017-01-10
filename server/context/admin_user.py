#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import time
import threading 
from context import Context

class AdminUser(object):
	
	__instance = None
	lock = threading.RLock()

	def __init__(self):
		self.user_id = 'Admin'

	@classmethod
	def getInstance(cls):
		cls.lock.acquire()
		if(cls.__instance == None):
			cls.__instance = AdminUser()
		cls.lock.release()
		return cls.__instance 