#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import socket
import logging
import time
import threading
from local_user import LocalUser

class MessageParser(object):

	def __init__(self):
		self.token = list()
		self.message = None
		self.operate_type = None
		self.json_dct = dict()
		self.operate = None
		self._message_key_init()
		self._josn_key_init()

	def parse(self, user_input):
		self.json_dct = {}
		self.operate = None
		msg_list = user_input.strip().split(' ', 1)
		self.operate = msg_list[0]
		if len(msg_list) == 2:
			self.message = msg_list[1]
		if self._parseRegister():
			return self.json_dct
		elif self._parseLogin():
			return self.json_dct
		elif self._parseLogout():
			return self.json_dct()
		elif self._parseChat():
			return self.json_dct
		elif self._parseRoomCreate():
			return self.json_dct
		elif self._parseRoomInvite():
			return self.json_dct
		elif self._parseRoomEnter():
			return self.json_dct
		elif self._parseRoomLeave():
			return self.json_dct
		elif self._parseGame():
			return self.json_dct
		else:
			return self.json_dct

	def _parseGame(self):
		if self.operate == self.msg_key_operate_21game:
			self.json_dct.update({self.json_key_operate: self.json_key_operate_game})
			msg_txt = self.message
			msg_to = self.operate.capitalize()
			user = LocalUser.getInstance()
			usr_info = user.getUserInfo()
			self.json_dct.update({self.json_key_user:usr_info})
			self.json_dct.update({self.json_key_message:{\
						   self.json_key_message_id: user.user_id + '@' + str(time.time()),
						   self.json_key_message_from: usr_info[self.json_key_user_id],
						   self.json_key_message_to: msg_to,
						   self.json_key_message_text: msg_txt,
						}
					})
			return True
		return False

	def _parseRoomLeave(self):
		if self.operate == self.msg_key_operate_room:
			msg_list = self.message.split(' ', 1)
			action = msg_list[0]
			if action == self.msg_key_operate_leave:
				self.json_dct.update({self.json_key_operate: self.json_key_operate_room_leave})
				user = LocalUser.getInstance()
				usr_info = user.getUserInfo()
				self.json_dct.update({self.json_key_user:usr_info})
				room_id = str()
				user = LocalUser.getInstance()
				room_id = user.getRoomPlace()
				self.json_dct.update({self.json_key_room: {self.json_key_room_id: room_id}})
				self.json_dct.update({self.json_key_message:{\
						   self.json_key_message_id: user.user_id + '@' + str(time.time()),
						   self.json_key_message_from: usr_info[self.json_key_user_id],
						   self.json_key_message_to: None,
						   self.json_key_message_text: None,
						}
					})
				return True
		return False

	def _parseRoomEnter(self):
		if self.operate == self.msg_key_operate_room:
			msg_list = self.message.split(' ', 2)
			action = msg_list[0]
			if action == self.msg_key_operate_enter and len(msg_list) == 2:
				self.json_dct.update({self.json_key_operate: self.json_key_operate_room_enter})
				user = LocalUser.getInstance()
				usr_info = user.getUserInfo()
				self.json_dct.update({self.json_key_user:usr_info})
				room_id = str()
				if not '#' in msg_list[1]:
					room_id = usr_info[self.json_key_user_id] + '#' + msg_list[1].strip('[]')
				else:
					room_id = msg_list[1].strip('[]')
				self.json_dct.update({self.json_key_room: {self.json_key_room_id: room_id}})
				self.json_dct.update({self.json_key_message:{\
						   self.json_key_message_id: user.user_id + '@' + str(time.time()),
						   self.json_key_message_from: usr_info[self.json_key_user_id],
						   self.json_key_message_to: None,
						   self.json_key_message_text: None,
						}
					})
				return True
		return False

	def _parseRoomInvite(self):
		if self.operate == self.msg_key_operate_room:
			msg_list = self.message.split(' ', 1)
			action = msg_list[0]
			if action == self.msg_key_operate_invite and len(msg_list) == 2:
				self.json_dct.update({self.json_key_operate: self.json_key_operate_room_invite})
				user = LocalUser.getInstance()
				usr_info = user.getUserInfo()
				self.json_dct.update({self.json_key_user:usr_info})
				user = LocalUser.getInstance()
				room_id = user.getRoomPlace()
				self.json_dct.update({self.json_key_room: {self.json_key_room_id: room_id}})
				self.json_dct.update({self.json_key_message:{\
						   self.json_key_message_id: user.user_id + '@' + str(time.time()),
						   self.json_key_message_from: usr_info[self.json_key_user_id],
						   self.json_key_message_to: None,
						   self.json_key_message_text: msg_list[1],
						}
					})
				return True
		return False

	def _parseRoomCreate(self):
		if self.operate == self.msg_key_operate_room:
			msg_list = self.message.split(' ', 1)
			action = msg_list[0]
			if action == self.msg_key_operate_create:
				self.json_dct.update({self.json_key_operate: self.json_key_operate_room_create})
				user = LocalUser.getInstance()
				usr_info = user.getUserInfo()
				self.json_dct.update({self.json_key_user:usr_info})
				room_id = usr_info[self.json_key_user_id] + '#' + msg_list[1]
				self.json_dct.update({self.json_key_room: {self.json_key_room_id: room_id}})
				self.json_dct.update({self.json_key_message:{\
						   self.json_key_message_id: user.user_id + '@' + str(time.time()),
						   self.json_key_message_from: None,
						   self.json_key_message_to: None,
						   self.json_key_message_text: None,
						}
					})
				return True
		return False

	def _parseChat(self):
		if self.operate == self.msg_key_operate_chat:
			user = LocalUser.getInstance()
			usr_info = user.getUserInfo()
			msg_list = self.message.split(' ', 1)
			if usr_info and len(msg_list) >= 1:
				self.json_dct.update({self.json_key_operate: self.json_key_operate_message_send})
				msg_to = None
				if msg_list[0].startswith('[') and msg_list[0].endswith(']'):
					msg_to = msg_list[0].strip('[]')
					msg_txt = msg_list[1]
				else:
					msg_to = user.getRoomPlace()
					msg_txt = self.message
				self.json_dct.update({self.json_key_user:usr_info})
				msg_dct = {}
				msg_dct.update({self.json_key_message:{\
						   self.json_key_message_id: user.user_id + '@' + str(time.time()),
						   self.json_key_message_from: usr_info[self.json_key_user_id],
						   self.json_key_message_to: msg_to,
						   self.json_key_message_text: msg_txt,
						}
					})
				self.json_dct.update(msg_dct)
				return True
		return False

	def _parseLogout(self):
		if self.operate == self.msg_key_operate_logout:
			usr_info = user.getUserInfo()
			if usr_info:
				self.json_dct.update({self.json_key_operate: self.json_key_operate_logout})
				self.json_dct.update({self.json_key_user:usr_info})
				return True
		else:
			return False

	def _parseLogin(self):
		if self.operate == self.msg_key_operate_login:
			msg_list = self.message.split(' ', 1)
			if len(msg_list) < 2:
				return False 
			self.json_dct.update({self.json_key_operate: self.json_key_operate_login})
			account_name = msg_list[0]
			account_pass_word = msg_list[1]
			user = {}
			user.update({self.json_key_user:{\
						self.json_key_user_id: account_name,
						self.json_key_user_nick_name: account_name,
						self.json_key_user_pass_word: account_pass_word
					}
				})
			self.json_dct.update(user)
			return True
		return False

	def _parseRegister(self):
		if self.operate == self.msg_key_operate_register:
			msg_list = self.message.split(' ', 1)
			if len(msg_list) < 2:
				return False 
			self.json_dct.update({self.json_key_operate: self.json_key_operate_register})
			account_name = msg_list[0]
			account_pass_word = msg_list[1]
			user = {}
			user.update({self.json_key_user:{\
						self.json_key_user_id: account_name,
						self.json_key_user_nick_name: account_name,
						self.json_key_user_pass_word: account_pass_word
					}
				})
			self.json_dct.update(user)
			return True
		return False

	def _josn_key_init(self):
		self.json_key_operate = 'Operate'
		self.json_key_operate_register = 'Register'
		self.json_key_operate_login = 'Login'
		self.json_key_operate_logout = 'Logout'
		self.json_key_operate_message_send = 'Message_Send'
		self.json_key_operate_room_create = 'Room_Create'
		self.json_key_operate_room_invite = 'Room_Invite'
		self.json_key_operate_room_enter = 'Room_Enter'
		self.json_key_operate_room_leave = 'Room_Leave'
		self.json_key_operate_game = 'Game'
		
		self.json_key_user = 'User'
		self.json_key_user_id = 'User_Id'
		self.json_key_user_nick_name = 'User_Nick_Name'
		self.json_key_user_pass_word = 'User_Pass_Word'

		self.json_key_message = 'Message'
		self.json_key_message_id = 'Message_Id'
		self.json_key_message_from = 'Message_From'
		self.json_key_message_to = 'Message_To'
		self.json_key_message_text = 'Message_Text'

		self.json_key_room = 'Room'
		self.json_key_room_id = 'Room_Id'

	def _message_key_init(self):
		self.msg_key_message = '$'
		self.msg_key_operate_chat = 'chat'
		self.msg_key_operate_create = 'create'
		self.msg_key_operate_room = 'room'
		self.msg_key_operate_invite = 'invite'	
		self.msg_key_operate_enter = 'enter'
		self.msg_key_operate_leave = 'leave'
		self.msg_key_operate_register = 'register'
		self.msg_key_operate_login = 'login'
		self.msg_key_operate_logout = 'logout'
		self.msg_key_operate_21game = '21game'