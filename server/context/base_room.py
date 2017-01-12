#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import thread
import threading 
import time
import copy
from message import Message
from context import Context
from admin_user import AdminUser
sys.path.append('../')
from server_logger import logger

class BaseRoom(object):

    def __init__(self, room_id, room_owner):
    	self.room_id = room_id
    	self.room_owner = room_owner
        self.admin_owner = AdminUser.getInstance()
    	self.listening_user = dict()
        self.permission_user = set()
        self.permission_user.add(self.room_owner.user_id)
        self.permission_user.add(self.admin_owner.user_id)
        self.lock = threading.RLock()
        self.key_message_room_tag = 'Room_Place'
        self.greet_message = 'welcome %s to %s'
        self.farewell_message = '%s leave %s'

    def __del__(self):
        pass

    def create(self):
        ret_code, ret_data = True, str()
        ctx = Context.getInstance()
        if ctx.online_room.has_key(self.room_id):
            logger.info('Room [%s] has been created, owner is [%s].', self.room_id, self.room_owner)
            return False, 'Room has been created.'
        else:
            ctx.addOnlineRoom(self.room_id, self)
            logger.info("Room [%s] create success", self.room_id)
            return True, 'Room create success.'

    def destroy(self):
        ret_code, ret_data = True, str()
        context = Context.getInstance()
        context.removeOnlineRoom(self.room_id, self)
        logger.info('Room [%s] destroy, owner is [%s]', self.room_id, self.room_owner)

    def getRoomOwner(self):
        return self.room_owner

    def getPermitUser(self):
        self.lock.acquire()
        ret = self.permission_user
        self.lock.release()
        return ret

    def addUser(self, user_id, user_obj):
        ctx = Context.getInstance()
        # ctx.addOnlineUser(user_id, user_obj)
        ctx.addOnlineRoomUser(self.room_id, user_obj)
    	self.lock.acquire()
        self.listening_user.update({user_id: user_obj})
        logger.info("user [%s] enter room [%s], room users now [%s].",user_id, self.room_id, self.listening_user)
        self.lock.release()
        return True

    def removeUser(self, user_id, user_obj):
    	self.lock.acquire()
        ret_code = False
        if self.listening_user.has_key(user_id):
            ctx = Context.getInstance()
            if self.room_owner.user_id == user_id: 
                ctx.changeOnlineRoomOwner(self.room_id, user_obj, self.admin_owner)
            ctx.removeOnlineRoomUser(self.room_id, user_obj)
            del self.listening_user[user_id]
            self.permission_user.remove(user_id)
            logger.info("user [%s] leave room [%s], room users now [%s].",user_id, self.room_id, self.listening_user)
            ret_code = True
        self.lock.release()
        return ret_code
    
    def addUserPerssion(self, user_id):
        self.lock.acquire()
        self.permission_user.add(user_id)
        self.lock.release()

    def inviteUser(self, inviter, invited_user_id = []):
        logger.info("user [%s] invite %s to [%s]", inviter, invited_user_id, self.room_id)
        invite_msg = "%s invite you to room %s"
        self.lock.acquire()
        ret_code = True
        if not inviter in self.permission_user:
            ret_code = False
        else:
            for user_id in invited_user_id:
                if not user_id in self.permission_user:
                    message = Message(None, inviter, user_id, invite_msg%(inviter, self.room_id))
                    self.permission_user.add(user_id)
                    message.messageTransport()
                else:
                    pass
        logger.info("after invitation, the permitted user is [%s].", self.permission_user)
        self.lock.release()
        return ret_code

    def boardcast(self, message_dict, except_user = None):
        self.lock.acquire()
        logger.info('room [%s] received message [%s].', self.room_id, message_dict)
        if except_user is None:
            except_user = []
        message_dict.update({self.key_message_room_tag: self.room_id})
        for user_id, user_obj in self.listening_user.items():
            if user_id in except_user:
                continue
            try:
                logger.info('room message [%s] send to user [%s]', message_dict, user_obj.user_id)
                user_obj.receiveMessage(message_dict)
            except:
                import traceback
                traceback.print_exc()  
        self.lock.release()
        return True