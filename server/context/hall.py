#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import thread
import threading 
import time
from base_room import BaseRoom
from context import Context
from admin_user import AdminUser
sys.path.append('../')
from server_logger import logger

class Hall(BaseRoom):

    __instance = None
    lock = threading.RLock()

    def __init__(self):
        self.room_id = 'hall'
        self.room_owner = AdminUser.getInstance()
        super(Hall, self).__init__(self.room_id, self.room_owner)
        self.name = 'Hall'
        ctx = Context.getInstance()
        ctx.addOnlineRoom(self.room_id, self)

    @classmethod
    def getInstance(cls):
        cls.lock.acquire()
        if(cls.__instance == None):
            cls.__instance = Hall()
        cls.lock.release()
        return cls.__instance

    def enterRoom(self, user_id, user_obj):
        user_id = user_obj.user_id
        if not user_id in self.listening_user:
            message = str({'System_Message':self.greet_message%(user_id, self.room_id)})
            self.addUserPerssion(user_id)
            self.addUser(user_id, user_obj)
            self.boardcast(message)
            return True, 'enter hall success'
        return False, 'already in hall now'

    def leaveRoom(self, user_id, user_obj):
        context = Context.getInstance()
        context.removeOnlineUser(user_id, user_obj)
        return self.removeUser(user_id, user_obj)

# def test(i):
#     r = Hall.getInstance()
#     r.addUser({i:i})

# if __name__ == '__main__':
#     lst = []
#     for i in range(0, 100):
#         lst.append(thread.start_new_thread(test, (i,)))

#     r = Hall.getInstance()
#     print r.lock 
#     print r.listening_user
#     a = raw_input()