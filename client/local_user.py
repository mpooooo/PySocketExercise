#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import socket
import logging
import time
import threading

class LocalUser(object):
	
	__instance = None

	def __init__(self):
		self.user_id = None
		self.nick_name = None
		self.handler = None
		self._pos_rom = 'hall'
		self.created_rooms = []
		self._json_key_user_id = 'User_Id'
		self._json_key_user_nick_name = 'User_Nick_Name'

	@classmethod
	def getInstance(cls):
		if(cls.__instance == None):
			cls.__instance = LocalUser()
		return cls.__instance

	def setUserId(self, user_id):
		self.user_id = user_id
		self.nick_name = user_id

	def getUserId(self):
		return self.user_id
		
	def setNickName(self, nick_name):
		self.nick_name = nick_name

	def getRoomPlace(self):
		return self._pos_rom

	def setRoomPlace(self, room_name):
		self._pos_rom = room_name

	def setHandler(self, handler):
		self.handler = handler

	def printStstus(self):
		print "User Id: {0} \nUser in {1} Room".format(self.user_id, self._pos_rom)

	def getUserInfo(self):
		user_info = {}
		if self.user_id:
			user_info.update({self._json_key_user_id: self.user_id, self._json_key_user_nick_name: self.nick_name})
		return user_info