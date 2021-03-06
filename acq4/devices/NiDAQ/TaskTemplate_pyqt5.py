# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acq4/devices/NiDAQ/TaskTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(231, 366)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.triggerDevList = QtWidgets.QComboBox(Form)
        self.triggerDevList.setObjectName("triggerDevList")
        self.triggerDevList.addItem("")
        self.gridLayout.addWidget(self.triggerDevList, 1, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.numPtsLabel = QtWidgets.QLabel(Form)
        self.numPtsLabel.setObjectName("numPtsLabel")
        self.gridLayout.addWidget(self.numPtsLabel, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.denoiseCombo = QtWidgets.QComboBox(self.groupBox)
        self.denoiseCombo.setObjectName("denoiseCombo")
        self.denoiseCombo.addItem("")
        self.denoiseCombo.addItem("")
        self.gridLayout_3.addWidget(self.denoiseCombo, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 2, 0, 1, 1)
        self.filterCombo = QtWidgets.QComboBox(self.groupBox)
        self.filterCombo.setObjectName("filterCombo")
        self.filterCombo.addItem("")
        self.filterCombo.addItem("")
        self.filterCombo.addItem("")
        self.gridLayout_3.addWidget(self.filterCombo, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 5, 0, 1, 1)
        self.downsampleSpin = QtWidgets.QSpinBox(self.groupBox)
        self.downsampleSpin.setMinimum(1)
        self.downsampleSpin.setMaximum(10000000)
        self.downsampleSpin.setProperty("value", 1)
        self.downsampleSpin.setObjectName("downsampleSpin")
        self.gridLayout_3.addWidget(self.downsampleSpin, 5, 1, 1, 1)
        self.butterworthCtrl = QtWidgets.QWidget(self.groupBox)
        self.butterworthCtrl.setObjectName("butterworthCtrl")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.butterworthCtrl)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_15 = QtWidgets.QLabel(self.butterworthCtrl)
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 0, 3, 1, 1)
        self.butterworthPassbandSpin = SpinBox(self.butterworthCtrl)
        self.butterworthPassbandSpin.setMaximum(1000.0)
        self.butterworthPassbandSpin.setProperty("value", 1.0)
        self.butterworthPassbandSpin.setObjectName("butterworthPassbandSpin")
        self.gridLayout_4.addWidget(self.butterworthPassbandSpin, 1, 1, 1, 2)
        self.label_14 = QtWidgets.QLabel(self.butterworthCtrl)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 0, 1, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.butterworthCtrl)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        self.butterworthPassDBSpin = QtWidgets.QDoubleSpinBox(self.butterworthCtrl)
        self.butterworthPassDBSpin.setProperty("value", 3.0)
        self.butterworthPassDBSpin.setObjectName("butterworthPassDBSpin")
        self.gridLayout_4.addWidget(self.butterworthPassDBSpin, 1, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.butterworthCtrl)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 2, 0, 1, 1)
        self.butterworthStopbandSpin = SpinBox(self.butterworthCtrl)
        self.butterworthStopbandSpin.setProperty("value", 2.0)
        self.butterworthStopbandSpin.setObjectName("butterworthStopbandSpin")
        self.gridLayout_4.addWidget(self.butterworthStopbandSpin, 2, 1, 1, 2)
        self.butterworthStopDBSpin = QtWidgets.QDoubleSpinBox(self.butterworthCtrl)
        self.butterworthStopDBSpin.setProperty("value", 40.0)
        self.butterworthStopDBSpin.setObjectName("butterworthStopDBSpin")
        self.gridLayout_4.addWidget(self.butterworthStopDBSpin, 2, 3, 1, 1)
        self.butterworthBidirCheck = QtWidgets.QCheckBox(self.butterworthCtrl)
        self.butterworthBidirCheck.setObjectName("butterworthBidirCheck")
        self.gridLayout_4.addWidget(self.butterworthBidirCheck, 3, 1, 1, 2)
        self.gridLayout_3.addWidget(self.butterworthCtrl, 4, 1, 1, 1)
        self.besselCtrl = QtWidgets.QWidget(self.groupBox)
        self.besselCtrl.setObjectName("besselCtrl")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.besselCtrl)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.besselCutoffSpin = SpinBox(self.besselCtrl)
        self.besselCutoffSpin.setProperty("value", 2.0)
        self.besselCutoffSpin.setObjectName("besselCutoffSpin")
        self.gridLayout_5.addWidget(self.besselCutoffSpin, 0, 1, 1, 2)
        self.label_12 = QtWidgets.QLabel(self.besselCtrl)
        self.label_12.setObjectName("label_12")
        self.gridLayout_5.addWidget(self.label_12, 1, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.besselCtrl)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 0, 0, 1, 1)
        self.besselOrderSpin = QtWidgets.QSpinBox(self.besselCtrl)
        self.besselOrderSpin.setMinimum(1)
        self.besselOrderSpin.setMaximum(16)
        self.besselOrderSpin.setProperty("value", 4)
        self.besselOrderSpin.setObjectName("besselOrderSpin")
        self.gridLayout_5.addWidget(self.besselOrderSpin, 1, 1, 1, 2)
        self.besselBidirCheck = QtWidgets.QCheckBox(self.besselCtrl)
        self.besselBidirCheck.setObjectName("besselBidirCheck")
        self.gridLayout_5.addWidget(self.besselBidirCheck, 2, 1, 1, 2)
        self.gridLayout_3.addWidget(self.besselCtrl, 3, 1, 1, 1)
        self.denoiseCtrl = QtWidgets.QWidget(self.groupBox)
        self.denoiseCtrl.setObjectName("denoiseCtrl")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.denoiseCtrl)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_13 = QtWidgets.QLabel(self.denoiseCtrl)
        self.label_13.setObjectName("label_13")
        self.gridLayout_6.addWidget(self.label_13, 0, 0, 1, 1)
        self.denoiseThresholdSpin = QtWidgets.QDoubleSpinBox(self.denoiseCtrl)
        self.denoiseThresholdSpin.setProperty("value", 4.0)
        self.denoiseThresholdSpin.setObjectName("denoiseThresholdSpin")
        self.gridLayout_6.addWidget(self.denoiseThresholdSpin, 0, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.denoiseCtrl)
        self.label_16.setObjectName("label_16")
        self.gridLayout_6.addWidget(self.label_16, 1, 0, 1, 1)
        self.denoiseWidthSpin = QtWidgets.QSpinBox(self.denoiseCtrl)
        self.denoiseWidthSpin.setMinimum(1)
        self.denoiseWidthSpin.setMaximum(100000)
        self.denoiseWidthSpin.setProperty("value", 1)
        self.denoiseWidthSpin.setObjectName("denoiseWidthSpin")
        self.gridLayout_6.addWidget(self.denoiseWidthSpin, 1, 1, 1, 1)
        self.gridLayout_3.addWidget(self.denoiseCtrl, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 3)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.rateSpin = SpinBox(self.groupBox_2)
        self.rateSpin.setMinimum(0.01)
        self.rateSpin.setMaximum(1000000.0)
        self.rateSpin.setProperty("value", 40000.0)
        self.rateSpin.setObjectName("rateSpin")
        self.gridLayout_2.addWidget(self.rateSpin, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.periodSpin = SpinBox(self.groupBox_2)
        self.periodSpin.setMinimum(1.0)
        self.periodSpin.setMaximum(10000.0)
        self.periodSpin.setProperty("value", 1.0)
        self.periodSpin.setObjectName("periodSpin")
        self.gridLayout_2.addWidget(self.periodSpin, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 3)

        self.retranslateUi(Form)
        Qt.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = Qt.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Trigger"))
        self.triggerDevList.setItemText(0, _translate("Form", "No Trigger"))
        self.label_3.setText(_translate("Form", "Points"))
        self.numPtsLabel.setText(_translate("Form", "0"))
        self.groupBox.setTitle(_translate("Form", "Post-processing"))
        self.denoiseCombo.setToolTip(_translate("Form", "Denoise method to use.\n"
"- Pointwise method compares each point to its neighbors"))
        self.denoiseCombo.setItemText(0, _translate("Form", "None"))
        self.denoiseCombo.setItemText(1, _translate("Form", "Pointwise"))
        self.label_7.setText(_translate("Form", "Denoise"))
        self.label_9.setText(_translate("Form", "Filter"))
        self.filterCombo.setToolTip(_translate("Form", "Lowpass filter types to use for AI channels. Filter is applied before downsampling."))
        self.filterCombo.setItemText(0, _translate("Form", "None"))
        self.filterCombo.setItemText(1, _translate("Form", "Bessel"))
        self.filterCombo.setItemText(2, _translate("Form", "Butterworth"))
        self.label_8.setText(_translate("Form", "Downsample"))
        self.downsampleSpin.setToolTip(_translate("Form", "Amount DAQ data should be downsampled before returning results (output data is not downsampled before sending to the DAQ). DI/DO data is downsampled by subsampling, AI/AO data is downsampled by averaging. "))
        self.downsampleSpin.setSuffix(_translate("Form", "x"))
        self.label_15.setText(_translate("Form", "dB"))
        self.butterworthPassbandSpin.setToolTip(_translate("Form", "Upper frequency of butterworth passband in multiples of maximum nyquist frequency (sample rate / 2)."))
        self.label_14.setText(_translate("Form", "Freq."))
        self.label_5.setText(_translate("Form", "pass"))
        self.butterworthPassDBSpin.setToolTip(_translate("Form", "Maximum amplitude of loss in passband"))
        self.label_6.setText(_translate("Form", "stop"))
        self.butterworthStopbandSpin.setToolTip(_translate("Form", "Lower frequency of butterworth stopband in multiples of maximum nyquist frequency (sample rate / 2)."))
        self.butterworthStopDBSpin.setToolTip(_translate("Form", "Minimum amplitude of loss in stopband"))
        self.butterworthBidirCheck.setText(_translate("Form", "Bidirectional"))
        self.label_12.setText(_translate("Form", "Order"))
        self.label_11.setText(_translate("Form", "Cutoff"))
        self.besselBidirCheck.setText(_translate("Form", "Bidirectional"))
        self.label_13.setText(_translate("Form", "Threshold"))
        self.denoiseThresholdSpin.setToolTip(_translate("Form", "Minimum threshold of detected noise events"))
        self.label_16.setText(_translate("Form", "Width"))
        self.denoiseWidthSpin.setToolTip(_translate("Form", "Maximum radius of detected noise events"))
        self.groupBox_2.setTitle(_translate("Form", "Timing"))
        self.label.setText(_translate("Form", "Rate"))
        self.rateSpin.setSuffix(_translate("Form", " Hz"))
        self.label_4.setText(_translate("Form", "Period"))
        self.periodSpin.setSuffix(_translate("Form", " μs"))

from acq4.pyqtgraph import SpinBox
