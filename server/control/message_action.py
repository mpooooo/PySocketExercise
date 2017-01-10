#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
sys.path.append('..')
from context.hall import Hall
from context.context import Context
from context.user import User

def callback(cls):  
    def _deco(func):
        def __deco(*args, **kwargs):
            ret_code, ret_data = func(*args, **kwargs)
            cls.callback(ret_code, ret_data)
        return __deco  
    return _deco

class MessageAction(object):

    callback_func = None
    message_instance = None
    
    def __init__(self, msg_obj, callback):
        MessageAction.message_instance = msg_obj
        MessageAction.callback_func = callback

    def setCallback(self, callback_func):
        MessageAction.callback_func = callback_func

    def setMessage(self, msg_obj):
        MessageAction.message_instance = msg_obj

    def getMessage(self):
        return MessageAction.message_instance

    @staticmethod
    def callback(ret_code, ret_data):
        ret_msg = dict()
        if not MessageAction.message_instance is None:
            ret_msg.update({'Message_Id': MessageAction.message_instance.message_id})
        ret_msg.update({'Ret_Code': ret_code, 'Detail':ret_data})
        if not MessageAction.callback_func is None:
            MessageAction.callback_func(str(ret_msg))

    def messageTransport(self):
        ret_code, ret_data = MessageAction.message_instance.messageTransport()
        MessageAction.callback(ret_code, ret_data)