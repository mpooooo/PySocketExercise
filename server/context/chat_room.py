#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import thread
import threading 
import time
from base_room import BaseRoom
sys.path.append('../')
from server_logger import logger

class ChatRoom(BaseRoom):

    __instance = None
    lock = threading.RLock()
    
    def __init__(self, room_id, room_owner):     
        print 'this is chat room init'   
        super(ChatRoom, self).__init__(room_id, room_owner)

    @classmethod
    def getInstance(cls, room_id, room_owner):
        cls.lock.acquire()
        if(cls.__instance == None or (not cls.__instance.room_id == room_id) 
            or (not cls.__instance.room_owner == room_owner) ):
            cls.__instance = ChatRoom(room_id, room_owner)
        cls.lock.release()
        return cls.__instance

    def enterRoom(self, user_id, user_obj):
        user_id = user_obj.user_id
        if user_id in self.permission_user and not user_id in self.listening_user:
            self.addUser(user_id, user_obj)
            message = str({'system message':self.greet_message%(user_id, self.room_id)})
            self.boardcast(message)
            return True, 'enter success'
        else:
            return False, 'not permission or in the room already'

    def leaveRoom(self, user_id, user_obj):
        user_id = user_obj.user_id
        if user_id in self.listening_user:
            self.removeUser(user_id, user_obj)
            message = self.farewell_message%(user_id, self.room_id)
            return True, 'leave room success'
        return False, 'not in room failed'

    # def addUser2Room(self, user_id, user):
    #     if user_id in self.getPermitUser():
    #         message = str({'system message':self.greet_message%(user_id, self.room_id)})
    #         self.addUser(user_id, user)
    #         self.boardcast(message)
    #         return True
    #     else:
    #         return False
                
    # def removeRoomUser(self, user_id, user):
    #     message = self.farewell_message%(user_id, self.room_id)
    #     if user.user_id == user_id and self.removeUser(user_id, user):
    #         self.boardcast({'system message':message})
    #         return True
    #     else:
    #         return False

def test(i):
    r = ChatRoom.getInstance(0, 'admin')
    r.addUser(i, i)

class test_user(object):
    """docstring for test_user"""
    def __init__(self, arg):
        super(test_user, self).__init__()
        self.user_id = arg
        

if __name__ == '__main__':
    a = test_user(1)
    r = ChatRoom.getInstance(0, a)
    r1 = ChatRoom.getInstance(1, a)
    r2 = ChatRoom.getInstance(1, a)
    print id(r), id(r1), id(r2)
    r.addUser('a', 1)
    time.sleep(5)