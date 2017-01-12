#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
from message_action import callback, MessageAction
sys.path.append('..')
from context.hall import Hall
from context.context import Context

class UserAction(object):

    def __init__(self, user_obj):
        self._user = user_obj

    def setUser(self, user_obj):
        self._user = user_obj

    def getUser(self):
        return self._user

    @callback(MessageAction)
    def register(self):
        ret_code, ret_data = self._user.register()
        return ret_code, ret_data

    @callback(MessageAction)    
    def login(self):
        context = Context.getInstance()
        ret_code, ret_data = self._user.login()
        if ret_code is True:
            context.addOnlineUser(self._user.user_id, self._user)
            hall = Hall.getInstance()
            hall.enterRoom(self._user.user_id, self._user)
        return ret_code, ret_data

    @callback(MessageAction)
    def logout(self):
        context = Context.getInstance()
        ret_code, ret_data = self._user.logout()
        if ret_code is True:
            user_connected_list = context.getOnlineConnectedRoomWithUser(self._user)
            print user_connected_list
            for room_obj in user_connected_list:
                room_obj.leaveRoom(self._user.user_id, self._user)
            context.removeOnlineUser(self._user.user_id, self._user)
            del self._user
        return ret_code, ret_data