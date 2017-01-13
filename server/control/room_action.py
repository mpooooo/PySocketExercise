#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
from message_action import callback, MessageAction
sys.path.append('..')
from context.context import Context
from context.hall import Hall

class RoomAction(object):

    def __init__(self, room_obj):
        self._room = None
        self.setRoom(room_obj)
        #self

    def setRoom(self, room_obj):
        online_room = None
        if not room_obj is None:
            context = Context.getInstance()
            online_room = context.getOnlineRoomWithId(room_obj.room_id)
        if online_room is None:
            self._room = room_obj
        else:
            self._room = online_room

    def getRoom(self):
        return self._room

    @callback(MessageAction)
    def roomCreate(self):
        ret_code, ret_data = self._room.create()
        return ret_code, ret_data

    @callback(MessageAction)
    def roomEnter(self, user_obj):
        context = Context.getInstance()
        goal_room_id, goal_room = self._room.room_id, None
        ret_code, ret_data = False, str()
        if self._room.room_id in context.online_room:
            goal_room = context.getOnlineRoomWithId(goal_room_id)
        if not goal_room is None:
            ret_code, ret_data = goal_room.enterRoom(user_obj.user_id, user_obj)
        else:
            ret_code, ret_data = False, 'can not find the room id in online rooms'
        return ret_code, ret_data

    @callback(MessageAction)
    def roomLeave(self, user_obj):
        context = Context.getInstance()
        goal_room_id, goal_room = self._room.room_id, None
        ret_code, ret_data = False, str()
        if self._room.room_id in context.online_room:
            goal_room = context.getOnlineRoomWithId(goal_room_id)
        if not goal_room is None:
            ret_code, ret_data = goal_room.leaveRoom(user_obj.user_id, user_obj)
        else:
            ret_code, ret_data = False, 'can not find the room id in online rooms'
        return ret_code, ret_data

    @callback(MessageAction)
    def roomInvite(self, invitor_user_obj, invited_user_id_list):
        context = Context.getInstance()
        goal_room_id, goal_room = self._room.room_id, None
        ret_code, ret_data = False, str()
        if self._room.room_id in context.online_room:
            goal_room = context.getOnlineRoomWithId(goal_room_id)
        if not goal_room is None:
            invitor_id = invitor_user_obj.user_id
            ret_code = goal_room.inviteUser(invitor_id, invited_user_id_list)
        else:
            ret_code, ret_data = False, 'can not find the room id in online rooms'
        return ret_code, ret_data