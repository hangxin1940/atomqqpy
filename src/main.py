from Atom.mainwindow import *

if __name__=='__main__':
    from PyQt4.QtGui import *
    import sys
    
    app=QApplication(sys.argv)
    login=MainWindow()
    login.showLoginDialog()
    sys.exit(app.exec_())
