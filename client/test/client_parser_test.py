#!/usr/bin/env python2.7
#coding=utf-8
import unittest  
import sys,os
import socket
import time
sys.path.append("../")
from message_parser import MessageParser
from local_user import LocalUser
from client import Client
from action import Action

class MessageParserTest(unittest.TestCase): 
	'''
		test for the json message for server translated by message_parser with user's input
		for example:　chat haha => {'Message': {'Message_To': 'hall', 'Message_From': 'user1', 'Message_Text': 'haha1'}, \
					　'Operate': 'Message_Send', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}}
	'''

	def setUp(self):
		self.parser = MessageParser()
		self.user = LocalUser.getInstance()
		self.user.setUserId('user1')

	def tearDown(self): 
		pass

	def parserTest(self, in_str, aim_out_str):
		result = self.parser.parse(in_str)
		aim_result = (eval(aim_out_str))
		del result[self.parser.json_key_message][self.parser.json_key_message_id]
		self.assertEqual(result, aim_result)

	def cmdTest(self):
		input1 = 'chat haha1'
		out1 = "{'Message': {'Message_To': 'hall', 'Message_From': 'user1', 'Message_Text': 'haha1'}, 'Operate': 'Message_Send', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}}"
		print self.parser.parse(input1)
		self.parserTest(input1, out1)

		input2 = 'chat [user1] haha'
		out2 = "{'Message': {'Message_To': 'user1', 'Message_From': 'user1', 'Message_Text': 'haha'}, 'Operate': 'Message_Send', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}}"
		self.assertEqual(self.user.getUserInfo(), eval("{'User_Nick_Name': 'user1', 'User_Id': 'user1'}"))
		result2 = self.parser.parse(input2)
		del result2[self.parser.json_key_message][self.parser.json_key_message_id]
		aim_res = (eval(out2))
		self.assertEqual(result2,aim_res)

		input3 = 'register asd 123456'
		out3 = "{'Operate': 'Register', 'User': {'User_Pass_Word': '123456', 'User_Nick_Name': 'asd', 'User_Id': 'asd'}}"
		self.assertEqual(self.parser.parse(input3), eval(out3))

		input4 = 'login asd 123456'
		out4 = "{'Operate': 'Login', 'User': {'User_Pass_Word': '123456', 'User_Nick_Name': 'asd', 'User_Id': 'asd'}}"
		self.assertEqual(self.parser.parse(input4), eval(out4))

		input5 = 'chat [asd] 123456'
		out5 = "{'Message': {'Message_To': 'asd', 'Message_From': 'user1', 'Message_Text': '123456'}, 'Operate': 'Message_Send', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}}"
		self.parserTest(input5, out5)

		input6 = 'room create room_1'
		out6 = "{'Message': {'Message_To': None, 'Message_From': None, 'Message_Text': None}, 'Operate': 'Room_Create', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}, 'Room': {'Room_Id': 'user1#room_1'}}"
		self.parserTest(input6, out6)

		input7 = 'room invite user1 asd'
		out7 = "{'Message': {'Message_To': None, 'Message_From': 'user1', 'Message_Text': 'user1 asd'}, 'Operate': 'Room_Invite', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}, 'Room': {'Room_Id': 'hall'}}"
		self.parserTest(input7, out7)

		input8 = 'room enter room_1'
		print self.parser.parse(input8)
		out8 = "{'Message': {'Message_To': None, 'Message_From': 'user1', 'Message_Text': None}, 'Operate': 'Room_Enter', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}, 'Room': {'Room_Id': 'user1#room_1'}}"
		self.parserTest(input8, out8)

		input9 = 'room leave room_1'
		print self.parser.parse(input9)
		out9 = "{'Message': {'Message_To': None, 'Message_From': 'user1', 'Message_Text': None}, 'Operate': 'Room_Leave', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}, 'Room': {'Room_Id': 'hall'}}"
		self.parserTest(input9, out9)

		input10 = '21game 1+2+3/6'
		out10 = "{'Message': {'Message_To': '21game', 'Message_From': 'user1', 'Message_Text': '1+2+3/6'}, 'Operate': 'Game', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}}"
		result10 = self.parser.parse(input10)
		print result10
		self.parserTest(input10, out10)

def suite(): 
	suite = unittest.TestSuite() 
	suite.addTest(MessageParserTest("cmdTest"))
	return suite  
	
if __name__ == "__main__": 
	unittest.main(defaultTest = 'suite')