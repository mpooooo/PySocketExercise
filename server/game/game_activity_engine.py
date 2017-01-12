#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import threading
import time
from context.message import Message
from game21 import Game21

class GameActivityEngine(object):
   
    """docstring for ActivityEngine"""

    __instance = None
    lock = threading.RLock()
   
    def __init__(self):
        self.lock = threading.RLock()
        self.activity_instance = list()
        self.recv_message_queue = list()

    @classmethod
    def getInstance(cls):
        cls.lock.acquire()
        if(cls.__instance == None):
            cls.__instance = GameActivityEngine()
        cls.lock.release()
        return cls.__instance

    def start(self):
        self._loadActivity()
        while True:
           self._activityStart()
           time.sleep(1)

    def receiveMessage(self, message_obj, user_obj):
        self.lock.acquire()
        self.recv_message_queue.append((message_obj.consumer_id, message_obj.received_text, user_obj))
        self.lock.release()

    def sendMessage(self, msg_to, message):
        message = Message(None, None, msg_to, message)
        message.messageTransport()
        del message

    def _loadActivity(self):
        self.game21 = Game21()
        self.activity_instance.append(self.game21)

    def _activitySetUp(self, activity):
        if activity.triggerStart():
            activity.setUp()
            message = activity.getGameMessage()
            group = activity.getGameGroup()
            self.sendMessage(group, message)
        else:
            pass

    def _activitytearDown(self, activity):
        if activity.triggerEnd():
            winner = activity.getWinner()
            winner_message = None
            if not winner is None:
                winner_message = 'Game: winner is: ' + str(winner)
            else:
                winner_message = 'Game: nobody get correct answer.'
            group = activity.getGameGroup()
            self.sendMessage(group, winner_message)
            activity.tearDown()
        else:
            pass

    def _activityAlive(self, activity):
        self.lock.acquire()
        if activity.triggerAlive():
            del_list = []
            for msg_to, msg, user_obj in self.recv_message_queue:
                if msg_to == activity.getTag():
                    activity.judge(msg, user_obj)
                    del_list.append((msg_to, msg, user_obj))
                else:
                    pass
            else:
                for pair in del_list:
                    self.recv_message_queue.remove(pair)
        else:
            pass
        self.lock.release()

    def _activityStart(self):
        for act in self.activity_instance:
            self._activitySetUp(act)
            self._activitytearDown(act)
            self._activityAlive(act)