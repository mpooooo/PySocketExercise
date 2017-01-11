#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import socket 
import time
import threading
import signal
from local_user import LocalUser
from message_parser import MessageParser
from action import Action
from client_logger import logger

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
            logger.debug('Clent create socket fd success.')
        except socket.error, msg:
            logger.error("client create socket failed, the error msg : %s.",msg)
            raise socket.error

        try:
            self.listen_fd.connect(self.addr)
            logger.debug('Client connect %s port %s success.', self.addr[0], self.addr[1])
        except socket.error, msg:
            logger.error('Client: connect %s port %s failed, the error msg: %s.',self.addr[0],self.addr[1],msg)
            raise socket.error
        logger.debug('connect %s success.', self.addr)

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
                logger.debug('client send user cmd message %s.', msg)
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
        logger.debug('client receive server message %s.', rev_data)
        rev_lst = None
        try:
           rev_lst = eval(rev_data)
        except TypeError:
            logger.error('Client receive data %s beyond rule.', rev_data)
        if not type(rev_lst) == type(list()):
            logger.error('Client do not receive %s except list', type(rev_lst))
        else:
            self.lock.acquire()
            for item in rev_lst:
                if type(item) == type(str()):
                    try:
                        item = eval(item)
                    except TypeError:
                        logger.error('Client receive date list should be eval to dict %s', item)
                if type(item) == type(dict()):
                    self.recv_queue.append(item)
                else:
                    logger.debug('Client do not recv %s item except dict.', type(item))
            self.lock.release()
        logger.debug('Client receive message %s from server after fliter.', self.recv_queue)

def loginOrRegister(client):
    parser = MessageParser()
    next_menu = False
    logger.info('Login And Register Menu.')
    while True:
        data = raw_input()
        logger.debug('User input %s in Client Login.', data)
        if data == 'exit':
            client.close()
            sys.exit()
        json_dct = parser.parse(data)
        logger.debug('User input after parser is %s.', json_dct)
        if json_dct and json_dct[parser.json_key_operate] == parser.json_key_operate_register:
            client.messageSend(str(json_dct))
            rev_lst = client.getReceiveData()
            for ret_dict in rev_lst:
                if ret_dict.has_key('Ret_Code') and (ret_dict['Ret_Code']) == True:
                    # logger.info('User register success.')
                    logger.info(ret_dict['Detail'])
                    break
            else:
                logger.info(ret_dict['Detail'])
                # logger.warning('User register failed, %s', ret_dict['Detail'])
        elif json_dct and json_dct[parser.json_key_operate] == parser.json_key_operate_login:
            client.messageSend(str(json_dct))
            rev_lst = client.getReceiveData()
            for ret_dict in rev_lst:
                if ret_dict.has_key('Ret_Code') and (ret_dict['Ret_Code']) is True:
                    user = LocalUser.getInstance()
                    user.setUserId(json_dct[parser.json_key_user][parser.json_key_user_id])
                    next_menu = True
                    logger.info(ret_dict['Detail'])
                    # logger.info('User login success.')
                    break
            else:
                logger.info(ret_dict['Detail'])
                # logger.info('User login failed')
        else:
            logger.warning('User input command beyond rule.')
        if next_menu:
            break

def inputMessage(action):
    parser = MessageParser()
    logger.info('input you chat command with the instruction above.')
    while True:
        input_cmd = raw_input('')
        if input_cmd == 'exit':
            action.client.close()
            sys.exit()
        print 'leihou', input_cmd
        json_dct = parser.parse(input_cmd)
        if json_dct:
            action.act(json_dct)
        else:
            logger.info('not in rule, please check and input your command again.')
    client.close()

def outputMessage(action):
    while True:
        ret_lst = action.client.getReceiveData()
        action.output(ret_lst)

def quit(signum, frame):
    logger.info('client close...')
    sys.exit()

if __name__ == '__main__':
    host = '10.53.228.191'
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
            * room create room_id:                   create chat room          *
            * room invite user1 user2:               invite users to room      *
            * room enter  room_id:                   enter to room             *
            * room leave room id:                    leave cur room            *
            *                                                                  *
            ********************************************************************
        '''
    try:
        user = LocalUser.getInstance()
        action = Action(client, user)
        output_thread = threading.Thread(target = outputMessage, args = [action])
        output_thread.setDaemon(True)
        output_thread.start()
        inputMessage(action)
    except Exception, exc:
        print exc

   