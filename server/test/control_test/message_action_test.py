import unittest  
import sys,os
import socket
import time
sys.path.append("../../")
from control.controller import Controller

class MessageAction(unittest.TestCase):  

	received_data = None
	async_ret_message = None

	def setUp(self):
		self.controller = Controller()
		self.handler = MessageAction
		self.received_data = None

	@classmethod
	def asynRetData(self, ret_msg):
		print 'asynRetData:',ret_msg
		MessageAction.async_ret_message = ret_msg
		
	def tearDown(self): 
		pass

	def simulateHandler(self, input_msg):
		self.received_data = input_msg
		self.handler = MessageAction

	def distribute(self, input_msg):
		self.simulateHandler(input_msg)
		self.controller.distribute(self)
		time.sleep(1)

	def messageTest(self):
		input_msg = "{'Message': {'Message_To': 'hall', 'Message_From': 'user1', 'Message_Id': 'user1@1483974195.38', 'Message_Text': 'haha1'}, 'Operate': 'Message_Send', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}}"	
		self.distribute(input_msg)
		self.assertEqual(MessageAction.async_ret_message, "{'Ret_Code': False, 'Message_Id': 'user1@1483974195.38', 'Detail': 'can not find online user or room.'}")
		input_msg1 = "{'Operate':'Register','User':{'User_Id':'qwe','User_Nick_Name':'qwe', 'User_Pass_Word':'123456',}}"
		self.distribute(input_msg1)
		input_msg2 = "{'Operate':'Login','User':{'User_Id':'qwe','User_Nick_Name':'qwe', 'User_Pass_Word':'123456',}}"
		self.distribute(input_msg2)
		self.distribute(input_msg)
		self.assertEqual(MessageAction.async_ret_message, "{'Ret_Code': True, 'Message_Id': 'user1@1483974195.38', 'Detail': 'message send success.'}")
		time.sleep(1)

def suite():
	suite = unittest.TestSuite()
	suite.addTest(MessageAction("messageTest"))

	
	return suite  
	
if __name__ == "__main__": 
	if os.path.exists('./user.db'):
		os.remove('./user.db')
	unittest.main(defaultTest = 'suite')