# -*- coding: utf-8 -*-

"""
登录窗口
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *


from UI.Ui_login import Ui_LoginWindow
from taskpoll import PThreadProcess,PThread


class LoginWindow(QDialog, Ui_LoginWindow,PThreadProcess):
    
    """
    登录窗口
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        PThreadProcess.__init__(self)
        
        self.parent=parent
        
        self.setupUi(self)
        self.setCheckAreaVisibale(False)

        #开始论讯
        self.startPoll()
        
        self.threadGetCodeStr=ThreadGetCodeStr()
        self.threadGetCodeStr.connect(self,self.processCodeResult)
        
        self.threadGetCodeImg=ThreadGetCodeImg()
        self.threadGetCodeImg.connect(self,self.processImgResult)
        
        self.threadPreLogin=ThreadPreLogin()
        self.threadPreLogin.connect(self,self.processPreLoginResult)
       
    
    @pyqtSignature("QString")
    def on_qqnum_editTextChanged(self, uin):
        """
        用户编辑qq号
        """
        self.btnLogin.setEnabled(False)
        self.loginMsg.setText('')
        self.threadGetCodeStr.setUin(self.qqnum.currentText())
        self.threadGetCodeStr.start()

    @pyqtSignature("QString")
    def on_qqnum_currentIndexChanged(self, uin):
        """
        用户选择qq号
        """
        pass
    
    
    @pyqtSignature("bool")
    def on_cbxRemeberPasswd_clicked(self, checked):
        """
        记住密码状态改变
        """
        if checked is False:
            self.cbxAutoLogin.setChecked(False)
            
 
    
    @pyqtSignature("bool")
    def on_cbxAutoLogin_clicked(self, checked):
        """
        自动登录状态改变
        """
        if checked is True:
            self.cbxRemeberPasswd.setChecked(True)
    
    @pyqtSignature("")
    def on_btnSetting_clicked(self):
        """
        设置
        """
        pass
    
    @pyqtSignature("")
    def on_btnLogin_clicked(self):
        """
        登录
        """
        self.parent.setupUi_login(self.parent)
        self.parent.face.setPixmap(QPixmap(self.facePath))
        self.parent.setVisible(True)
        self.setVisible(False)
        self.btnLogin.setEnabled(False)
        self.threadPreLogin.setUinPaCode(self.qqnum.currentText(), self.qqpasswd.text(), self.checkCode.text())
        self.threadPreLogin.start()
        
    @pyqtSignature("QString")
    def on_changeImg_linkActivated(self,link):
        self.btnLogin.setEnabled(False)
        self.threadGetCodeImg.setUinCode(self.qqnum.currentText(), self.md5Check)
        self.threadGetCodeImg.start()
    
    
    

    def processCodeResult(self,rcode,code):
        """
        处理获取得验证码
        rcode 验证码标志
        code 验证码本体
        """
        
        if rcode=='0':
            self.btnLogin.setEnabled(True)
            self.setCheckAreaVisibale(False)
            self.checkCode.setText(code)
        else:
            self.md5Check=code
            self.btnLogin.setEnabled(False)
            self.threadGetCodeImg.setUinCode(self.qqnum.currentText(), code)
            self.threadGetCodeImg.start()
            
    def processImgResult(self,pic):
        """
        处理获取得图片验证码
        """
        self.checkImg.setPixmap(QPixmap(pic))
        self.checkCode.setText("")
        self.setCheckAreaVisibale(True)
        self.btnLogin.setEnabled(True)
        
    def processPreLoginResult(self,rcode,r):
        """
        处理握手登录
        """
        
        if rcode != '0':
            self.parent.setVisible(False)
            self.setVisible(True)
            
            self.btnLogin.setEnabled(False)
            self.threadGetCodeStr.setUin(self.qqnum.currentText())
            self.threadGetCodeStr.start()
            
            self.loginMsg.setText('<font color=red>%s</font>'%r)
        else:
            #登录握手成功
            self.parent.processLoginResult(self.facePath,self.qqnum.currentText(),self.loginStatus.currentText())
        
class ThreadGetCodeStr(PThread):
    """
    线程 获取文字验证码
    """
    
    def __init__(self):
        PThread.__init__(self)
        
    
    def setUin(self,uin):
        self.uin=uin
    
    def run(self):
        from Tencent.WebQQ.protocol import Login
        login=Login()
        rcode,code=login.getCheckCode(self.uin)
        self.emit((rcode,code))
        
class ThreadGetCodeImg(PThread):
    """
    线程 获取图片验证码
    """
    def __init__(self):
        PThread.__init__(self)
        
    
    def setUinCode(self,uin,code):
        self.uin=uin
        self.code=code
    
    def run(self):
        from Tencent.WebQQ.protocol import Login
        login=Login()
        img=login.getCheckImg(self.uin, self.code)
        self.emit((img,))
        
class ThreadPreLogin(PThread):
    """
    线程 握手登录
    """
    
    def __init__(self):
        PThread.__init__(self)
        
    
    def setUinPaCode(self,uin,passwd,code):
        self.uin=uin
        self.passwd=passwd
        self.code=code
    
    def run(self):
        from Tencent.WebQQ.protocol import Login
        login=Login()
        rcode,r=login.login(self.uin,self.passwd,self.code)
        
        self.emit((rcode,unicode(r,'utf-8')))
        
    
if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = LoginWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    
