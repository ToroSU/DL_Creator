from genericpath import isfile
import sys
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMessageBox, QProgressDialog
from PyQt5.QtGui import *
from Ui_GUI_ import Ui_Form
import DLC_info_catch
from DLC_list2excel import create_list
from DLC_list_checking import list_checking_main
from DLC_config_reader import DLC_config_reader_main
import os
# import time
from Ui_wlanbt_select import Ui_wlanbt_select_Form
import shutil


## def function
def str2bool(v):
    return str(v).lower() in ("yes", "true", "t")

def list_diff(li1, li2): 
    # https://magic-panda-engineer.github.io/Python/python-compare-two-lists
    return (list(set(li1).symmetric_difference(set(li2))))

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


# Start 
print("Please wait...")

# Set config file name and settings (global)
config_filename = "DLC_config.ini" 
settings = QtCore.QSettings(config_filename, QtCore.QSettings.IniFormat)

dir_path = os.getcwd() # get current path (as know as driver package path)
# for wlanbt set
first_click_loaddate = True
wlanbt_module_name_list = ["Intel", "AzureWave MTK", "AzureWave RTK", "Liteon RTK", "Liteon Qualc."]
batch_in_folder_path_list = []
AUMIDs_in_folder_path_list = []
wlan_final_item_list = []
wlan_final_path_list = []


