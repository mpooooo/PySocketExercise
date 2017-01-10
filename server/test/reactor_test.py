import unittest  
import sys
import socket
sys.path.append("../")
from reactor.event import Event
from reactor.reactor import Reactor

class ReactorTest(unittest.TestCase):  
    def setUp(self):
        self.host = '127.0.0.2'
        self.port = 2003
        
    def tearDown(self): 
        pass

    def reactorBackTest(self):
        addr = (self.host, self.port)
        listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        listen_fd.connect(addr)
        reactor1 = Reactor.getInstance()
        reactor2 = Reactor.getInstance()
        self.assertEqual(id(reactor1), id(reactor2))
        data = "{'Operate':'Register','User':{'User_Id':'asd','User_Nick_Name':'asd'}}"
        listen_fd.send(data)
        self.assertEqual('register success',listen_fd.recv(1024))
        listen_fd.close()

    def eventTest(self):
        self.assertEqual(Event.ReadEvent, 1) 
        self.assertEqual(Event.WriteEvent, 2) 
        self.assertEqual(Event.ErrorEvent, 3) 

def suite(): 
    suite = unittest.TestSuite() 
    suite.addTest(ReactorTest("eventTest"))
    suite.addTest(ReactorTest("reactorBackTest"))
    return suite  
    
if __name__ == "__main__": 
    unittest.main(defaultTest = 'suite')