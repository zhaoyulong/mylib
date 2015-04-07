# -*- coding: utf-8 -*-

import os
import threading
import socket
import time

INTERNEL = 10 #10s
TIMEOUT = 10*60 #10m

class HeartBeatServerThread(threading.Thread):
    def ErrHandler(self, e):
        print e
        
    def TimeoutHandler(self, addr):
        print addr
        
    def __init__(self, sock, lock, timeout):
        '''构造函数'''
        self.sock       =   sock
        self.lock       =   lock
        self.running    =   True
        self.timeout    =   timeout
        self.clients    =   {}
        self.errHandler =   self.ErrHandler
        self.timeoutHandler =    self.TimeoutHandler
        threading.Thread.__init__(self)
        
    def Stop(self):
        self.running = False
    
    def setErrorHandler(self, func):
        self.errHandler  =   func
        
    def setTimeoutHandler(self, func):
        self.timeoutHandler  =   func
    
    def update(self, data, addr):
        if data == 'beat':
            self.lock.acquire()
            self.clients[addr] = time.time()
            self.lock.release()
        
        elif data == 'end':
            self.lock.acquire()
            del self.clients[addr]
            self.lock.release()
        
    def check(self):
        self.lock.acquire()
        curtime = time.time()
        TimeoutList = []
        for key in self.clients:
            if curtime - self.clients[key] > self.timeout:
                TimeoutList.append(key)
                
        for key in TimeoutList:
            del self.clients[key]
            self.timeoutHandler(key)
        self.lock.release()
        if self.running:
            threading.Timer(self.timeout, self.check, ()).start()
        
    def run(self):
        threading.Timer(self.timeout, self.check, ()).start()
        while self.running:
            data = ''
            try:
                data, addr = self.sock.recvfrom(1024)
                if len(data) > 0:
                    self.update(data, addr)
            except socket.error as e:
                if e[0] == 10035:
                    if len(data) == 0:
                        continue
                elif e[0] == 11:
                    if len(data) == 0:
                        continue
                else:
                    self.errHandler(e)
                    break
            
            finally:
                time.sleep(0.05)
            
                
         
class HeartBeatClientThread(threading.Thread):
    def ErrHandler(self, e):
        print e
        
    def __init__(self, sock, internal, addr):
        '''构造函数'''
        self.sock       =   sock
        self.internal   =   internal
        self.running    =   True
        self.serverAddr =   addr
        self.errHandler =   self.ErrHandler
        threading.Thread.__init__(self)    
        
    def Stop(self):
        self.sock.sendto('end',self.serverAddr)
        self.running = False
    
    def setErrorHandler(self, func):
        self.errHandler  =   func
        
    def run(self):
        while self.running:
            try:
                self.sock.sendto('beat',self.serverAddr)
            except socket.error as e:
                if e[0] == 10035:
                    time.sleep(1)
                    continue
                elif e[0] == 11:
                    time.sleep(1)
                    continue
                else:
                    self.errHandler(e)
                    break
            finally:
                time.sleep(self.internal)
                

def CreateServer(IP, port, timeout=TIMEOUT):
    sock    =   socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setblocking(0)
    sock.bind((IP,port))
    return HeartBeatServerThread(sock, threading.Lock(), timeout)

def CreateClient(IP, port, internale=INTERNEL):
    sock    =   socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return HeartBeatClientThread(sock, internale, (IP, port))