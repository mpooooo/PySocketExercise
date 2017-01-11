#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import threading
import time
from user_action import UserAction
from message_action import MessageAction
from room_action import RoomAction
from game_action import GameEnginAction
sys.path.append('../')
from context.context import Context
from context.user import User
from context.hall import Hall
from server_logger import logger

class ActionInterface(UserAction, MessageAction, RoomAction, GameEnginAction):

    def __init__(self, user_obj = None, msg_obj = None, room_obj = None, callback_func = None):
        UserAction.__init__(self, user_obj)
        MessageAction.__init__(self, msg_obj, callback_func)
        RoomAction.__init__(self, room_obj)
        GameEnginAction.__init__(self)
        self.heartbeat_sock_handle = set()
        self.lock = threading.RLock()

    def roomEnter(self):
        RoomAction.roomEnter(self, self.getUser())
    
    def roomLeave(self):
        RoomAction.roomLeave(self, self.getUser())

    def roomInvite(self):
        user_id_list = self.getMessage().received_text.strip().split(' ')
        invite_user_id_list = []
        for invite_user in user_id_list:
            invite_user_id_list.append(invite_user.strip())
        RoomAction.roomInvite(self, self.getUser(), invite_user_id_list)

    def disconnect(self, user_handler):
        self.setCallback(None)
        context = Context.getInstance()
        goal_user, goal_user_id = None, None
        for user_id, user in context.getOnlineUser().items():
            if user.telecom_handler is user_handler:
                goal_user, goal_user_id = user, user_id
                break
        if not goal_user is None:
            logger.info('user[%s] disconnect to the server', goal_user.user_id)
            user_obj = User.getInstance(goal_user_id, goal_user.nick_name)
            self.setUser(user_obj)
            self.logout()
            # user_connected_list = context.getOnlineConnectedRoomWithUser(user_obj)
            # for room_obj in user_connected_list:
            #     self.setRoom(room_obj)
            #     RoomAction.roomLeave(self, user_obj)
            # del user_obj
        else:
            logger.error('disconnect user obj is None.')
            pass

    def gameMessageTransport(self):
        GameEnginAction.gameMessageTransport(self, self.getMessage(), self.getUser())

    def addHeartbeat(self, sock_handle):
        self.lock.acquire()
        self.heartbeat_sock_handle.add(sock_handle)
        self.lock.release()

    def heartbeatStart(self):
        logger.info('heartbeat start...')
        while True:
            self.lock.acquire()
            for sock_handle in self.heartbeat_sock_handle:
                sock_handle.asynRetData(str({'Heartbeat':'heartbeat'}))
            self.lock.release()
            time.sleep(2)