class wlanbtSelectWindos(QtWidgets.QMainWindow, Ui_wlanbt_select_Form):
    def __init__(self):
        super(wlanbtSelectWindos, self).__init__()
        self.setupUi(self)
        self.tableWidget.setColumnWidth(0, 780)
        self.tableWidget.cellClicked.connect(self.cell_was_clicked)
        self.select_pushButton.clicked.connect(self.when_selectButton_click)
        self.select_pushButton.setEnabled(False) # disable select button until loaddata
        self.loadData_pushButton.clicked.connect(self.when_loadData_Button_click)
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("Please click Load Data button"))
        # initial settings of select_pushButton click 
        self.wlanbt_button_clicked_count = 0 # for click button countdown


    def reset_all(self):
        global batch_in_folder_path_list
        global AUMIDs_in_folder_path_list
        global wlan_final_item_list
        global wlan_final_path_list
        global first_click_loaddate

        # initial settings of select_pushButton click 
        self.wlanbt_button_clicked_count = 0 # for click button countdown
        # reset variable, reset select window label
        first_click_loaddate = True
        batch_in_folder_path_list = []
        AUMIDs_in_folder_path_list = []
        wlan_final_item_list = []
        wlan_final_path_list = []
        self.wlanbt_button_clicked_count = 0
        self.select_pushButton.setEnabled(False)

        if self.wlanbt_total_count != 0: # reset label when config file have Wlan/BT module
            self.vendor_label.setText(wlanbt_module_name_list[self.used_wlanbt_module[0][0]])
            self.function_label.setText(self.used_wlanbt_module[0][1])
            self.module_label.setText(self.used_wlanbt_module[0][2])
        
        while self.tableWidget.rowCount() > 1: # clear tablewidget
            self.tableWidget.removeRow(0)

        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("Please click Load Data button"))
        print("Reset variable")


    def loaddata(self):
        global batch_in_folder_path_list
        self.wlanbt_list_for_gui = DLC_info_catch.search_wlanbt(batch_in_folder_path_list)
        self.tableWidget.setRowCount(len(self.wlanbt_list_for_gui))
        for row in range(0, len(self.wlanbt_list_for_gui)):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(self.wlanbt_list_for_gui[row]))


    def when_loadData_Button_click(self):
        # if click "Load Data" button, reset settings of select_pushButton 
        global wlan_final_item_list
        global wlan_final_path_list
        global first_click_loaddate
        self.select_pushButton.setEnabled(True) 

        # after click run button load all config settings 
        self.list_info, self.os_info, self.other_setting, self.wlanbt_info = DLC_config_reader_main()
        # obtain used wlanbt module, output: [[0, "Wlan", "Ax201"], [0, "Bluetooth", "Ax201"]....]
        self.used_wlanbt_module, self.wlanbt_total_count = DLC_info_catch.obtain_used_module(self.wlanbt_info)
        
        # case: without wlanbt module, call function complete_and_create_list, create list, return 0
        if self.wlanbt_total_count == 0:
            QMessageBox.about(self, "WARNING", "No Wlan/BT module in config.ini")
            self.complete_and_create_list()
            return 0 

        self.wlanbt_button_clicked_count = 0
        wlan_final_item_list = []
        wlan_final_path_list = []
        # 第一次按 load data按鈕才會把值寫入 tableWidget， 按save button的話則重置 first_click_loaddate
        if first_click_loaddate:
            self.loaddata()
            first_click_loaddate = False
        else:
            print("Reset")
            
        # set label
        # used_wlanbt_module e.g. [[0, 0, 'Ax201'], [0, 1, 'Ax211'], [1, 0, 'MT7921'], [1, 1, 'MT7922']]
        # self.wlanbt_button_clicked_count : e.g. count 0~7 (wlan and bt)
        self.vendor_label.setText(wlanbt_module_name_list[self.used_wlanbt_module[0][0]])
        self.function_label.setText(self.used_wlanbt_module[0][1])
        self.module_label.setText(self.used_wlanbt_module[0][2])


    def when_selectButton_click(self):
        global wlan_final_item_list
        global wlan_final_path_list
        global batch_in_folder_path_list
        global AUMIDs_in_folder_path_list
        # after click run button load all config settings 
        # self.list_info, self.os_info, self.other_setting, self.wlanbt_info = DLC_config_reader_main()
        # obtain used wlanbt module, output: [[0, "Wlan", "Ax201"], [0, "Bluetooth", "Ax201"]....]
        self.used_wlanbt_module, self.wlanbt_total_count = DLC_info_catch.obtain_used_module(self.wlanbt_info)

        if self.wlanbt_button_clicked_count == 0:
            final_item_name = self.used_wlanbt_module[self.wlanbt_button_clicked_count][1] + "({})".format(self.used_wlanbt_module[self.wlanbt_button_clicked_count][2])
            wlan_final_item_list.append(final_item_name)
            wlan_final_path_list.append(self.temp_string)

        if  self.wlanbt_button_clicked_count > 0 and self.wlanbt_button_clicked_count < self.wlanbt_total_count : # 用來檢查是否點完module 
            # print(used_wlanbt_module[self.wlanbt_button_clicked_count] ,self.temp_string)
            # used_wlanbt_module e.g. [[0, 0, 'Ax201'], [0, 1, 'Ax211'], [1, 0, 'MT7921'], [1, 1, 'MT7922']]

            final_item_name = self.used_wlanbt_module[self.wlanbt_button_clicked_count][1] + "({})".format(self.used_wlanbt_module[self.wlanbt_button_clicked_count][2])
            wlan_final_item_list.append(final_item_name)
            wlan_final_path_list.append(self.temp_string)

            #最後一個module按完後 關閉wlanbt選擇視窗, 並return 0 結束函數 (同時避免做接下來的setText)
            if self.wlanbt_button_clicked_count == self.wlanbt_total_count-1: # -1 cause counter is 0 to odd end
                QMessageBox.about(self, "WlanBT Save", "Save Successfully")

                # TODO 暫時將程式結尾放在這邊，後續換好一點的位置，海景第一排
                self.complete_and_create_list()
                return 0

        # 按下按鈕執行完後，計數+1，並設置下一個vendor/ module label      
        self.wlanbt_button_clicked_count += 1
        # set label
        # used_wlanbt_module e.g. [[0, 0, 'Ax201'], [0, 1, 'Ax211'], [1, 0, 'MT7921'], [1, 1, 'MT7922']]
        # self.wlanbt_button_clicked_count : e.g. count 0~7 (wlan and bt)
        self.vendor_label.setText(wlanbt_module_name_list[self.used_wlanbt_module[self.wlanbt_button_clicked_count][0]])
        self.function_label.setText(self.used_wlanbt_module[self.wlanbt_button_clicked_count][1])
        self.module_label.setText(self.used_wlanbt_module[self.wlanbt_button_clicked_count][2])


    def cell_was_clicked(self, row, column):
        item = self.tableWidget.item(row, column)
        self.temp_string = item.text()

    
    def complete_and_create_list(self):
        global batch_in_folder_path_list
        global AUMIDs_in_folder_path_list

        final_item_list, final_bat_path_list, final_aumids_path_list = DLC_info_catch.final_list_sort(batch_in_folder_path_list, AUMIDs_in_folder_path_list, wlan_final_item_list, wlan_final_path_list, self.wlanbt_info)
        all_list = DLC_info_catch.all_List_get(final_item_list, final_bat_path_list, final_aumids_path_list, self.os_info)
        if str2bool(self.other_setting[0]):
            create_list(self.list_info, self.os_info, final_item_list, all_list)
            QMessageBox.about(self, "Export List", "File output completed, path is: \n{}".format(dir_path))

        else:
            QMessageBox.about(self, "Export List", "\nExportDriverList= {},\ndo not export excel files.".format(self.other_setting[0]))
        
        # reset all
        self.reset_all()
        self.close() # close wlanbt select window
        return 0  # exit


