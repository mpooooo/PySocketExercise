#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import socket
import logging
import time
import threading
from message_parser import MessageParser
from local_user import LocalUser
from client_logger import logger

class Action(object):

    def  __init__(self, client, user):
        self.user = user
        self.client = client
        self.parser = MessageParser()
        self.room_create_message = dict()
        self.room_enter_message = dict()
        self.room_leave_message = dict()
        self.chat_message = dict()
        self.lock = threading.RLock()
        self.key_ret_code = 'Ret_Code'
        self.key_ret_detail = 'Detail'
        self.key_system_message = 'System_Message'
        self.value_system_message = 'system message:'
        self.key_message_text = 'Message_Text'
        self.key_message_from = 'Message_From'
        self.value_message_from = 'From user id: '
        self.key_message_id = 'Message_Id'
        self.key_room_place = "Room_Place"
        self.value_room_place = 'Room id: '

    def act(self, json_message):
        operate = json_message[self.parser.json_key_operate]
        if operate == self.parser.json_key_operate_room_create:
            self.roomCreate(json_message)
        elif operate == self.parser.json_key_operate_room_enter:
            self.roomEnter(json_message)
        elif operate == self.parser.json_key_operate_room_leave:
            self.roomLeave(json_message)
        else:
            self.chat(json_message)

    def output(self, msg_list):
        for dct in msg_list:
            if dct.has_key(self.key_ret_code) and dct.has_key(self.key_ret_detail):
                self._retMessageDistribute(dct, dct[self.key_message_id])
            elif dct.has_key(self.key_system_message):
                logger.info(self.key_system_message + ':' + dct[self.key_system_message])
            elif dct.has_key(self.key_message_text):
                output_message = str()
                if dct.has_key(self.key_room_place):
                    output_message += self.value_room_place + dct[self.key_room_place] + '\n'
                if not dct[self.key_message_from] is None:
                    output_message += self.value_message_from + dct[self.key_message_from] + '\n'
                logger.info(output_message + dct[self.key_message_text])

    def _roomCreateOutput(self, msg_id, msg_dct):
        logger.info(msg_dct[self.key_ret_detail])

    def _roomEnterOutput(self, msg_id, msg_dct):
        if msg_dct[self.key_ret_code] is True:
            user = LocalUser.getInstance()
            user.setRoomPlace(self.room_enter_message[msg_id])
            del self.room_enter_message[msg_id]
        logger.info(msg_dct[self.key_ret_detail])

    def _roomLeaveOutput(self, msg_id, msg_dct):
        if msg_dct[self.key_ret_code] is True:
            user = LocalUser.getInstance()
            user.setRoomPlace('hall')
            del self.room_leave_message[msg_id]
        logger.info(msg_dct[self.key_ret_detail])

    def _chatOutput(self, msg_id, msg_dct):
        if msg_dct[self.key_ret_code] is True:
            pass
        else:
            logger.info(msg_dct[self.key_ret_detail])

    def _retMessageDistribute(self, msg_dct, msg_id):
        self.lock.acquire()
        if msg_id in self.room_create_message.keys():
            self._roomCreateOutput(msg_id, msg_dct)
        elif msg_id in self.room_enter_message.keys():
            self._roomEnterOutput(msg_id, msg_dct)
        elif msg_id in self.room_leave_message.keys():
            self._roomLeaveOutput(msg_id, msg_dct)
        elif msg_id in self.chat_message.keys():
            self._chatOutput(msg_id, msg_dct)
        else:
            pass
        self.lock.release()

    def chat(self, json_message):
        message_id = json_message[self.parser.json_key_message][self.parser.json_key_message_id]
        self.client.messageSend(str(json_message))
        self.chat_message[message_id] = json_message

    def roomCreate(self, json_message):
        message_id = json_message[self.parser.json_key_message][self.parser.json_key_message_id]
        room_id = json_message[self.parser.json_key_room][self.parser.json_key_room_id]
        self.client.messageSend(str(json_message))
        self.room_create_message[message_id] = room_id
        
    def roomEnter(self, json_message):
        message_id = json_message[self.parser.json_key_message][self.parser.json_key_message_id]
        room_id = json_message[self.parser.json_key_room][self.parser.json_key_room_id]
        self.client.messageSend(str(json_message))
        self.room_enter_message[message_id] = room_id

        # data_list = self.client.messageReveive()
        # for ret_code, ret_data in data_list:
        #     if not ret_code:
        #         print 'room create failed, %s.'%ret_data
        #     else:
        #         self.user.pos_room = room_id

    def roomLeave(self, json_message):
        message_id = json_message[self.parser.json_key_message][self.parser.json_key_message_id]
        room_id = json_message[self.parser.json_key_room][self.parser.json_key_room_id]
        self.client.messageSend(str(json_message))
        self.room_leave_message[message_id] = room_id

        # data_list = self.client.messageReveive()
        # for ret_code, ret_data in data_list:
        #     if not ret_code:
        #         print 'room create failed, %s.'%ret_data
        #     else:
        #         self.user.pos_room = 'hall'
