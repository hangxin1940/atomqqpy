# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from UI.Ui_main import Ui_MainWindow
from UI.Ui_main_loging import Ui_MainWindowLoging

from qqmodel import *
from Atom.loginwindow import LoginWindow
from taskpoll import PThreadProcess
from tasks import *

class MainWindow(QMainWindow, Ui_MainWindow,Ui_MainWindowLoging,PThreadProcess):
    """
    主程序，qq面板
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        PThreadProcess.__init__(self)
        
        self.setupUi_login(self)
        self.setWindowTitle(u"AtomQQ")
        
        # 得到桌面控件
        desktop = QApplication.desktop()
        # 得到屏幕可显示尺寸
        rectScr = desktop.availableGeometry()
        rectMain=self.geometry()
        rectMain.moveTo(rectScr.width()-rectMain.width(),rectMain.y())
        
        self.setGeometry(rectMain)
        
        self.show()
        self.setVisible(False)
        self.startPoll()
        
        
        
        
    def showLoginDialog(self):
        """
        显示登录窗口
        """
        self.login=LoginWindow(self)
        self.login.show()
        
    
    def processLoginResult(self,face,uin,status):
        """
        处理单手登录
        """
        
        
        channel=ThreadLoginChannel(uin,status)
        channel.connect(self, self.processLoginChannel)
        channel.start()
        
        
        
    def processLoginChannel(self,faild,result):
        """
        登录成功
        """
        
        #登录失败
        if not faild:
            self.setVisible(False)
            self.login.show()
            return
        
        
        facePath=self.face.pixmap()
        self.login.close()
        self.setupUi(self)
        
        self.userInfo={}
        self.uin=str(result.get("uin"))
        self.lbUserName.setText(self.uin)
        self.imgUserFace.setPixmap(facePath)
        
        
        
        #设置好友mvc
        self.friendModel = FriendListModel()
        self.friendDelegate= FriendDelegate(self)
        
        #设置排序代理
        self.sortProxy=SortProxyModel()
        self.sortProxy.setSourceModel(self.friendModel)
        self.sortProxy.sort(0)
        
        self.twFriends.setModel(self.friendModel)
        self.twFriends.setItemDelegate(self.friendDelegate)
        
        #设置群mvc
        self.qunModel = FriendListModel()
        self.qunDelegate= QunDelegate(self)
        
        self.twQun.setModel(self.qunModel)
        self.twQun.setItemDelegate(self.qunDelegate)
        
        #获取当前登录账户得信息
        self.threadGetUserInfo=ThreadGetFriendInfo(self.uin)
        self.threadGetUserInfo.connect(self,self.processUserInfo)
        self.threadGetUserInfo.start()
        
        #获得账户签名
        self.threadSingleLongNick=ThreadSingleLongNick()
        self.threadSingleLongNick.setFriend(self.uin)
        self.threadSingleLongNick.connect(self, self.processSingleLongNick)
        self.threadSingleLongNick.start()
        
        #获得头像
        self.friendsFace={}
        self.threadFace=ThreadFace(self.uin)
        self.threadFace.connect(self, self.processFace)
        self.threadFace.start()
        
        #获取好友列表
        self.threadGetFriendList=ThreadGetFriendList()
        self.threadGetFriendList.connect(self, self.processFriendList)
        self.threadGetFriendList.start()
        
        #获取群列表
        self.threadGetQunList=ThreadGetQunList()
        self.threadGetQunList.connect(self, self.processQunList)
        self.threadGetQunList.start()
        ######################################################
        #icon = QIcon('Res.img.header.jpg')
        
        #tryIcon=QSystemTrayIcon(self)
        #tryIcon.setIcon(icon)
        #tryIcon.show()
        #tryIcon.showMessage(u"提示",u"您有新的任务，请注意查收")
        
    def processUserInfo(self,infos):      
        """
        处理当前用户信息
        """
        
        rcode=infos.get("retcode")
        
        if rcode == 0:
            #设置用户信息
            self.userInfo.update(infos.get("result"))
            self.lbUserName.setText(self.userInfo.get("nick"))
            
        else:
            print infos
    
    def processSingleLongNick(self,infos):      
        """
        处理用户签名
        """
        
        rcode=infos.get("retcode")
        
        if rcode == 0:
            
            lnick=infos.get("result")[0]
            uin=lnick.get("uin")
            
            
            if str(uin)==str(self.uin):
                
                #给当前用户设置
                self.userInfo["lnick"]=lnick.get("lnick")
                self.lbUserNick.setText(lnick.get("lnick"))
            else:
                lnick=lnick.get("lnick")
                index=self.friendDict.get(str(uin))
                
                root=self.friendModel.getData()
                
                cate= root.childs()[index[0]]
                chil=cate.childs()[index[1]]
                chil.data()["lnick"]=lnick
                self.friendModel.layoutChanged.emit()
            
            
        else:
            print infos
            
    
    def processFace(self,uin,facetype,infos):      
        """
        处理头像
        """
        self.friendsFace[uin]=infos
        #如果是登录用户
        if str(uin)==str(self.uin):
            
            if infos is False:
                #设置默认头像
                pass
            else:
                #设置头像
                print infos
                face=QPixmap(infos)
                self.imgUserFace.setPixmap(face)
        else:
            
            #设置好友头像
            if facetype==1:
                if infos is False:
                    #设置默认头像
                    pass
                else:
                    #设置头像
                    index=self.friendDict.get(str(uin))
                    
                    root=self.friendModel.getData()
                    
                    cate= root.childs()[index[0]]
                    chil=cate.childs()[index[1]]
                    chil.data()["face"]=infos
                    self.friendModel.layoutChanged.emit()
            #设置群头像
            elif facetype==4:
                if infos is False:
                    #设置默认头像
                    pass
                else:
                    index=self.qunDict.get(str(uin))
                    root=self.qunModel.getData()
                    cate= root.childs()[0]
                    chil=cate.childs()[index]
                    chil.data()["face"]=infos
                    self.qunModel.layoutChanged.emit()
                    
    
    def processFriendList(self,result):
        """
        处理好友列表
        """
        rcode=result.get("retcode")
        if rcode==0:
            flist= result.get("result")
            
            #组装好友
            froot=FriendItem("root")
            
            friends=flist.get("friends")
            marknames=flist.get("marknames")
            vipinfo=flist.get("vipinfo")
            info=flist.get("info")
            
            categories=flist.get("categories")
            
            #如果默认分组(我的好友)没有更改
            hasIndex0=False
            for c in categories:
                if c.get("index")==0:
                    hasIndex0=True
                    break
            
            if not hasIndex0:
                index0={"index":0,"sort":0,"name":u"我的好友"}
                categories.append(index0)
                
                
            #生成分组
            for category in categories:
                ca=FriendItem(category)
                froot.appendChild(ca)
            
            #生成好友
            for friend in friends:
                uin=friend.get("uin")
                
                
                
                
                for markname in marknames:
                    if markname.get("uin") == uin:
                        friend.update(markname)
                        marknames.remove(markname)
                        break
                
                for vip in vipinfo:
                    if vip.get("u")==uin:
                        del vip["u"]
                        friend.update(vip)
                        vipinfo.remove(vip)
                        break
                    
                for inf in info:
                    if inf.get("uin")==uin:
                        friend.update(inf)
                        info.remove(inf)
                        break
                
                friend["face"]=False
                item=FriendItem(friend) 
                
                
                for cat in froot.childs():
                    if cat.data().get("index")==friend.get("categories"):
                        cat.appendChild(item)
                        break;
                    
                    
            self.friendListData=froot
            self.friendModel.setFriendData(self.friendListData)
            
            #建立一个好友索引
            self.friendDict={}
            
            i=0
            for item in froot.childs():
                j=0
                for child in item.childs():
                    uin=str(child.data()["uin"])
                    self.friendDict[uin]=[i,j]
                    j+=1
                i+=1
            
            #获取在线好友
            self.threadGetOnlineFriends=ThreadGetOnlineFriends()
            self.threadGetOnlineFriends.connect(self, self.processOnlineFriends)
            self.threadGetOnlineFriends.start()
            
    def processOnlineFriends(self,result):
        """
        处理在线好友
        """
        rcode=result.get("retcode")
        
        if rcode == 0:
            
            onlines=result.get("result")
            for friend in onlines:
                uin=friend.get("uin")
                index=self.friendDict.get(str(uin))
                    
                root=self.friendModel.getData()
                
                cate= root.childs()[index[0]]
                chil=cate.childs()[index[1]]
                chil.data().update(friend)
                chil.data()["online"]=True
                self.qunModel.layoutChanged.emit()
                
            #self.twFriends.setModel(self.sortProxy)
            #self.twFriends.setSortingEnabled(True)
        
    def processQunList(self,result):
        """
        处理群列表
        """
        rcode=result.get("retcode")
        if rcode==0:
            qlist= result.get("result")
            
            
            qroot=FriendItem("root")
            
            
            qun=FriendItem({u"name":u"群列表"})
            
            qroot.appendChild(qun)
            
            nameList=qlist.get("gnamelist")
            markList=qlist.get("gmarklist")
            
            for mark in markList:
                uin=mark.get("uin")
                for name in nameList:
                    code=name.get("code")
                    if uin==code:
                        nameList.get("code")["markname"]=mark.get("markname")
            
            for q in nameList:
                qunItem=FriendItem(q)
                qun.appendChild(qunItem)
            
            self.qunListData=qroot
            self.qunModel.setFriendData(self.qunListData)
            
            #建立一个群索引
            self.qunDict={}
            
            tempQun=[]
            for item in qroot.childs():
                j=0
                for child in item.childs():
                    uin=child.data()["code"]
                    tempQun.append(uin)
                    self.qunDict[str(uin)]=j
                    j+=1
                
            
            #获取群公告
            self.threadQunMemo=ThreadQunMemo(tempQun)
            self.threadQunMemo.connect(self,self.processQunMemo)
            self.threadQunMemo.start()
                
    def processQunMemo(self,result):
        """
        处理群公告
        """
        rcode=result.get("retcode")
        if rcode==0:
            codes= result.get("result")
            
            
            for memo in codes:
                code=memo.get("gcode")
                index=self.qunDict.get(str(code))
                    
                root=self.qunModel.getData()
                
                cate= root.childs()[0]
                chil=cate.childs()[index]
                chil.data()["memo"]=memo.get("memo")
                self.friendModel.layoutChanged.emit()
            
###################################################################


if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())