# Main Window
class mywindow(QtWidgets.QMainWindow, Ui_Form):
    #__init__:解構函式，Class被建立後就會預先載入的專案。
    # 馬上執行，這個方法可以用來對物件做一些希望的初始化。
    def __init__(self):
        #這裡需要過載一下mywindow，同時也包含了QtWidgets.QMainWindow的預載入項。
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.wlanbtSelectWindos_ = wlanbtSelectWindos()

        # greeting message
        cls()
        print("--Program startup--")

        # if config file is exist, load config to GUI
        if os.path.isfile(config_filename):
            self.read_config_to_GUI()

        # run button click
        self.run_pushButton.clicked.connect(self.when_run_pushButton_click)
        # save button click
        self.save_pushButton.clicked.connect(self.when_save_puchButton_click)

        # behavior of if checkBox checked/unchecked
        self.exportDriverList_checkBox.toggled.connect(self.when_exportList_checkBox_checked)
        self.listChecking_checkBox.toggled.connect(self.when_listChecking_checkBox_checked)
        self.package2zip_checkBox.toggled.connect(self.when_package2zip_checkBox_checked)

    # main button
    def when_run_pushButton_click(self):
        global batch_in_folder_path_list
        global AUMIDs_in_folder_path_list
        
        # after click run button load all config settings 
        self.list_info, self.os_info, self.other_setting, self.wlanbt_info = DLC_config_reader_main()
        # if list checking is True
        if str2bool(self.other_setting[1]): # ListChecking=true
            self.when_listChecking_is_enable()
            QMessageBox.about(self, "List checking", "Checking Complete")

        # TODO Refactor the code this part
        else: 
            # list_info, os_info, other_setting, wlanbt_info = DLC_config_reader_main()
            # Serach all folder at root_folder, Use folder to detect.
            root_folder = os.listdir(dir_path) # all file and folder under current path
            package_list = [] # list of root foder

            for i in range(0, len(root_folder)): 
                realpath_root = os.path.join(dir_path, root_folder[i])
                # detect is it driverPackage folder or others.(to do fix check function)
                if os.path.isdir(realpath_root):
                    if root_folder[i][0:2].isdigit(): #暴力分法，看前兩個字元是不是數字，之後再優化
                        # self.package_list.append(root_folder[i])
                        package_list.append(root_folder[i])

            # Batch / AUMIDs file path list, use .bat/ AUMIDs.txt to detect.
            # TODO bat file exist (maybe todo ...)
            # Main output 1: list of bat file path.
            # Main output 2 : list of AUMIDS file path. list amount same as Mina output 1. 
            # batch_in_folder_path_list, AUMIDs_in_folder_path_list = DLC_info_catch.batch_and_aumids_file_get(self.package_list) 
            batch_in_folder_path_list, AUMIDs_in_folder_path_list = DLC_info_catch.batch_and_aumids_file_get(package_list)

            if str2bool(self.other_setting[2]): # zip the package
                self.when_package2zip_enable()

            else:
                self.wlanbtSelectWindos_.show() # enter crete list main code


    def when_exportList_checkBox_checked(self):
        # exportDriverList_checkBox is checked
        if self.exportDriverList_checkBox.isChecked():
            self.listChecking_checkBox.setEnabled(False)
            self.listChecking_checkBox.setChecked(False)
            self.package2zip_checkBox.setEnabled(False)
            self.package2zip_checkBox.setChecked(False)
        else: 
            self.listChecking_checkBox.setEnabled(True)
            self.package2zip_checkBox.setEnabled(True)


    def when_listChecking_checkBox_checked(self):
        if self.listChecking_checkBox.isChecked():
            self.exportDriverList_checkBox.setEnabled(False)
            self.exportDriverList_checkBox.setChecked(False)
            self.package2zip_checkBox.setEnabled(False)
            self.package2zip_checkBox.setChecked(False)
        else: 
            self.exportDriverList_checkBox.setEnabled(True)
            self.package2zip_checkBox.setEnabled(True)


    def when_package2zip_checkBox_checked(self):
        if self.package2zip_checkBox.isChecked():
            self.exportDriverList_checkBox.setEnabled(False)
            self.exportDriverList_checkBox.setChecked(False)
            self.listChecking_checkBox.setEnabled(False)
            self.listChecking_checkBox.setChecked(False)
        else: 
            self.exportDriverList_checkBox.setEnabled(True)
            self.listChecking_checkBox.setEnabled(True)      


    def when_listChecking_is_enable(self):
        list_checking_main()


    def when_package2zip_enable(self):
        global batch_in_folder_path_list
        driverPackageZip_folder = "ZIP_DriverPackage"

        # progressBar UI
        progress = QProgressDialog(self) 
        progress.setWindowTitle("Please wait")  
        progress.setLabelText("Compressing...")
        progress.setCancelButtonText("Cancel")
        progress.setMinimumDuration(2)
        progress.setWindowModality(Qt.WindowModal)
        progress.setRange(0, len(batch_in_folder_path_list)) # set progressBar range 

        # Zip the file and place it in the corresponding folder
        for i in range(0, len(batch_in_folder_path_list)):
            progress.setValue(i) 
            if progress.wasCanceled():
                QMessageBox.warning(self,"WARNING","User interrupt") 
                break
            
            # compression main
            current_path = batch_in_folder_path_list[i] # e.g. 14_WLANBT_Intel\BT\BT_Intel_22.150.0.6 (bat file path)
            zip_file_final_path = os.path.join(driverPackageZip_folder, current_path) # e.g. ZIP_DriverPackage\14_WLANBT_Intel\BT\BT_Intel_22.150.0.6
            zip_folder_root = zip_file_final_path.split("\\")
            zip_folder_root.pop() # cuz folder rule
            zip_folder_root = os.path.join(*zip_folder_root) # e.g. ZIP_DriverPackage\14_WLANBT_Intel\BT, # * mean each list element 
            # Prepare the corresponding folder
            if not os.path.exists(zip_folder_root):
                os.makedirs(zip_folder_root)
                print("mkdir: ", zip_folder_root)

            shutil.make_archive(zip_file_final_path, format='zip', root_dir=current_path)

        # when compression done
        else:
            progress.setValue(len(batch_in_folder_path_list))
            QMessageBox.information(self,"Message","Compression complete\nPath: {}".format(driverPackageZip_folder))         


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
        self.exportDriverList_checkBox.setChecked(str2bool(settings.value("Other_Setting/ExportDriverList")))
        self.listChecking_checkBox.setChecked(str2bool(settings.value("Other_Setting/ListChecking")))
        self.package2zip_checkBox.setChecked(str2bool(settings.value("Other_Setting/Package2Zip")))


if __name__ == '__main__': #如果整個程式是主程式
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())

