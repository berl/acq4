# -*- coding: utf-8 -*-
from RackTemplate import *
from PyQt4 import QtCore, QtGui

class MCRackGui(QtGui.QWidget):
    def __init__(self, dev):
        QtGui.QWidget.__init__(self)
        self.dev = dev
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.hostText.setText(dev.config['channelID'])
        
