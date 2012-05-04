# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from tasks import *
'''
Created on 2012-4-22

@author: hang
'''

###################################################################
#    好友部分
###################################################################
###################################################################





class FriendItem(object):
    
    """
    好友item
    """
    def __init__(self, data=None):
        """
        data=数据
        parent=父类，这里指好友分组
        """
        self.friendData = data
        self.childItems = []
        self.parentItem=None

    def appendChild(self, item):
        """
        作为父类,添加一个子项
        """
        item.setParent(self)
        self.childItems.append(item)
        
    def setParent(self,parentItem=None):
        """
        设置父
        """
        self.parentItem = parentItem

    def child(self, row):
        """
        返回指定位置的子子项
        """
        return self.childItems[row]
    
    def childs(self):
        """
        返回所有子项
        """
        return self.childItems

    def childCount(self):
        """
        返回子项个数
        """
        return len(self.childItems)

    def data(self):
        """
        返回数据
        """
        return self.friendData

    def parent(self):
        """
        返回父类
        """
        
        return self.parentItem
    
    def onlines(self):
        """
        返回在线得好友
        """
        n=0
        for f in self.childItems:
            if f.data().get("online"):
                n+=1
                
        return n
    

    def row(self):
        """
        返回自身所在的行
        """
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

###################################################################
class FriendDelegate(QStyledItemDelegate):
    
    def __init__(self,parent=None):
        QStyledItemDelegate.__init__(self,parent)
        self.parent=parent
    
    def paint(self,painter,option,index):
        item=index.internalPointer()
        if not item.parent():
            return
        
        rect=option.rect
        painter.save()
        
        #好友列表
        if item.parent() and item.parent().data()!='root':
            
            
            
            vrect=QRect(rect)
            vrect.setLeft(0)
            #鼠标悬停
            if option.state & QStyle.State_MouseOver:
                painter.setBrush(QApplication.palette().highlight())
                painter.setPen(QPen(Qt.NoPen))
                painter.drawRect(vrect)
            
            #选中状态
            if option.state & QStyle.State_Selected:
                if option.state & QStyle.State_MouseOver:
                    painter.setBrush(QApplication.palette().highlight())
                    painter.setPen(QPen(Qt.NoPen))
                    painter.drawRect(vrect)
                else:
                    painter.setBrush(QApplication.palette().base())
                    painter.setPen(QPen(Qt.NoPen))
                    painter.drawRect(vrect)
                
            
            
            
            friend = item.data()
            
            online=friend.get("online")
            
            hheight=rect.height()*0.7
            hleft=rect.left()-18
            htop=(rect.height()-hheight)/2+rect.top()
            
            hrect=QRect(hleft,htop,hheight,hheight)
            #画头像
            if not item.data().get("face"):
                head=QImage("Res/img/header.png")
                
                if not item.data().get("_get_face"):
                    item.data()["_get_face"]=True
                    
                    ft=ThreadFace(friend.get("uin"))
                    ft.connect(self.parent, self.parent.processFace)
                    ft.start()
                    
            else:
                head=QImage(friend.get("face"))
            
            painter.drawImage(hrect,head)
            #如果离线
            if not online:
                painter.fillRect(hrect, QColor(255, 255, 255, 170));
            
            
            #画好友昵称
            if friend.get("markname"):
                nickname="%s [%s]"%(friend.get("markname"),friend.get("nick"))
            else :
                nickname=friend.get("nick")
            
            
            nickrect=rect.translated(30,8)
            font = QFont()
            font.setPointSize(10)
            painter.setFont(font)
            
            if friend.get("is_vip"):
                #如果离线
                if not online:
                    pen=QPen(QColor(200,80,80))
                else:
                    pen=QPen(Qt.red)
                    
            else:
                if not online:
                    pen=QPen(QColor(80,80,80))
                else:
                    pen=QPen(Qt.black)
            
            painter.setPen(pen)
            painter.drawText(nickrect, Qt.AlignLeft, nickname)
            
            #画个性签名
            if item.data().get("lnick"):
                
                
                lnick=item.data().get("lnick")
                lnickrect=rect.translated(30,27)
                lnickrect.setRight(rect.right()-10)
                font.setPointSize(9)
                painter.setFont(option.font)
                painter.setPen(QPen(QColor(80,80,80)))
                painter.drawText(lnickrect, Qt.AlignLeft, lnick)
            elif not item.data().get("_get_lnick"):
                item.data()["_get_lnick"]=True
                self.parent.threadSingleLongNick.setFriend(friend.get("uin"))
                self.parent.threadSingleLongNick.start()
                
            painter.restore()
        #如果是分组  
        elif item.parent().data()=='root':
            
            #选中状态
            if option.state & QStyle.State_Selected:
                #焦点离开
                if option.state & QStyle.State_HasFocus:
                    painter.setBrush(QApplication.palette().highlight())
                else:
                    painter.setBrush(QApplication.palette().button())
                painter.setPen(QPen(Qt.NoPen))
                painter.drawRect(rect)
            
            try:
                cname=item.data().get("name")
            except  AttributeError:
                painter.restore()
                return
            cname="%s (%d/%d)"%(cname,item.onlines(),len(item.childs()))
            crect=rect.translated(4,5)
            
            font = QFont()
            font.setPointSize(9)
            painter.setFont(font)
            painter.setPen(QPen(Qt.black))
            painter.drawText(crect, Qt.AlignLeft, cname)
            painter.restore()
        #QApplication.style().drawItemText(painter,option.rect,Qt.AlignLeft,option.palette,True,item.data(),QPalette.Highlight) 
    
    def sizeHint(self, option, index):
        item =index.internalPointer()
        
        size=option.decorationSize
        size.setHeight(26)
        
        if item.parent() and item.parent().data()!='root':
            size.setHeight(56)
            return size
        
        return size
    
