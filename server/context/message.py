#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
from context import Context
sys.path.append('../')
from server_logger import logger

class Message(object):

    def __init__(self, msg_id, msg_from, msg_to, msg):
    	self.message_id = msg_id
        self.producer_id = msg_from
        self.received_text = msg
    	self.consumer_id = msg_to
    	self.message_dict = {'Message_Id': self.message_id, 'Message_From': msg_from, 'Message_Text': msg}
    	# self.message_dict = str(self.message_dict_dct)

    def messageTransport(self):
    	ret_code, ret_data = True, 'message send success.' 

    	ctx = Context.getInstance()
        online_room = ctx.getOnlineRoom()
        online_user = ctx.getOnlineUser()
        logger.info("Message trans to [%s]....", self.consumer_id)
        logger.info("Message get onlien user [%s], online room [%s].", online_user, online_room)

    	if online_user.has_key(self.consumer_id):
    		online_user[self.consumer_id].receiveMessage(self.message_dict)
        elif online_room.has_key(self.consumer_id):
            online_room[self.consumer_id].boardcast(self.message_dict, [self.producer_id, ])
        else:
            ret_code, ret_data = False, 'can not find online user or room.'
    	return ret_code, ret_data

        