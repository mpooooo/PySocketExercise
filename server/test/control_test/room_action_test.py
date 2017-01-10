import unittest  
import sys,os
import socket
import time
sys.path.append("../../")
from control.controller import Controller

class RoomActionTest(unittest.TestCase):  

	received_data = None
	async_ret_message = None

	def setUp(self):
		self.controller = Controller()
		self.handler = RoomActionTest
		self.received_data = None

	@classmethod
	def asynRetData(self, ret_msg):
		print 'asynRetData:',ret_msg
		RoomActionTest.async_ret_message = ret_msg
		
	def tearDown(self): 
		pass

	def simulateHandler(self, input_msg):
		self.received_data = input_msg
		self.handler = RoomActionTest

	def distribute(self, input_msg):
		self.simulateHandler(input_msg)
		self.controller.distribute(self)
		time.sleep(1)
		
	def roomTest(self):
		input_msg = "{'Operate':'Room_Create','User':{'User_Id':'user1','User_Nick_Name':'user1'},'Room':{'Room_Id':'user1#room_1'}}"
		self.distribute(input_msg)
		self.assertEqual(RoomActionTest.async_ret_message, "{'Detail': 'Room create success.', 'Ret_Code': True}")
		self.distribute(input_msg)
		self.assertEqual(RoomActionTest.async_ret_message, "{'Detail': 'Room has been created.', 'Ret_Code': False}")
		input_msg = "{'Message': {'Message_To': None, 'Message_From': 'user1', 'Message_Id': 'user1@1483980161.7', 'Message_Text': None}, 'Operate': 'Room_Enter', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}, 'Room': {'Room_Id': 'user1#room_1'}}"
		self.distribute(input_msg)
		self.assertEqual(RoomActionTest.async_ret_message, "{'Ret_Code': True, 'Message_Id': 'user1@1483980161.7', 'Detail': 'enter success'}")
		self.distribute(input_msg)
		self.assertEqual(RoomActionTest.async_ret_message, "{'Ret_Code': False, 'Message_Id': 'user1@1483980161.7', 'Detail': 'enter failed'}")		
		input_msg = "{'Message': {'Message_To': None, 'Message_From': 'user1', 'Message_Id': 'user1@1483980432.81', 'Message_Text': None}, 'Operate': 'Room_Leave', 'User': {'User_Nick_Name': 'user1', 'User_Id': 'user1'}, 'Room': {'Room_Id': 'user1#room_1'}}"
		self.distribute(input_msg)
		self.assertEqual(RoomActionTest.async_ret_message, "{'Ret_Code': True, 'Message_Id': 'user1@1483980432.81', 'Detail': 'leave room success'}")
		self.distribute(input_msg)
		self.assertEqual(RoomActionTest.async_ret_message, "{'Ret_Code': False, 'Message_Id': 'user1@1483980432.81', 'Detail': 'leave room failed'}")
		time.sleep(1)

def suite():
	suite = unittest.TestSuite()
	suite.addTest(RoomActionTest("roomTest"))
	
	return suite  
	
if __name__ == "__main__": 
	if os.path.exists('./user.db'):
		os.remove('./user.db')
	unittest.main(defaultTest = 'suite')