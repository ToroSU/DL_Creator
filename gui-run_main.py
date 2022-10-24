from genericpath import isfile
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QDockWidget, QListWidget
from PyQt5.QtGui import *
from Ui_GUI_ import Ui_Form

import DLC_info_catch
from DLC_list2excel import creat_list
from DLC_config_reader import DLC_config_reader_main
import os
import time


## def function
def str2bool(v):
    return str(v).lower() in ("yes", "true", "t")

def list_diff(li1, li2): 
    # https://magic-panda-engineer.github.io/Python/python-compare-two-lists
    return (list(set(li1).symmetric_difference(set(li2))))


# Set config file name and settings (global)
config_filename = "DLC_config.ini" 
settings = QtCore.QSettings(config_filename, QtCore.QSettings.IniFormat)


dir_path = os.getcwd() # get current path (as know as driver package path)
list_info, os_info, other_setting, wlanbt_info = DLC_config_reader_main()


# Serach all folder at root_folder, Use folder to detect.
root_folder = os.listdir(dir_path) # all file and folder under current path
package_list = [] # list of root foder
for i in range(0, len(root_folder)): 
    realpath_root = os.path.join(dir_path, root_folder[i])
    # detect is it driverPackage folder or others.(to do fix check function)
    if os.path.isdir(realpath_root):
        if root_folder[i][0:2].isdigit(): #暴力分法，看前兩個字元是不是數字，之後再優化
            package_list.append(root_folder[i])

# Batch / AUMIDs file path list, use .bat/ AUMIDs.txt to detect.
# TODO bat file exist (maybe todo ...)
# Main output 1: list of bat file path.
# Main output 2 : list of AUMIDS file path. list amount same as Mina output 1. 
batch_in_folder_path_list, AUMIDs_in_folder_path_list = DLC_info_catch.batch_and_aumids_file_get(package_list) 


class mywindow(QtWidgets.QMainWindow, Ui_Form):
    #__init__:解構函式，也就是類被建立後就會預先載入的專案。
    # 馬上執行，這個方法可以用來對你的物件做一些你希望的初始化。
    def __init__(self):
        #這裡需要過載一下mywindow，同時也包含了QtWidgets.QMainWindow的預載入項。
        super(mywindow, self).__init__()
        self.setupUi(self)

        # if config file is exist, load config to GUI
        if os.path.isfile(config_filename):
            self.read_config_to_GUI()

        # run button click
        self.run_pushButton.clicked.connect(self.when_run_pushButton_click)
        # save button click
        self.save_pushButton.clicked.connect(self.when_save_puchButton_click)


    def when_run_pushButton_click(self):
        pass
        # s = self.listChecking_checkBox.isChecked()
        # print(s)



    def when_save_puchButton_click(self):
        # when save button click, save the file as DLC_config.ini 
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
        settings.setValue("Other_Setting/ExportDriverList", exportDriverList_bool_content)
        settings.setValue("Other_Setting/ListChecking", listChecking_bool_content)
        settings.setValue("Other_Setting/Package2Zip", package2zip_bool_content)
        settings.setValue("WLANBT_Info/Intel", wlanbt_intel_content)
        settings.setValue("WLANBT_Info/AzwaveMTK", wlanbt_azwaveMTK_content)
        settings.setValue("WLANBT_Info/AzwaveRTK", wlanbt_azwaveRTK_content)
        settings.setValue("WLANBT_Info/LiteonRTK", wlanbt_liteonRTK_content)
        settings.setValue("WLANBT_Info/LiteonQualc", wlanbt_liteonQualc_content)
        QMessageBox.about(self, "Save", "Save Successfully")

    def read_config_to_GUI(self):
        # if has DLC_config.ini file, load setting in GUI
        self.projectName_lineEdit.setText(settings.value("List_Info/ProjectName"))
        self.listVersion_lineEdit.setText(settings.value("List_Info/ListVersion"))
        self.updateDate_lineEdit.setText(settings.value("List_Info/UpdateDate"))
        self.osEdition_lineEdit.setText(settings.value("OS_Info/OSEdition"))
        self.osVersion_lineEdit.setText(settings.value("OS_Info/OSVersion"))
        self.osBuild_lineEdit.setText(settings.value("OS_Info/OSBuild"))
        self.wlanbt_intel_lineEdit.setText(settings.value("WLANBT_Info/Intel"))
        self.wlanbt_AzwaveMTK_lineEdit.setText(settings.value("WLANBT_Info/AzwaveMTK"))
        self.wlanbt_AzwaveRTK_lineEdit.setText(settings.value("WLANBT_Info/AzwaveRTK"))
        self.wlanbt_liteonRTK_lineEdit.setText(settings.value("WLANBT_Info/LiteonRTK"))
        self.wlanbt_liteonQualc_lineEdit.setText(settings.value("WLANBT_Info/LiteonQualc"))

 
if __name__ == '__main__': #如果整個程式是主程式
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())

