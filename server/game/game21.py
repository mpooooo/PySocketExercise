#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import time
import datetime
import random

class Game21(object):

    def __init__(self):
        self._game_message = 'Notice: 21Game task: use number %s with +=*/() to close 21'
        self._activity_tag = '21game'
        self._stop = False
        self._group = 'hall'
        self._answer_users = set()
        self._alive = False
        self._numbers = []
        self._gameLastInit()

    def setUp(self):
        self._answer_users.clear()
        self._numbers = []
        self._winner = None
        self._max_point = 0
        for i in range(0, 4):
            num = random.randint(1,10)
            self._numbers.append(num)

    def getTag(self):
        return self._activity_tag

    def getGameGroup(self):
        return self._group

    def tearDown(self):
        self._numbers = []
        self._winner = None
        self._answer_users.clear()
        self._alive = False
        self._max_point = 0

    def triggerAlive(self):
        return self._alive

    def getGameMessage(self):
        return self._game_message%(self._numbers)

    def triggerStart(self):
        if self._alive is True:
            return False
        cur_time = datetime.datetime.now()
        if cur_time.minute in [0, 30] and cur_time.second == 0:
            self.start_time = cur_time
            self._alive = True
            return True
        return False

    def stop(self):
        self._stop = True

    def triggerEnd(self):
        cur_time = datetime.datetime.now()
        if not self._alive:
            return False
        if ((self.start_time.minute + self._game_last_minute) == cur_time.minute 
            and (self.start_time.hour + self._game_last_hour) == cur_time.hour 
            and (self.start_time.second + self._game_last_second) == cur_time.second
            ) or self._stop:
            self._alive = False
            return True
        return False

    def getWinner(self):
        return self._winner

    def check(self, message_str):
        message_str = message_str.replace(' ', '')
        for c in message_str:
            if c.isdigit():
                pass
            elif c in ['+', '-', '*', '/', '(', ')']:
                message_str = message_str.replace(c, ' ')
            else:
                return False
        numbers = message_str.strip().split(' ')
        numbers = [int(n) for n in numbers]
        return numbers.sort() == self._numbers.sort()

    def judge(self, message_str, user_obj):
        if not self._alive:
            return False 
        user_id = user_obj.user_id
        if user_id in self._answer_users:
            user_obj.receiveMessage(str({'System_Message': 'You have been answered'}))
            return False
        self._answer_users.add(user_id)
        if not self.check(message_str):
            return False
        try:
            result = eval(message_str.strip())
        except:
            return False
        if result <= 21 and result > self._max_point:
            self._max_point = result
            self._winner = user_id
            if result == 21:
                self.stop()
        return True

    def _gameLastInit(self):
        self._game_last_day = 0
        self._game_last_hour = 0        
        self._game_last_minute = 3
        self._game_last_second = 0

# if __name__ == '__main__':
#     message_str = '1+ &2+3+4'
#     g21 = Game21()
#     print g21.check(message_str)
#     print [2,1].sort() == [1,2].sort()