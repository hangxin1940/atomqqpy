# -*- coding: utf-8 -*-
from taskpoll import PThread
class ThreadLoginChannel(PThread):
    """
    正式登录
    """
    
    def __init__(self,uin,status):
        PThread.__init__(self)
        
        self.uin=uin
        self.status=status
        
    
    def run(self):
        from Tencent.WebQQ.protocol import Login
        login=Login()
        result=login.loginChannel(self.uin, self.status)
        if result.get("retcode")==0:
            self.emit((True,result.get("result")))
        else:
            self.emit((False,result))
###################################################################
import Tencent.WebQQ.protocol as protocol
class ThreadGetFriendInfo(PThread):
    """
    获得用户资料
    """
    
    def __init__(self,uin):
        PThread.__init__(self)
        self.uin=uin
    
    def run(self):
        
        result=protocol.getFriendInfo(self.uin)
        
            
        self.emit((result,))

###################################################################
class ThreadGetFriendList(PThread):
    """
    获得用户好友列表
    """
    
    def __init__(self):
        PThread.__init__(self)
    
    def run(self):
        
        result=protocol.getFriendList()
        
            
        self.emit((result,))

###################################################################
class ThreadGetOnlineFriends(PThread):
    """
    获得用户好友列表
    """
    
    def __init__(self):
        PThread.__init__(self)
    
    def run(self):
        
        result=protocol.getOnlineFriends()
        
            
        self.emit((result,))
###################################################################
class ThreadGetQunList(PThread):
    """
    获得群列表
    """
    
    def __init__(self):
        PThread.__init__(self)
    
    def run(self):
        
        result=protocol.getQunList()
        
            
        self.emit((result,))


###################################################################
class ThreadSingleLongNick(PThread):
    """
    获得用户好友签名
    """
    
    def __init__(self,):
        PThread.__init__(self)
        
        
    def setFriend(self,uin,friendItem=None):
        
        self.uin=uin
        self.friendItem=friendItem
    
    def run(self):
        
        result=protocol.getSingleLongNick(self.uin)
        
            
        self.emit((result,))

###################################################################
class ThreadQunMemo(PThread):
    """
    获得群公告
    """
    
    def __init__(self,gcodes):
        PThread.__init__(self)
        self.gcodes=gcodes
        
        
    
    def run(self):
        
        result=protocol.getQunMemo(self.gcodes)
        
            
        self.emit((result,))

###################################################################
class ThreadFace(PThread):
    """
    获得头像
    """
    
    def __init__(self,uin,faceType=1):
        PThread.__init__(self)
        self.uin=uin
        self.faceType=faceType
        
        
        
    
    def run(self):
        
        result=protocol.getFace(self.uin, self.faceType)
            
        self.emit((self.uin,self.faceType,result))
