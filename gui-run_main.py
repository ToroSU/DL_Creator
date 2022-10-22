import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QDockWidget, QListWidget
from PyQt5.QtGui import *
from Ui_DLC_GUI import Ui_Form

class mywindow(QtWidgets.QMainWindow, Ui_Form):
    #__init__:解構函式，也就是類被建立後就會預先載入的專案。
    # 馬上執行，這個方法可以用來對你的物件做一些你希望的初始化。
    def __init__(self):
        #這裡需要過載一下mywindow，同時也包含了QtWidgets.QMainWindow的預載入項。
        super(mywindow, self).__init__()
        self.setupUi(self)

        self.run_pushButton.clicked.connect(self.when_run_pushButton_click)
        self.save_pushButton.clicked.connect(self.when_save_puchButton_click)

    def when_run_pushButton_click(self):
        s = self.listChecking_checkBox.isChecked()
        print(s)

    def when_save_puchButton_click(self):
        config_filename = "DLC_config.ini"
        settings = QtCore.QSettings(config_filename, QtCore.QSettings.IniFormat)

        customer_content = self.customer_comboBox.currentText()
        projectName_content = self.projectName_lineEdit.text()
        listVersion_content = self.listVersion_lineEdit.text()
        updateDate_content = self.updateDate_lineEdit.text()
        osEdition_content = self.osEdition_lineEdit.text()
        osVersion_content = self.osVersion_lineEdit.text()
        osBuild_content = self.osBuild_lineEdit.text()
        wlanbt_intel_content = self.wlanbt_intel_lineEdit.text()
        wlanbt_azwaveMTK_content = self.wlanbt_AzwaveMTK_lineEdit.text()
        wlanbt_azwaveRTK_content = self.wlanbt_AzwaveRTK_lineEdit.text()
        wlanbt_liteonRTK_content = self.wlanbt_liteonRTK_lineEdit.text()
        wlanbt_liteonQualc_content = self.wlanbt_liteonQualc_lineEdit.text()
        exportDriverList_bool_content = self.exportDriverList_checkBox.isChecked()
        listChecking_bool_content = self.listChecking_checkBox.isChecked()
        package2zip_bool_content = self.package2zip_checkBox.isChecked()

        settings.setValue("List_Info/Customer", customer_content)
        settings.setValue("List_Info/ProjectName", projectName_content)
        settings.setValue("List_Info/ListVersion", listVersion_content)
        settings.setValue("List_Info/UpdateDate", updateDate_content)
        settings.setValue("OS_Info/OSEdition", osEdition_content)
        settings.setValue("OS_Info/OSVersion", osVersion_content)
        settings.setValue("OS_Info/OSBuild", osBuild_content)
        settings.setValue("OS_Info/OSEdition", osEdition_content)
        settings.setValue("Other_Setting/ExportDriverList", exportDriverList_bool_content)
        settings.setValue("Other_Setting/ListChecking", listChecking_bool_content)
        settings.setValue("Other_Setting/Package2Zip", package2zip_bool_content)
        settings.setValue("WLANBT_Info/Intel", wlanbt_intel_content)
        settings.setValue("WLANBT_Info/AzwaveMTK", wlanbt_azwaveMTK_content)
        settings.setValue("WLANBT_Info/AzwaveRTK", wlanbt_azwaveRTK_content)
        settings.setValue("WLANBT_Info/LiteonRTK", wlanbt_liteonRTK_content)
        settings.setValue("WLANBT_Info/LiteonQualc", wlanbt_liteonQualc_content)
        print(config_filename, " Save Successfully")



 
if __name__ == '__main__': #如果整個程式是主程式
    config_filename = "DLC_config.ini"

    settings = QtCore.QSettings(config_filename, QtCore.QSettings.IniFormat)
    if os.path.isfile(config_filename):
        print("config file is exist")

    else:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        app = QtWidgets.QApplication(sys.argv)
        window = mywindow()
        window.show()
        sys.exit(app.exec_())

