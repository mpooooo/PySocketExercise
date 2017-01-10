#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import socket 
import logging
import time
import threading
import signal
from local_user import LocalUser
from message_parser import MessageParser
from action import Action
import copy

logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s  %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S', 
                    filename='./client.log'   
                    ) 

class Client(object):

    def __init__(self):
        self.addr = None
        self.listen_fd = None
        self.send_queue = []
        self.lock = threading.RLock()
        self.recv_queue = []

    def connectServer(self, host, port):
        self.addr = (host, port)
        try:
            self.listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            logging.info('Clent create socket fd success.')
        except socket.error, msg:
            logging.error("client create socket failed, the error msg : %s.",msg)
            raise socket.error

        try:
            self.listen_fd.connect(self.addr)
            logging.info('Client connect %s port %s success.', self.addr[0], self.addr[1])
        except socket.error, msg:
            logging.error('Client: connect %s port %s failed, the error msg: %s.',self.addr[0],self.addr[1],msg)
            raise socket.error
        print 'connect success.'

    def close(self):
        self.listen_fd.close()

    def messageInput(self, msg):
        self.lock.acquire()
        self.send_queue.append(msg)
        self.lock.release()

    def messageSend(self, data):        
        self.messageInput(data)
        self.lock.acquire()
        if self.send_queue:
            for msg in self.send_queue:
                self.listen_fd.sendall(msg)
            self.send_queue = []
        else:
            pass
        self.lock.release()

    def getReceiveData(self):
        self.messageReveive()
        self.lock.acquire()
        ret_data = self.recv_queue
        self.recv_queue = []
        self.lock.release()
        return ret_data

    def messageReveive(self, buffer_size = 1024):
        rev_data = self.listen_fd.recv(buffer_size)
        logging.info('receive original msg data: %s.', rev_data)
        rev_lst = eval(rev_data)
        if not type(rev_lst) == type(list()):
            logging.error('Client receive wrong data %s.', rev_lst)
        self.lock.acquire()
        for item in rev_lst:
            if not type(item) == type(dict()):
                self.recv_queue.append(eval(item))
            else:
                self.recv_queue.append(item)
        self.lock.release()
        print 'receive data %s'%rev_lst

def loginOrRegister(client):
    parser = MessageParser()
    next_menu = False
    while True:
        data = raw_input()
        if data == 'exit':
            client.close()
            sys.exit()
        json_dct = parser.parse(data)
        if json_dct and json_dct[parser.json_key_operate] == parser.json_key_operate_register:
            client.messageSend(str(json_dct))
            rev_lst = client.getReceiveData()
            for ret_dict in rev_lst:
                if ret_dict.has_key('Ret_Code') and (ret_dict['Ret_Code']) == True:
                    print 'register success'
                    break
            else:
                print 'register failed'
        elif json_dct and json_dct[parser.json_key_operate] == parser.json_key_operate_login:
            client.messageSend(str(json_dct))
            rev_lst = client.getReceiveData()
            print 'login',rev_lst
            for ret_dict in rev_lst:
                if ret_dict.has_key('Ret_Code') and (ret_dict['Ret_Code']) is True:
                    user = LocalUser.getInstance()
                    user.setUserId(json_dct[parser.json_key_user][parser.json_key_user_id])
                    print 'login success'
                    next_menu = True
                    break
            else:
                print 'login failed'
        else:
            print 'login or register menu.'
        if next_menu:
            break

def inputMessage(action):
    parser = MessageParser()
    print 'input chat cmd in the blow...'
    while True:
        input_cmd = raw_input('')
        if input_cmd == 'exit':
            action.client.close()
            sys.exit()
        json_dct = parser.parse(input_cmd)
        if json_dct:
            action.act(json_dct)
        else:
            print 'please input again'
    client.close()

def outputMessage(action):
    while True:
        ret_lst = action.client.getReceiveData()
        action.output(ret_lst)

def quit(signum, frame):
    print 'client close'
    sys.exit()

if __name__ == '__main__':
    host = '127.0.0.2'
    port = 2003
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    client = Client()
    client.connectServer(host, port)
    print '''
            *******************************************************************
            *                           Start Menu                            *
            *                                                                 *
            * register user_id passwords :     register user account          *         
            * login user_id passwords:         login server with account info *    
            * logout:                          user logout                    *    
            *                                                                 *
            *******************************************************************
          '''
    loginOrRegister(client)
    print '''
            ********************************************************************
            *                          Chat Dialog                             *   
            *                                                                  *
            * chat message:                          send message to cur room  *
            * chat [user] message:                   send message to user      *
            * room create [room id]:                 create chat room          *
            * room invite [room id]  user1 user2:    invite users to room      *
            * room enter [room id]:                  enter to room             *
            * room leave [room id]:                  leave cur room            *
            *                                                                  *
            ********************************************************************
        '''
    try:
        user = LocalUser.getInstance()
        print user
        action = Action(client, user)
        output_thread = threading.Thread(target = outputMessage, args = [action])
        output_thread.setDaemon(True)
        output_thread.start()
        inputMessage(action)
    except Exception, exc:
        print exc

   