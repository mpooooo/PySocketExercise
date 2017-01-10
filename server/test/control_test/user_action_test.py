import unittest  
import sys,os
import socket
import time
sys.path.append("../../")
from control.controller import Controller

class UserActionTest(unittest.TestCase):  

	received_data = None
	async_ret_message = None

	def setUp(self):
		self.controller = Controller()
		self.handler = UserActionTest
		self.received_data = None

	@classmethod
	def asynRetData(self, ret_msg):
		print 'asynRetData:',ret_msg
		UserActionTest.async_ret_message = ret_msg
		
	def tearDown(self): 
		pass

	def simulateHandler(self, input_msg):
		self.received_data = input_msg
		self.handler = UserActionTest

	def distribute(self, input_msg):
		self.simulateHandler(input_msg)
		self.controller.distribute(self)
		time.sleep(1)

	def userOperate(self, input_msg):
		ret_code, ret_data = self.controller.messageCheck(input_msg)
		self.assertTrue(ret_code)
		user = self.controller.extractUser(self.handler, ret_data)
		self.assertEqual(user.user_id, 'qwe')
		self.assertEqual(user.nick_name, 'qwe')
		UserActionTest.received_data = input_msg
		self.controller.distribute(self.handler)
		time.sleep(1)
		
	def userTest(self):
		input_msg = "{'Operate':'Register','User':{'User_Id':'qwe','User_Nick_Name':'qwe', 'User_Pass_Word':'123456',}}"
		self.userOperate(input_msg)
		self.assertEqual(UserActionTest.async_ret_message, "{'Detail': 'User registered complete.', 'Ret_Code': True}")
		input_msg =  "{'Operate':'Login','User':{'User_Id':'qwe','User_Nick_Name':'qwe', 'User_Pass_Word':'123456',}}"
		self.userOperate(input_msg)
		self.assertEqual(UserActionTest.async_ret_message, "{'Detail': 'login success.', 'Ret_Code': True}")
		input_msg =  "{'Operate':'Logout','User':{'User_Id':'qwe','User_Nick_Name':'qwe', 'User_Pass_Word':'123456',}}"
		self.userOperate(input_msg)
		self.assertEqual(UserActionTest.async_ret_message, "{'Detail': 'logout success', 'Ret_Code': True}")

def suite():
	suite = unittest.TestSuite()
	suite.addTest(UserActionTest("userTest"))
	
	return suite  
	
if __name__ == "__main__": 
	if os.path.exists('./user.db'):
		os.remove('./user.db')
	unittest.main(defaultTest = 'suite')