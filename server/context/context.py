#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import time
import threading
from locker import rlock, Locker
sys.path.append('../')
from server_logger import logger

class Context(object):

    __instance = None
    lock = threading.RLock()

    def __init__(self):
        self.online_user = {}
        self.online_room = {}
        self.user_room_map = {}
        self.user_connected_room = {}

    @classmethod
    def getInstance(cls):
        cls.lock.acquire()
        if(cls.__instance == None):
            cls.__instance = Context()
        cls.lock.release()
        return cls.__instance

    @rlock(Locker)
    def addOnlineRoomUser(self, room_id, user_obj):
        if not self.user_connected_room.has_key(user_obj.user_id):
            self.user_connected_room[user_obj.user_id] = set()
        self.user_connected_room[user_obj.user_id].add(room_id)
        # if not self.user_room_map.has_key(user_obj):
        #     self.user_room_map[user_obj] = set()
        # self.user_room_map[user_obj].add(room_id)
        logger.info('Context add online room [%s] user [%s]', room_id, user_obj)
        logger.info("Context status online room [%s], online user [%s], user:room [%s]", 
            self.online_room, self.online_user, self.user_connected_room)

    @rlock(Locker)
    def addOnlineRoom(self, room_id, room):
        self.online_room.update({room_id: room})
        room_owner = room.getRoomOwner()
        # if not self.user_room_map.has_key(room_owner):
        #     self.user_room_map[room_owner] = set()
        # self.user_room_map[room_owner].add(room_id)
        logger.info('Context add online room [%s]', room_id)
        logger.info("Context status online room [%s], online user [%s], user:room [%s]", 
            self.online_room, self.online_user, self.user_connected_room)

    @rlock(Locker)
    def changeOnlineRoomOwner(self, room_id, src_room_owner, dst_room_owner):
        if self.user_connected_room.has_key(src_room_owner.user_id) and \
            room_id in self.user_connected_room[src_room_owner.user_id]:
            self.user_connected_room[src_room_owner.user_id].remove(room_id)
            if not self.user_connected_room.has_key(dst_room_owner.user_id):
                self.user_connected_room[dst_room_owner.user_id] = set()
            self.user_connected_room[dst_room_owner.user_id].add(room_id)

        # if self.user_room_map.has_key(src_room_owner) and \
        #    room_id in self.user_room_map[src_room_owner]:
        #     self.user_room_map[src_room_owner].remove(room_id)
        #     if not self.user_room_map.has_key(dst_room_owner):
        #         self.user_room_map[dst_room_owner] = set()
        #     self.user_room_map[dst_room_owner].add(room_id)
        logger.info('Context change online room [%s] owner from %s to %s', room_id, src_room_owner.user_id, dst_room_owner.user_id)

    @rlock(Locker)
    def removeOnlineRoomUser(self, room_id, user_obj):
        if self.user_connected_room.has_key(user_obj.user_id) and \
            (room_id in self.user_connected_room[user_obj.user_id]):
            self.user_connected_room[user_obj.user_id].remove(room_id)
            if len(self.user_connected_room[user_obj.user_id]) == 0:
                del self.user_connected_room[user_obj.user_id]
        # if self.user_room_map.has_key(user_obj) and (room_id in self.user_room_map[user_obj]):
        #     self.user_room_map[user_obj].remove(room_id)
        #     if len(self.user_room_map[user_obj]) == 0:
        #         del self.user_room_map[user_obj]
        logger.info('Context remove online room [%s] user [%s]', room_id, user_obj)
        logger.info("Context status online room [%s], online user [%s], user:room [%s]", 
            self.online_room, self.online_user, self.user_connected_room)

    @rlock(Locker)
    def removeOnlineRoom(self, room_id, room_obj):
        if self.online_room.has_key(room_id):
            del self.online_room[room_id]
        # room_owner = room_obj.getRoomOwner()
        # for r_id in self.user_room_map[room_owner]:
        #     if r_id == room_id:
        #          self.user_room_map[room_owner].remove(r_id)
        #          if len(self.user_room_map) == 0:
        #             del self.user_room_map[room_owner]
        #          break
        # logger.info('Context remove online room [%s]', room_id)
        # logger.info("Context status online room [%s], online user [%s], user:room [%s]", 
        #     self.online_room, self.online_user, self.user_room_map)

    @rlock(Locker)
    def getOnlineConnectedRoomWithUser(self, user):
        room_id_list = list()
        if user.user_id in self.user_connected_room.keys():
            room_id_set = self.user_connected_room[user.user_id]
            for room_id in room_id_set:
                room_id_list.append(self.online_room[room_id])
        return room_id_list

    @rlock(Locker)
    def getOnlineRoom(self):
        ret = self.online_room
        return ret

    @rlock(Locker)
    def getOnlineRoomWithId(self, room_id):
        if self.online_room.has_key(room_id):
            return self.online_room[room_id]
        else:
            return None

    @rlock(Locker)
    def getOnlineRoomWithId(self, room_id):
        if self.online_room.has_key(room_id):
            return self.online_room[room_id]
        else:
            return None

    @rlock(Locker)
    def addOnlineUser(self, usr_id, user_obj):
        self.online_user.update({usr_id: user_obj})
        logger.info('Context add online user [%s]', usr_id)
        logger.info("Context status online room [%s], online user [%s], user:room [%s]", 
            self.online_room, self.online_user, self.user_connected_room)

    @rlock(Locker)
    def removeOnlineUser(self, usr_id, user_obj):
        if self.online_user.has_key(usr_id):
            del self.online_user[usr_id]
            if self.user_connected_room.has_key(user_obj.user_id):
                del self.user_connected_room[user_obj.user_id]
                # del self.user_room_map[user_obj.user_id]
            logger.info('Context remove online user [%s]', usr_id)
            logger.info("Context status online room [%s], online user [%s], user:room [%s]", 
            self.online_room, self.online_user, self.user_connected_room)

    @rlock(Locker)
    def getOnlineUser(self):
        ret = self.online_user
        return ret

    def __del__(self):
        pass