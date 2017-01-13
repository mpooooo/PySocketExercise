#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
from action_interface import ActionInterface
sys.path.append('../')
from thread_pool.thread_pool import ThreadPool
from context.user import User
from context.message import Message
from context.chat_room import ChatRoom
from server_logger import logger

key_operate = 'Operate'
key_user = 'User'
key_message = 'Message'
key_room = 'Room'

value_game = 'Game'
value_message_send = 'Message_Send'
value_register = 'Register'
value_login = 'Login'
value_logout = 'Logout'
value_room_create = 'Room_Create'
value_room_invite = 'Room_Invite'
value_room_enter = 'Room_Enter'
value_room_leave = 'Room_Leave'

class Controller(object):

    def __init__(self, exec_pool_size = 10):
        self._exec = None
        self._necessary_key = [key_operate, key_user]
        self._exec_thread_pool = ThreadPool(exec_pool_size)
        self.action = ActionInterface()
        self._actionMap()
        self.hander_user_map = {}
        self.gameEnginStart()

    def _actionMap(self):
        self._exec_map = {
        value_register: self.action.register,
        value_login: self.action.login,
        value_logout: self.action.logout,
        value_message_send: self.action.messageTransport,
        value_room_create: self.action.roomCreate,
        value_room_enter: self.action.roomEnter,
        value_room_leave: self.action.roomLeave,
        value_room_invite: self.action.roomInvite,
        value_game: self.action.gameMessageTransport,
        }

    def messageCheck(self, cmd_data):
        cmd_dict = dict()
        try:      
            cmd_dict = eval(cmd_data)
        except ValueError, e:
            return False, cmd_dict
        for nec_key in self._necessary_key:
            if not cmd_dict.has_key(nec_key):
                return False, cmd_dict
            else:
                pass
        return True, cmd_dict

    def extractUser(self, handler, cmd_dict):
        key_user_id = 'User_Id'
        key_user_nick_name = 'User_Nick_Name'
        key_user_pass_word = 'User_Pass_Word'
        if not cmd_dict.has_key(key_user):
            return None
        else:
            usr_dct = cmd_dict[key_user]
            pass_word = None
            usr_obj = User.getInstance(usr_dct[key_user_id], usr_dct[key_user_nick_name])
            # usr_obj.telecom_handler = handler
            if usr_dct.has_key(key_user_pass_word):
                usr_obj.pass_word = usr_dct[key_user_pass_word]
            return usr_obj

    def extractMessage(self, cmd_dict):
        key_message_id = "Message_Id"
        key_message_from = "Message_From"
        key_message_to = "Message_To"
        key_message_text = "Message_Text"
        if not cmd_dict.has_key(key_message):
            return None
        else:
            msg_dct = cmd_dict[key_message]
            msg_obj = Message(msg_dct[key_message_id], msg_dct[key_message_from], msg_dct[key_message_to], msg_dct[key_message_text])
            return msg_obj

    def extractRoom(self, cmd_dict, user):
        key_room_id = "Room_Id"
        if not cmd_dict.has_key(key_room):
            return None
        else:
            room_dct = cmd_dict[key_room]
            room_obj = ChatRoom.getInstance(room_dct[key_room_id], user)
            return room_obj

    def distribute(self, sock_handle):
        ret_data = None
        ret_code, cmd_dict = self.messageCheck(sock_handle.received_data)
        logger.info('Controller distribute received user message: %s .', sock_handle.received_data)
        if ret_code:
            usr_obj = self.extractUser(sock_handle, cmd_dict)
            self.action.setUser(usr_obj)    
            msg_obj = self.extractMessage(cmd_dict)
            self.action.setMessage(msg_obj)
            room_obj = self.extractRoom(cmd_dict, usr_obj)
            self.action.setRoom(room_obj)
            self.action.setCallback(sock_handle.asynRetData)
            self.action.setHandler(sock_handle)
            self._exec_thread_pool.addTask(self._exec_map[cmd_dict[key_operate]])
        else:
            logger.error('Controller ditribute error message: %s .', sock_handle.received_data)
            sock_handle.asynRetData({'Detail': 'message beyond rules', 'Ret_Code': False})

    def heartbeatStart(self):
        self._exec_thread_pool.addTask(self.action.heartbeatStart)

    def gameEnginStart(self):
        self._exec_thread_pool.addTask(self.action.gameEnginStart)

    def disconnect(self, sock_handle):
        self.action.disconnect(sock_handle)