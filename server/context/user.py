#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import time
from hall import Hall
import threading
from context import Context
import time, datetime
sys.path.append('..')
from sqlite_db import db_operation
from sqlite_db.user_interface import UserInterface
from admin_user import AdminUser
from server_logger import logger

class User(object):

    __instance = None
    lock = threading.RLock()

    def __init__(self, user_id, user_nick_name):
        self._user_id = user_id
        self.nick_name = user_nick_name
        self._pass_word = None
        self._telecom_handler = None
        self._last_online_time = None
        self._db_interface = None
        self.key_offline = 'offline'
        self.key_online = 'online'

    def __del__(self):
        del self._db_interface

    @classmethod
    def getInstance(cls, user_id, user_nick_name):
        cls.lock.acquire()
        if cls.__instance == None  or (not cls.__instance.user_id == user_id):
            #or (not cls.__instance._telecom_handler == handler and cls.__instance.user_id == user_id):
            cls.__instance = User(user_id, user_nick_name)
        cls.lock.release()
        return cls.__instance

    @property
    def user_id(self):
        return self._user_id
    
    @property
    def telecom_handler(self):
        return self._telecom_handler

    @telecom_handler.setter
    def telecom_handler(self, handler):
        self._telecom_handler = handler

    @property
    def pass_word(self, pass_word):
        self._pass_word = pass_word
    
    @pass_word.setter
    def pass_word(self, pass_word):
        self._pass_word = pass_word

    def register(self):
        logger.info('user register, user_id:[%s], user_passwords:[%s]', self.user_id, self._pass_word)
        if not self._db_interface:
            self._db_interface = UserInterface()
        ret_code, ret_data = True, str()
        if not self._pass_word:
            ret_code = False
            ret_data = 'register failed with empty pass words.'
        elif self._db_interface.userExist(self.user_id):
            ret_code = False
            ret_data = "User has already registered."
        elif self._db_interface.addNewUser(self.user_id, self.nick_name, self._pass_word, self.key_offline):
            ret_data = "User registered complete."
        else:
            ret_code = False
            ret_data = 'User register error, please retry.'
        logger.info('user registerd finish with [%s: %s]', ret_code, ret_data)
        return ret_code, ret_data

    def login(self, socket_handler):
        if not self._db_interface:
            self._db_interface = UserInterface()
        logger.info('user login, user_id:[%s], user_passwords:[%s]', self.user_id, self._pass_word)
        ret_code, ret_data = True, str()
        password_ret_code, pass_word = self._db_interface.getUserPassWords(self.user_id)
        status_ret_code, status = self._db_interface.getUserStatus(self.user_id)
        if password_ret_code:
            if pass_word == self._pass_word and status == self.key_offline:
                ret, info_dict = self._db_interface.getUserInfo(self.user_id, 
                            [self._db_interface.key_login_time, self._db_interface.key_online_time])
                last_login_time = info_dict[self._db_interface.key_login_time]
                online_time = info_dict[self._db_interface.key_online_time]
                logger.info('user login success, last login time [%s], online time [%s].', last_login_time, online_time)
                ret_data = 'login success.'
                if online_time is None:
                    online_time = 0
                self._db_interface.updateLoginStatus(self.user_id, self.key_online)
                self._db_interface.updateLoginTime(self.user_id, time.time())
                self.telecom_handler = socket_handler
                self.receiveMessage({'System_Message':'online time :'+str(int(online_time))+' seconds'})
            elif pass_word == self._pass_word and status == self.key_online:
                ret_code = False
                ret_data = 'user has been login'
            else:
                ret_code = False
                ret_data = 'login failed with wrong pass word.'
        else:
            ret_code = False;
            ret_data = 'login with unknown account.'
        logger.info('user login finish with [%s: %s]', ret_code, ret_data)
        return ret_code, ret_data

    def receiveMessage(self, message_dict):
        logger.info('user[%s] receive message[%s] to transport back.', self.user_id, message_dict)
        self._telecom_handler.asynRetData(str(message_dict))

    def getOnlineTime(self):
        if not self._db_interface:
            self._db_interface = UserInterface()
        now_time = time.time()
        ret_code, info_dict = self._db_interface.getUserInfo(self.user_id, 
                            [self._db_interface.key_login_time, self._db_interface.key_online_time])
        online_time = None
        if ret_code:
            login_time = info_dict[self._db_interface.key_login_time]
            online_time = info_dict[self._db_interface.key_online_time]
            if not online_time:
                online_time = now_time - login_time
            else:
                online_time += now_time - login_time
        return online_time

    def logout(self):
        if not self._db_interface:
            self._db_interface = UserInterface()
        ret_code, ret_data = False, str()
        logger.info('user logout, user_id:[%s]', self.user_id)
        status_ret_code, status = self._db_interface.getUserStatus(self.user_id)
        if status == self.key_offline:
            ret_code, ret_data = False, 'already offline'
        else:
            self._db_interface.updateLoginStatus(self.user_id, self.key_offline)
            self._db_interface.updateOnlineTime(self.user_id, self.getOnlineTime())
            ret_code, ret_data = True, 'logout success'
        logger.info('user logout finish with [%s: %s]', ret_code, ret_data)
        return ret_code, ret_data