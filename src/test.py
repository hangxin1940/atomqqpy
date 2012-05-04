# -*- coding: utf-8 -*-
"""
这个是个截图的demo
目前只是实现了区域的截取，但qt好像不能将bitmap数组直接存入剪贴板
"""

import sys 
# too lazy to keep track of QtCore or QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import * 
class MoviePlayer(QWidget): 
    def __init__(self, parent=None): 
        QWidget.__init__(self, parent) 
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("QMovie to show animated gif")
        
        # set up the movie screen on a label
        self.movie_screen = QLabel()
        # expand and center the label 
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, 
            QSizePolicy.Expanding)        
        self.movie_screen.setAlignment(Qt.AlignCenter) 
        btn_start = QPushButton("Start Animation")
        self.connect(btn_start, SIGNAL("clicked()"), self.start) 
        btn_stop = QPushButton("Stop Animation")
        self.connect(btn_stop, SIGNAL("clicked()"), self.stop)        
        main_layout = QVBoxLayout() 
        main_layout.addWidget(self.movie_screen)
        main_layout.addWidget(btn_start) 
        main_layout.addWidget(btn_stop)
        self.setLayout(main_layout) 
                
        # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QMovie("/home/hang/workspace/atomqq_py/src/AG_Dog.gif", QByteArray(), self) 
        self.movie.setCacheMode(QMovie.CacheAll) 
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        #self.movie.start()
        
    def start(self):
        """sart animnation"""
        self.movie.start()
        
    def stop(self):
        """stop the animation"""
        self.movie.stop()
        
        
if __name__ == "__main__11":
    app = QApplication(sys.argv) 
    player = MoviePlayer() 
    player.show() 
    sys.exit(app.exec_())
    
#################################################    
class F(QLabel): 
    def __init__(self, parent=None): 
        QLabel.__init__(self, parent)   
        
        self.originalPixmap = QPixmap.grabWindow(QApplication.desktop().winId())
        self.setPixmap(self.originalPixmap)
if __name__ == "__main__2":
    app = QApplication(sys.argv) 
    shot = F() 
    shot.show() 
    sys.exit(app.exec_())    


############################################
from PyQt4 import QtGui, QtCore

class AtomSnapShot(QtGui.QWidget):
    """
    截图
    """
    def __init__(self):
        QWidget.__init__(self)
        #获取一份截图
        self.screenPixmap = QPixmap.grabWindow(QApplication.desktop().winId())
        
        self.initUI()
        
    def initUI(self):      
        """
        初始化UI
        """
        self.setWindowTitle(u"Atom截图")
        
        self.pressed=False
        self.prect=None
        self.moved=False
        
        
        #真 全屏
        self.showFullScreen()




    def paintEvent(self, event):
        """
        画布事件
        """
        
        qp = QtGui.QPainter()
        qp.begin(self)
                
        self.drawScreenShot(qp)
        qp.end()
    
    def mousePressEvent(self, event):
        """
        鼠标按下事件
        """
        if event.button()==Qt.LeftButton:
            self.pressed=False
            
            #如果已经选择好矩形,并且鼠标在矩形内，则进入拖动模式
            if self.prect and self.prect.contains(event.pos()):
                self.moved=True
                self.lastMove=event.pos()
            else:
                self.pressed=True
                #获得鼠标坐标
                self.pStart=event.pos()
            
        elif event.button()==Qt.RightButton:
            if self.prect:
                self.pressed=False
                self.prect=None
                self.repaint()
            else:
                self.close()
            
        return QtGui.QWidget.mousePressEvent(self, event)
    
    def mouseMoveEvent(self, event):
        """
        鼠标移动事件
        """
        #如果拖动模式
        if self.moved:
            
            x=event.x()-self.lastMove.x()
            y=event.y()-self.lastMove.y()
            
            offsetX=self.prect.x()+x
            offsetY=self.prect.y()+y
            if 0>offsetX :
                offsetX=0
            if 0>offsetY :
                offsetY=0
            if offsetX+self.prect.width()>self.width():
                offsetX=self.prect.x()
            if offsetY+self.prect.height()>self.height():
                offsetY=self.prect.y()
                
            self.lastMove=event.pos()
            self.prect.moveTopLeft(QPoint(offsetX,offsetY))
            self.repaint()
        
        #如果画图模式
        elif self.pressed :
            #生成矩形
            self.prect=QRect(self.pStart,event.pos())
            self.repaint()
        
            
           
            
        return QtGui.QWidget.mouseMoveEvent(self, event)
    
    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件
        """
        self.pressed=False
        self.moved=False
        if event.button()==Qt.RightButton:
            self.prect=None
            self.repaint()
        return QtGui.QWidget.mouseReleaseEvent(self, event)
       
    def keyPressEvent(self, event):
        """
        键盘事件
        """
        if event.key() == Qt.Key_Escape:
            self.close()
        return QtGui.QWidget.keyPressEvent(self,event)
    def mouseDoubleClickEvent(self, event):
        """
        双击完成
        """
        if self.prect:
            #生成截图
            target=self.screenPixmap.copy(self.prect)
            clipboard=QApplication.clipboard()
            #放进系统剪贴板
            #clipboard.setPixmap(target)
            #clipboard.setText("fasdf")
            clipboard.setImage(target.toImage())
            
        self.close()
        
        return QtGui.QWidget.mouseDoubleClickEvent(self, event)
    
    def drawScreenShot(self, painter):
        """
        画屏幕截图与用户选择的区域
        """
        
        #首先画截图背景
        painter.drawPixmap(0,0,self.screenPixmap)    
        #然画框框
        if self.pressed or self.moved:
            
            
            painter.setPen(Qt.red)
            painter.drawRect(self.prect)
            font = QFont()
            font.setPointSize(10)
            painter.setFont(font)
            text=u"双击确认[%d,%d],[%dx%d]"%(self.prect.x(),self.prect.y(),self.prect.width(),self.prect.height())
            trect=QRect(self.prect.bottomRight(),QSize(500,20))
            painter.drawText(trect, Qt.AlignLeft, text)
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = AtomSnapShot()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   
    
