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
            if dct.has_key('Ret_Code') and dct.has_key('Detail'):
                self._retMessageDistribute(dct, dct['Message_Id'])
            elif dct.has_key("Message_Text"):
                print dct['Message_Text']
            else:
                pass

    def _roomCreateOutput(self, msg_id, msg_dct):
        if msg_dct['Ret_Code'] is True:
            print 'create room success'
        else:
            print 'create failed, %s'%msg_dct['Detail']
        
    def _roomEnterOutput(self, msg_id, msg_dct):
        if msg_dct['Ret_Code'] is True:
            user = LocalUser.getInstance()
            user.setRoomPlace(self.room_enter_message[msg_id])
            del self.room_enter_message[msg_id]
            print 'enter success'
        else:
            print 'enter failed, %s'%msg_dct['Detail']


    def _roomLeaveOutput(self, msg_id, msg_dct):
        if msg_dct['Ret_Code'] is True:
            user = LocalUser.getInstance()
            user.setRoomPlace('hall')
            del self.room_leave_message[msg_id]
            print 'leave room success'
        else:
            print 'leave failed, %s'%msg_dct['Detail']


    def _chatOutput(self, msg_id, msg_dct):
        if msg_dct['Ret_Code'] is True:
            pass
        else:
            print 'message send failed.'

    def _retMessageDistribute(self, msg_dct, msg_id):
        print msg_id, msg_id in self.chat_message
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
            print msg_dct['Message_From'] +':\n' + msg_dct['Message_Text']
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
