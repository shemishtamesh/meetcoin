# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerOodcsy.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.SendButton = QPushButton(self.centralwidget)
        self.SendButton.setObjectName(u"SendButton")
        self.SendButton.setGeometry(QRect(110, 290, 93, 28))
        self.Text = QTextBrowser(self.centralwidget)
        self.Text.setObjectName(u"Text")
        self.Text.setGeometry(QRect(370, 290, 256, 192))
        self.Lable = QLabel(self.centralwidget)
        self.Lable.setObjectName(u"Lable")
        self.Lable.setGeometry(QRect(370, 260, 101, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.SendButton.setText(QCoreApplication.translate("MainWindow", u"send data", None))
        self.Lable.setText(QCoreApplication.translate("MainWindow", u"received data", None))
    # retranslateUi

