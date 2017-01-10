#!/usr/bin/env python2.7
#coding=utf-8
import unittest  
import sys,os
import socket
import time
sys.path.append("../")
from message_parser import MessageParser
from client import Client

class ClientTest(unittest.TestCase): 
	'''
	'''

	def setUp(self):
		self.host = '127.0.0.2'
		self.port = 2003
		self.client = Client()

	def tearDown(self): 
		pass

	def clientTest(self):
		self.client.connectServer(self.host, self.port)

def suite(): 
	suite = unittest.TestSuite() 
	suite.addTest(ClientTest("clientTest"))
	return suite  
	
if __name__ == "__main__": 
	unittest.main(defaultTest = 'suite')