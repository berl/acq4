# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProtocolTemplate.ui'
#
# Created: Tue Dec 29 11:48:53 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(302, 377)
        Form.setAutoFillBackground(True)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter_2 = QtGui.QSplitter(Form)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_2 = QtGui.QFrame(self.layoutWidget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.icModeRadio = QtGui.QRadioButton(self.frame_2)
        self.icModeRadio.setObjectName("icModeRadio")
        self.horizontalLayout_2.addWidget(self.icModeRadio)
        self.i0ModeRadio = QtGui.QRadioButton(self.frame_2)
        self.i0ModeRadio.setChecked(True)
        self.i0ModeRadio.setObjectName("i0ModeRadio")
        self.horizontalLayout_2.addWidget(self.i0ModeRadio)
        self.vcModeRadio = QtGui.QRadioButton(self.frame_2)
        self.vcModeRadio.setObjectName("vcModeRadio")
        self.horizontalLayout_2.addWidget(self.vcModeRadio)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.holdingCheck = QtGui.QCheckBox(self.frame_2)
        self.holdingCheck.setObjectName("holdingCheck")
        self.horizontalLayout_6.addWidget(self.holdingCheck)
        self.holdingSpin = QtGui.QDoubleSpinBox(self.frame_2)
        self.holdingSpin.setMinimum(-1000000.0)
        self.holdingSpin.setMaximum(1000000.0)
        self.holdingSpin.setObjectName("holdingSpin")
        self.horizontalLayout_6.addWidget(self.holdingSpin)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_6)
        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.primarySignalCheck = QtGui.QCheckBox(self.layoutWidget)
        self.primarySignalCheck.setObjectName("primarySignalCheck")
        self.gridLayout.addWidget(self.primarySignalCheck, 0, 0, 1, 1)
        self.secondarySignalCheck = QtGui.QCheckBox(self.layoutWidget)
        self.secondarySignalCheck.setObjectName("secondarySignalCheck")
        self.gridLayout.addWidget(self.secondarySignalCheck, 1, 0, 1, 1)
        self.primarySignalCombo = QtGui.QComboBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.primarySignalCombo.sizePolicy().hasHeightForWidth())
        self.primarySignalCombo.setSizePolicy(sizePolicy)
        self.primarySignalCombo.setMinimumSize(QtCore.QSize(40, 0))
        self.primarySignalCombo.setObjectName("primarySignalCombo")
        self.primarySignalCombo.addItem(QtCore.QString())
        self.gridLayout.addWidget(self.primarySignalCombo, 0, 1, 1, 1)
        self.secondarySignalCombo = QtGui.QComboBox(self.layoutWidget)
        self.secondarySignalCombo.setMinimumSize(QtCore.QSize(40, 0))
        self.secondarySignalCombo.setObjectName("secondarySignalCombo")
        self.secondarySignalCombo.addItem(QtCore.QString())
        self.gridLayout.addWidget(self.secondarySignalCombo, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 2, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.setSecondaryGainCheck = QtGui.QCheckBox(self.layoutWidget)
        self.setSecondaryGainCheck.setObjectName("setSecondaryGainCheck")
        self.horizontalLayout_7.addWidget(self.setSecondaryGainCheck)
        self.secondaryGainSpin = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.secondaryGainSpin.setObjectName("secondaryGainSpin")
        self.horizontalLayout_7.addWidget(self.secondaryGainSpin)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 2, 1, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.setPrimaryGainCheck = QtGui.QCheckBox(self.layoutWidget)
        self.setPrimaryGainCheck.setObjectName("setPrimaryGainCheck")
        self.horizontalLayout_5.addWidget(self.setPrimaryGainCheck)
        self.primaryGainSpin = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.primaryGainSpin.setObjectName("primaryGainSpin")
        self.horizontalLayout_5.addWidget(self.primaryGainSpin)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.frame = QtGui.QFrame(self.layoutWidget)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.waveGeneratorLabel = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waveGeneratorLabel.sizePolicy().hasHeightForWidth())
        self.waveGeneratorLabel.setSizePolicy(sizePolicy)
        self.waveGeneratorLabel.setObjectName("waveGeneratorLabel")
        self.verticalLayout.addWidget(self.waveGeneratorLabel)
        self.waveGeneratorWidget = StimGenerator(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waveGeneratorWidget.sizePolicy().hasHeightForWidth())
        self.waveGeneratorWidget.setSizePolicy(sizePolicy)
        self.waveGeneratorWidget.setObjectName("waveGeneratorWidget")
        self.verticalLayout.addWidget(self.waveGeneratorWidget)
        self.verticalLayout_2.addWidget(self.frame)
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.topPlotWidget = PlotWidget(self.splitter)
        self.topPlotWidget.setObjectName("topPlotWidget")
        self.bottomPlotWidget = PlotWidget(self.splitter)
        self.bottomPlotWidget.setObjectName("bottomPlotWidget")
        self.verticalLayout_3.addWidget(self.splitter_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.icModeRadio.setText(QtGui.QApplication.translate("Form", "IC", None, QtGui.QApplication.UnicodeUTF8))
        self.i0ModeRadio.setText(QtGui.QApplication.translate("Form", "I=0", None, QtGui.QApplication.UnicodeUTF8))
        self.vcModeRadio.setText(QtGui.QApplication.translate("Form", "VC", None, QtGui.QApplication.UnicodeUTF8))
        self.holdingCheck.setText(QtGui.QApplication.translate("Form", "Holding (pA)", None, QtGui.QApplication.UnicodeUTF8))
        self.primarySignalCheck.setText(QtGui.QApplication.translate("Form", "Primary:", None, QtGui.QApplication.UnicodeUTF8))
        self.secondarySignalCheck.setText(QtGui.QApplication.translate("Form", "Secondary:", None, QtGui.QApplication.UnicodeUTF8))
        self.primarySignalCombo.setItemText(0, QtGui.QApplication.translate("Form", "MembranePotential", None, QtGui.QApplication.UnicodeUTF8))
        self.secondarySignalCombo.setItemText(0, QtGui.QApplication.translate("Form", "MembraneCurrent", None, QtGui.QApplication.UnicodeUTF8))
        self.setSecondaryGainCheck.setText(QtGui.QApplication.translate("Form", "Set Gain", None, QtGui.QApplication.UnicodeUTF8))
        self.setPrimaryGainCheck.setText(QtGui.QApplication.translate("Form", "Set Gain", None, QtGui.QApplication.UnicodeUTF8))
        self.waveGeneratorLabel.setText(QtGui.QApplication.translate("Form", "Function (values in pA)", None, QtGui.QApplication.UnicodeUTF8))

from lib.util.generator.StimGenerator import StimGenerator
from lib.util.qtgraph.PlotWidget import PlotWidget
