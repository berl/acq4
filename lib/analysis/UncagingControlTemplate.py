# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UncagingControlTemplate.ui'
#
# Created: Wed Sep 15 03:08:15 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_UncagingControlWidget(object):
    def setupUi(self, UncagingControlWidget):
        UncagingControlWidget.setObjectName("UncagingControlWidget")
        UncagingControlWidget.resize(379, 232)
        self.gridLayout_4 = QtGui.QGridLayout(UncagingControlWidget)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(UncagingControlWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.thresholdSpin = QtGui.QDoubleSpinBox(UncagingControlWidget)
        self.thresholdSpin.setObjectName("thresholdSpin")
        self.gridLayout.addWidget(self.thresholdSpin, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(UncagingControlWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.directTimeSpin = QtGui.QDoubleSpinBox(UncagingControlWidget)
        self.directTimeSpin.setObjectName("directTimeSpin")
        self.gridLayout.addWidget(self.directTimeSpin, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(UncagingControlWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.poststimTimeSpin = QtGui.QDoubleSpinBox(UncagingControlWidget)
        self.poststimTimeSpin.setObjectName("poststimTimeSpin")
        self.gridLayout.addWidget(self.poststimTimeSpin, 2, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.groupBox_4 = QtGui.QGroupBox(UncagingControlWidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox_4)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gradientRadio = QtGui.QRadioButton(self.groupBox_2)
        self.gradientRadio.setObjectName("gradientRadio")
        self.gridLayout_3.addWidget(self.gradientRadio, 0, 0, 1, 2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.colorSpin1 = QtGui.QDoubleSpinBox(self.groupBox_2)
        self.colorSpin1.setObjectName("colorSpin1")
        self.horizontalLayout_2.addWidget(self.colorSpin1)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.colorSpin3 = QtGui.QDoubleSpinBox(self.groupBox_2)
        self.colorSpin3.setMaximum(100.0)
        self.colorSpin3.setObjectName("colorSpin3")
        self.horizontalLayout_3.addWidget(self.colorSpin3)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 2, 0, 1, 2)
        self.gradientWidget = GradientWidget(self.groupBox_2)
        self.gradientWidget.setObjectName("gradientWidget")
        self.gridLayout_3.addWidget(self.gradientWidget, 3, 0, 1, 2)
        self.rgbRadio = QtGui.QRadioButton(self.groupBox_2)
        self.rgbRadio.setObjectName("rgbRadio")
        self.gridLayout_3.addWidget(self.rgbRadio, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 4, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.gridLayout_4.addWidget(self.groupBox_4, 0, 1, 2, 1)
        self.groupBox = QtGui.QGroupBox(UncagingControlWidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.eventFindRadio = QtGui.QRadioButton(self.groupBox)
        self.eventFindRadio.setObjectName("eventFindRadio")
        self.gridLayout_2.addWidget(self.eventFindRadio, 0, 0, 1, 1)
        self.chargeTransferRadio = QtGui.QRadioButton(self.groupBox)
        self.chargeTransferRadio.setObjectName("chargeTransferRadio")
        self.gridLayout_2.addWidget(self.chargeTransferRadio, 1, 0, 1, 1)
        self.useSpontActCheck = QtGui.QCheckBox(self.groupBox)
        self.useSpontActCheck.setObjectName("useSpontActCheck")
        self.gridLayout_2.addWidget(self.useSpontActCheck, 2, 0, 1, 1)
        self.medianCheck = QtGui.QCheckBox(self.groupBox)
        self.medianCheck.setObjectName("medianCheck")
        self.gridLayout_2.addWidget(self.medianCheck, 3, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 1, 0, 1, 1)
        self.recolorBtn = QtGui.QPushButton(UncagingControlWidget)
        self.recolorBtn.setObjectName("recolorBtn")
        self.gridLayout_4.addWidget(self.recolorBtn, 2, 0, 1, 2)

        self.retranslateUi(UncagingControlWidget)
        QtCore.QMetaObject.connectSlotsByName(UncagingControlWidget)

    def retranslateUi(self, UncagingControlWidget):
        UncagingControlWidget.setWindowTitle(QtGui.QApplication.translate("UncagingControlWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("UncagingControlWidget", "Noise Threshold", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("UncagingControlWidget", "Direct Time", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("UncagingControlWidget", "Post-Stim. Time", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("UncagingControlWidget", "Coloring Scheme:", None, QtGui.QApplication.UnicodeUTF8))
        self.gradientRadio.setText(QtGui.QApplication.translate("UncagingControlWidget", "Gradient", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("UncagingControlWidget", "Low % Cutoff", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("UncagingControlWidget", "High % Cutoff", None, QtGui.QApplication.UnicodeUTF8))
        self.rgbRadio.setText(QtGui.QApplication.translate("UncagingControlWidget", "RGB", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("UncagingControlWidget", "Analysis Method:", None, QtGui.QApplication.UnicodeUTF8))
        self.eventFindRadio.setText(QtGui.QApplication.translate("UncagingControlWidget", "Event Finding", None, QtGui.QApplication.UnicodeUTF8))
        self.chargeTransferRadio.setText(QtGui.QApplication.translate("UncagingControlWidget", "Total Charge Transfer", None, QtGui.QApplication.UnicodeUTF8))
        self.useSpontActCheck.setText(QtGui.QApplication.translate("UncagingControlWidget", "Use Spont. Activity", None, QtGui.QApplication.UnicodeUTF8))
        self.medianCheck.setText(QtGui.QApplication.translate("UncagingControlWidget", "Use Median", None, QtGui.QApplication.UnicodeUTF8))
        self.recolorBtn.setText(QtGui.QApplication.translate("UncagingControlWidget", "Re-Color", None, QtGui.QApplication.UnicodeUTF8))

from pyqtgraph.GradientWidget import GradientWidget
