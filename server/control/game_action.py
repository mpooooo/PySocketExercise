#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
from game.game_activity_engine import GameActivityEngine

class  GameEnginAction(object):

	"""docstring for  GameAction"""

	def __init__(self):
		pass

	def gameEnginStart(self):
		engine = GameActivityEngine.getInstance()
		engine.start()

	def gameMessageTransport(self, msg_obj, user_obj):
		engine = GameActivityEngine.getInstance()
		engine.receiveMessage(msg_obj, user_obj)
