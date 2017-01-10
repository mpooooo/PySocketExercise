import unittest  
import sys,os
import socket
import time
sys.path.append("../")
from context.user import User
from context.message import Message
from context.chat_room import ChatRoom
from context.context import Context
from context.hall import Hall
from context.admin_user import AdminUser

class ContextTest(unittest.TestCase):  
    
    def setUp(self):
        self.usr1 = User(ContextTest, 'hywwqq1', 'hywwqq1', '123456')
        self.usr2 = User(ContextTest, 'hywwqq1', 'hywwqq1', '1236')
        self.room1 = ChatRoom.getInstance('hywwqq#11', self.usr1)

    @classmethod
    def asynRetData(self, ret_code, ret_data):
        print 'asynRetData:',ret_code, ret_data
        
    def tearDown(self): 
        pass

    def userTest(self):
        self.assertEqual(self.usr1.register(), (True, 'User registered complete.')) 
        self.assertEqual(self.usr1.login(), (True, 'login success.'))
        self.assertEqual(self.usr2.register(), (False, 'User has already registered.'))
        self.assertEqual(self.usr2.login(), (False, 'login failed with wrong pass word.'))
        time.sleep(1)
        self.assertTrue(self.usr1.getOnlineTime() > 1)
        ctx = Context.getInstance()
        self.assertEqual(self.usr1.login(), (False, 'user has been login'))
        self.assertTrue(self.usr1.logout())
        self.assertFalse(self.usr1.logout())
        self.assertEqual(self.usr1.login(), (True, 'login success.'))

    def roomTest(self):
        room2 = ChatRoom.getInstance('hywwqq#11', self.usr1)
        self.assertEqual(id(self.room1), id(room2))
        usr3 = User(sys.stdout, 'asd', 'asd', '1236')
        room3 = ChatRoom.getInstance('asd#1', usr3)
        self.assertNotEqual(id(self.room1), id(room3))
        self.room1.addUser2Room(self.usr1.user_id, self.usr1)
        self.assertEqual(usr3.register(), (True, 'User registered complete.')) 
        self.assertFalse(self.room1.addUser2Room(usr3.user_id, usr3))
        self.room1.inviteUser(self.room1.room_owner.user_id, [usr3.user_id])
        usr4 = User(sys.stdout, 'qwe', 'qwe', '1236')
        self.assertFalse(self.room1.inviteUser(usr4.user_id, [usr4.user_id]))
        self.assertTrue(self.room1.inviteUser(usr3.user_id, [usr4.user_id]))
        self.assertTrue(self.room1.create())
        self.assertFalse(self.room1.create())
        self.assertFalse(self.room1.removeRoomUser(usr3.user_id, usr3))
        self.assertTrue(self.room1.enterRoom(usr3.user_id, usr3))
        self.assertFalse(self.room1.enterRoom(usr3.user_id, usr3))
        self.assertFalse(self.room1.enterRoom(usr3.user_id, usr4))
        self.assertTrue(self.room1.enterRoom(usr4.user_id, usr4))
        self.room1.removeRoomUser(usr3.user_id, usr3)
        self.assertEqual(id(self.usr1), id(self.room1.room_owner))
        self.room1.removeRoomUser(self.room1.room_owner.user_id, self.room1.room_owner)
        self.room1.destroy()

    def hallTest(self):
        hall = Hall.getInstance()
        self.assertEqual(hall.room_id, 'hall')
        self.assertEqual(hall.room_owner, AdminUser.getInstance())
        usr = User(sys.stdout, 'qwe', 'qwe', '1236')
        self.assertFalse(usr.login()[0])
        self.assertTrue(usr.register()[0])
        self.assertTrue(usr.login()[0])
        usr2 = User(sys.stdout, 'aaa', 'asd', '1236')
        self.assertTrue(usr2.register()[0])
        self.assertTrue(usr2.login()[0])
        self.assertTrue(hall.removeRoomUser(usr2.user_id, usr2))
        self.assertTrue(hall.addUser2Room(usr2.user_id, usr2))

def suite(): 
    suite = unittest.TestSuite() 
    suite.addTest(ContextTest("userTest"))
    suite.addTest(ContextTest("roomTest"))
    suite.addTest(ContextTest("hallTest"))
    return suite  
    
if __name__ == "__main__": 
    if os.path.exists('./user.db'):
        os.remove('./user.db')
    unittest.main(defaultTest = 'suite')