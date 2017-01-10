#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import sqlite3 as db
import time
import ConfigParser
from sqlite_interface import SqliteInterface
USER_CONFIG_PATH = './sqlite_db/db.conf'
#USER_CONFIG_PATH = '../sqlite_db/db.conf'

USER_SECTION = 'user_db'

class UserInterface(object):
	
	def __init__(self):
		self._conf_path = USER_CONFIG_PATH
		self._user_section = USER_SECTION
		self._extractKeyFromConf(self._conf_path, self._user_section)
		self.dbpath = self._getConfig(self._conf_path, self._user_section, 'path')
		self.table_name = self._getConfig(self._conf_path, self._user_section, 'table_name')
		self.sqlite_interface = SqliteInterface(self.dbpath)
		self.sqlite_interface.connectDataBase()
		self.sqlite_interface.createTable(self.table_name, self.table_info)

	def __del__(self):
		if self.sqlite_interface.getConnection():
			self.sqlite_interface.closeConnection()
		del self.sqlite_interface

	def userExist(self, user_id):
		# select_tuple = (self.key_user_id, '=', user_id, '')
		ret_code, ret_data = self.getUserInfo(user_id, [self.key_user_id])
		return ret_code

	def addNewUser(self, user_id, user_nick_name, user_pass_word, user_status):
		cols = [self.key_user_id, self.key_register_time, self.key_user_nick_name, self.key_user_pass_word,
		 		  self.key_user_status]
		values = [user_id, time.time(), user_nick_name, user_pass_word, user_status]
		ret_code = self.sqlite_interface.insert(self.table_name, cols, values)
		return ret_code

	def getUserStatus(self, user_id):
		ret_code, ret_data = self.getUserInfo(user_id, [self.key_user_status])
		if ret_data is not None:
			ret_data = ret_data[self.key_user_status]
		return ret_code, ret_data

	def getUserPassWords(self, user_id):
		ret_code, ret_data = self.getUserInfo(user_id, [self.key_user_pass_word])
		if ret_data is not None:
			ret_data = ret_data[self.key_user_pass_word]
		return ret_code, ret_data

	def getUserNickName(self, user_id):
		ret_code, ret_data = self.getUserInfo(user_id, [self.key_user_nick_name])
		if ret_data is not None:
			ret_data = ret_data[self.key_user_nick_name]
		return ret_code, ret_data

	def getUserLoginTime(self, user_id):
		ret_code, ret_data = self.getUserInfo(user_id, [self.key_login_time])
		if ret_data is not None:
			ret_data = ret_data[self.key_login_time]
		return ret_code, ret_data
		
	def getUserInfo(self, user_id, ret_col = ['*']):
		select_tuple = (self.key_user_id, '=', user_id, '')
		ret_code, ret_data = self.sqlite_interface.fetchOne(self.table_name, [select_tuple, ], ret_col)
		#print "Fetch %s, %s"%(ret_code, ret_data)
		return ret_code, ret_data

	def updateLoginStatus(self, user_id, status):
		login_tuple = (self.key_user_status, status)
		condition_tuple = (self.key_user_id, '=', user_id, '')
		ret_code = self.sqlite_interface.update(self.table_name, [login_tuple], [condition_tuple])
		return ret_code
	
	def updateLoginTime(self, user_id, update_time):
		login_tuple = (self.key_login_time, update_time)
		condition_tuple = (self.key_user_id, '=', user_id, '')
		
		ret_code = self.sqlite_interface.update(self.table_name, [login_tuple], [condition_tuple])
		return ret_code

	def updateOnlineTime(self, user_id, online_time):
		online_tuple = (self.key_online_time , online_time)
		condition_tuple = (self.key_user_id, '=', user_id, '')
		ret_code = self.sqlite_interface.update(self.table_name, [online_tuple], [condition_tuple])
		return ret_code

	def _extractKeyFromConf(self, conf_path, section):
		self.table_info = eval(self._getConfig(conf_path, section, 'table_info'))
		self.key_user_id, self.type_user_id = 'User_Id', self.table_info['User_Id']
		self.key_register_time, self.type_register_time = 'Register_Time', self.table_info['Register_Time']
		self.key_login_time, self.type_login_time = 'Login_Time', self.table_info['Login_Time']
		self.key_last_online_time, self.type_last_online_time = 'Last_Oline_Time', self.table_info['Last_Oline_Time']
		self.key_user_nick_name, self.type_user_nick_name = 'User_Nick_Name', self.table_info['User_Nick_Name']
		self.key_user_pass_word, self.type_user_pass_word = 'User_Pass_Word', self.table_info['User_Pass_Word']
		self.key_online_time, self.type_online_time = 'Online_Time', self.table_info['Online_Time']
		self.key_user_status, self.type_user_status = 'User_Status', self.table_info['User_Status']

	def _getConfig(self, path, section, key):
	    config = ConfigParser.ConfigParser()
	    config.read(USER_CONFIG_PATH)
	    return config.get(section, key)

if __name__ == '__main__':
	ui = UserInterface()
	#print ui.table_info
	#print ui.userExist('hywwqq')
	#print ui.addNewUser('hywwqq', 'hywwqq', '123455', 'offline')
	#print ui.userExist('hywwqq')
	#print ui.getUserPassWords('hywwqq')
	#print ui.updataLoginTime('hywwqq')
	#print ui.getUserInfo('hywwqq')
	#print ui.updataLoginTime('hywwqq')
	#print ui.getUserInfo('hywwqq')