###################################################################
class FriendListModel(QAbstractItemModel):
    
    
    
    """
    好友模型
    """
    def __init__(self,parent=None):
        super(FriendListModel,self).__init__(parent)
        
        froot=FriendItem('root')
        
        c1=FriendItem({"index":0,"sort":0,"name":u"正在加载..."})
        froot.appendChild(c1)
        self.rootItem=froot
        
        pass
    
    def setFriendData(self,data):
        """
        设置数据源
        """
        self.rootItem=data
        self.layoutChanged.emit()
    
    def columnCount(self,parent=QModelIndex()):
        """
        返回列数
        """
        return 1
    
    def rowCount(self, parent=QModelIndex()):
        """
        这个方法返回了数据的行数
        也就是有多少个条目得数据
        """
        
        if not parent.isValid():
            parentItem=self.rootItem
        else:
            parentItem=parent.internalPointer()
        
        return parentItem.childCount()

    def data(self,index,role=Qt.DisplayRole):
        """
        根据当前index索引，返回当前的数据
        然后再由Qt进行渲染显示
        """
        if not index.isValid():  
            return None  
        if role != Qt.DisplayRole:  
            return None  
        
        item = index.internalPointer()  
        return QVariant(item.data()) 
    
    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()
    
    def getData(self):
        return self.rootItem
    
    def parent(self, index):
        """
        返回父索引
        """
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)
    
###################################################################

class SortProxyModel(QSortFilterProxyModel):
    """
    排序代理
    """
    
    def __init__(self, parent = None):
        QSortFilterProxyModel.__init__(self, parent)
    
    
    def lessThan11(self,left_index,right_index):
        """
        比较方法
        用于判断紧邻的两个数据的大小
        """

        return 0<1

        #获取相邻的两个QVariant对象
        left_var=left_index.internalPointer()
        
        if left_var.parent() and left_var.parent().data()!='root':
            return False
        
        right_var=right_index.internalPointer()

        #转化为Python对象
        left_str=left_var.toPyObject()
        right_str=right_var.toPyObject()

        friendL=left_str.data().get("online")
        friendR=right_str.data().get("online")
        
        if friendL:
            left_int=1
        else:
            left_int=0
        
        if friendR:
            right_int=1
        else:
            right_int=0

        #从方法名已经看出来，只要返回左是否比右小的bool值就行
        return left_int < right_int

