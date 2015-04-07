# -*- coding: utf-8 -*-

from SocketServer import ThreadingTCPServer, StreamRequestHandler
import logging.config
import logging
import logging.handlers as handlers
import os
import struct
import cPickle

LOGCONFIG = "E:\\code\\websafe\\back\\config\\log.cfg"

class LogRequestHandler(StreamRequestHandler):
    def handle(self):
        while 1:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L", chunk)[0]
            print slen
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            # ʹ��SocketHandler���͹��������ݰ���Ҫʹ�ý����ΪLogRecord
            # ��SocketHandler�ĵ�
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)
            print record

    def unPickle(self, data):
        return cPickle.loads(data)

    def handleLogRecord(self, record):
        logger = logging.getLogger(record.name)
        logger.handle(record)

class LogServer():
    '''����serve_forever()�������ģ�������Ҫ����һ�����̻��߳���������־����'''
    def __init__(self, addr, requestHandler):
        self.bindAddress    =   addr
        self.requestHandler =   requestHandler
        logging.config.fileConfig(LOGCONFIG)
        
    def start(self):
        self.svr = ThreadingTCPServer(self.bindAddress, self.requestHandler)
        self.svr.serve_forever()
    
    def stop(self):
        self.svr.shutdown()

        
class LogClient():
    def __init__(self, host, port, name, level):
        self.logger =   logging.getLogger(name)
        hdlr        =   handlers.SocketHandler(host, port)
        hdlr.setLevel(level)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(level)
        
    def GetLogger(self):
        return self.logger
        