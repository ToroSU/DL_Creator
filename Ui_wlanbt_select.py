# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\EddieYW_Su\Desktop\DL_Creator_current\Main_Repo\GUI_branch\DL_Creator\wlanbt_select.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wlanbt_select_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(835, 442)
        self.select_pushButton = QtWidgets.QPushButton(Form)
        self.select_pushButton.setGeometry(QtCore.QRect(650, 60, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.select_pushButton.setFont(font)
        self.select_pushButton.setObjectName("select_pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 20, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(340, 80, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.vendor_label = QtWidgets.QLabel(Form)
        self.vendor_label.setGeometry(QtCore.QRect(140, 20, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        font.setUnderline(True)
        self.vendor_label.setFont(font)
        self.vendor_label.setObjectName("vendor_label")
        self.loadData_pushButton = QtWidgets.QPushButton(Form)
        self.loadData_pushButton.setGeometry(QtCore.QRect(650, 20, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.loadData_pushButton.setFont(font)
        self.loadData_pushButton.setObjectName("loadData_pushButton")
        self.function_label = QtWidgets.QLabel(Form)
        self.function_label.setGeometry(QtCore.QRect(140, 80, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        font.setUnderline(True)
        self.function_label.setFont(font)
        self.function_label.setObjectName("function_label")
        self.module_label = QtWidgets.QLabel(Form)
        self.module_label.setGeometry(QtCore.QRect(440, 80, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        font.setUnderline(True)
        self.module_label.setFont(font)
        self.module_label.setObjectName("module_label")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(20, 130, 800, 300))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(11)
        self.tableWidget.setFont(font)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "WlanBT Select and Save"))
        self.select_pushButton.setText(_translate("Form", "Select"))
        self.label.setText(_translate("Form", "Vendor:"))
        self.label_2.setText(_translate("Form", "Function:"))
        self.label_3.setText(_translate("Form", "Module:"))
        self.vendor_label.setText(_translate("Form", "Vendor_label"))
        self.loadData_pushButton.setText(_translate("Form", "Load Data"))
        self.function_label.setText(_translate("Form", "Func.Label"))
        self.module_label.setText(_translate("Form", "Mod.Label"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Path"))