###################################################################
#    群部分
###################################################################
###################################################################
###################################################################
class QunDelegate(QStyledItemDelegate):
    
    def __init__(self,parent=None):
        QStyledItemDelegate.__init__(self,parent)
        self.parent=parent
    
    def paint(self,painter,option,index):
        item=index.internalPointer()
        if not item.parent():
            return
        
        rect=option.rect
        painter.save()
        
        #群列表
        if item.parent() and item.parent().data()!='root':
            
            
            
            vrect=QRect(rect)
            vrect.setLeft(0)
            #鼠标悬停
            if option.state & QStyle.State_MouseOver:
                painter.setBrush(QApplication.palette().highlight())
                painter.setPen(QPen(Qt.NoPen))
                painter.drawRect(vrect)
            
            #选中状态
            if option.state & QStyle.State_Selected:
                if option.state & QStyle.State_MouseOver:
                    painter.setBrush(QApplication.palette().highlight())
                    painter.setPen(QPen(Qt.NoPen))
                    painter.drawRect(vrect)
                else:
                    painter.setBrush(QApplication.palette().base())
                    painter.setPen(QPen(Qt.NoPen))
                    painter.drawRect(vrect)
                
            
            
            
            friend = item.data()
            
            hheight=rect.height()*0.7
            hleft=rect.left()-18
            htop=(rect.height()-hheight)/2+rect.top()
            
            hrect=QRect(hleft,htop,hheight,hheight)
            #画头像
            if not item.data().get("face"):
                head=QImage("Res/img/header.png")
                
                if not item.data().get("_get_face"):
                    item.data()["_get_face"]=True
                    
                    ft=ThreadFace(friend.get("code"),4)
                    ft.connect(self.parent, self.parent.processFace)
                    ft.start()
                    
            else:
                head=QImage(friend.get("face"))
            
            painter.drawImage(hrect,head)
            
            
            #画好友昵称
            if friend.get("markname"):
                nickname="%s [%s]"%(friend.get("markname"),friend.get("nick"))
            else :
                nickname=friend.get("name")
            
            
            nickrect=rect.translated(30,8)
            font = QFont()
            font.setPointSize(10)
            painter.setFont(font)
            
            painter.setPen(QPen(Qt.black))
            painter.drawText(nickrect, Qt.AlignLeft, nickname)
            
            #画群通知
            if item.data().get("memo"):
                lnick=item.data().get("memo")
                lnickrect=rect.translated(30,27)
                lnickrect.setRight(rect.right()-10)
                font.setPointSize(9)
                painter.setFont(option.font)
                painter.setPen(QPen(QColor(80,80,80)))
                painter.drawText(lnickrect, Qt.AlignLeft, lnick)
                
            painter.restore()
        #如果是分组  
        elif item.parent().data()=='root':
            
            #选中状态
            if option.state & QStyle.State_Selected:
                #焦点离开
                if option.state & QStyle.State_HasFocus:
                    painter.setBrush(QApplication.palette().highlight())
                else:
                    painter.setBrush(QApplication.palette().button())
                painter.setPen(QPen(Qt.NoPen))
                painter.drawRect(rect)
            
            try:
                cname=item.data().get("name")
            except  AttributeError:
                painter.restore()
                return
            cname
            crect=rect.translated(4,5)
            
            font = QFont()
            font.setPointSize(9)
            painter.setFont(font)
            painter.setPen(QPen(Qt.black))
            painter.drawText(crect, Qt.AlignLeft, cname)
            painter.restore()
        #QApplication.style().drawItemText(painter,option.rect,Qt.AlignLeft,option.palette,True,item.data(),QPalette.Highlight) 
    
    def sizeHint(self, option, index):
        item =index.internalPointer()
        
        size=option.decorationSize
        size.setHeight(26)
        
        if item.parent() and item.parent().data()!='root':
            size.setHeight(56)
            return size
        
        return size