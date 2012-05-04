# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/hang/workspace/atomqq_py/src/Atom/UI/main_loging.ui'
#
# Created: Wed Apr 25 06:11:15 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindowLoging(object):
    def setupUi_login(self, MainWindowLoging):
        MainWindowLoging.setObjectName(_fromUtf8("MainWindowLoging"))
        MainWindowLoging.setWindowModality(QtCore.Qt.NonModal)
        MainWindowLoging.resize(280, 593)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindowLoging.sizePolicy().hasHeightForWidth())
        MainWindowLoging.setSizePolicy(sizePolicy)
        MainWindowLoging.setMinimumSize(QtCore.QSize(280, 0))
        MainWindowLoging.setWindowTitle(QtGui.QApplication.translate("MainWindowLoging", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        MainWindowLoging.setDocumentMode(False)
        self.centralWidget = QtGui.QWidget(MainWindowLoging)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.face = QtGui.QLabel(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.face.sizePolicy().hasHeightForWidth())
        self.face.setSizePolicy(sizePolicy)
        self.face.setMinimumSize(QtCore.QSize(42, 42))
        self.face.setText(QtGui.QApplication.translate("MainWindowLoging", "adsfadsf", None, QtGui.QApplication.UnicodeUTF8))
        self.face.setAlignment(QtCore.Qt.AlignCenter)
        self.face.setObjectName(_fromUtf8("face"))
        self.gridLayout.addWidget(self.face, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setText(QtGui.QApplication.translate("MainWindowLoging", "正在登录...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 4, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 2, 1, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.centralWidget)
        self.progressBar.setProperty("value", 10)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 5, 0, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindowLoging.setCentralWidget(self.centralWidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindowLoging)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindowLoging = QtGui.QMainWindow()
    ui = Ui_MainWindowLoging()
    ui.setupUi(MainWindowLoging)
    MainWindowLoging.show()
    sys.exit(app.exec_())

