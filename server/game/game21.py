#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import time
import datetime
import random

class Game21(object):

    def __init__(self):
        self._game_message = 'user +=*/ with number %s to close 21'
        self._activity_tag = '21game'
        self._game_last = 3
        self._stop = False
        self._group = 'hall'
        self._answer_users = set()
        self._alive = False
        self._numbers = []

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
        #if cur_time.minute == 0 and cur_time.second == 0 and cur_time.minute%1 == 0:
        if cur_time.second % 10 == 0:
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
        #if (cur_time.minute == self._game_last and cur_time.second == 0 and cur_time.hour%3 == 0) or self._stop:
        if self.start_time.minute + self._game_last == cur_time.minute or self._stop:
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
        print numbers, self._numbers, numbers.sort() == self._numbers.sort()
        return numbers.sort() == self._numbers.sort()

    def judge(self, message_str, user):
        if not self._alive:
            return False 
        print 'judging ',message_str, user
        if user in self._answer_users:
            print 'user has been answer'
            return False
        self._answer_users.add(user)
        if not self.check(message_str):
            return False
        try:
            result = eval(message_str.strip())
            print 'get result', result
        except:
            return False
        if result <= 21 and result > self._max_point:
            self._max_point = result
            self._winner = user
            if result == 21:
                self.stop()
        return True


if __name__ == '__main__':
    message_str = '1+ &2+3+4'
    g21 = Game21()
    print g21.check(message_str)
    print [2,1].sort() == [1,2].sort()