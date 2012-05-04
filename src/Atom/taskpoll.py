# -*- coding: utf-8 -*-
'''
Created on 2012-4-22

@author: hang
'''
#############################################
from threading import Thread
from Queue import Queue
from PyQt4.QtCore import QTimer,QObject,SIGNAL
from warnings import catch_warnings

class PThreadProcess:
    """
    任务调度基类
    """
    def __init__(self):
        
        self.__pollTimer=QTimer()
        self.taskQueue=Queue()
        QObject.connect(self.__pollTimer, SIGNAL("timeout()"),self.processTask)
        
    
    def startPoll(self,polltime=200):
        """
        polltime为轮寻时间
        """
        #是否停止轮寻
        self.__stopPoll=False
        
        #每200毫秒扫描一次队列
        self.__pollTimer.start(200)
        
    def stopPoll(self):
        """
        停止轮讯
        """
        self.__stopPoll=True
        self.__pollTimer.stop()
        
    def processTask(self):
        """
        处理任务队列
        """
        #如果没有要求停止论讯，则遍历任务队列，并执行任务
        while not self.__stopPoll and self.taskQueue.qsize():
            #取得一个任务
            task=self.taskQueue.get(0)
            
            func=task[0]
            args=task[1]
            #执行处理
            func(*args)
        
        
#############################################
class PThread():
    """
    任务线程的基类
    """
    
    def __init__(self):
        pass
        
    def connect(self,pThreadProcess,processHandler):
        """
        将处理器绑定至任务队列
        处理器参数必须是字典dict
        """
        self.__taskQueue=pThreadProcess.taskQueue
        self.__processHandler=processHandler
        
    def start(self):
        self.thread=Thread(target=self.run,args=())
        self.thread.start()
        
    def isAlive(self):
        return self.thread.isAlive()
    
    def run(self):
        
        raise NotImplementedError()
    
    def emit(self,args):
        """
        提交任务
        """
        
        self.__taskQueue.put((self.__processHandler,args))
        
###########################################   