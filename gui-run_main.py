from genericpath import isfile
import sys, os, re, time, shutil
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QProgressDialog, QTableView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui_GUI_ import Ui_Form
import DLC_info_catch, DLC_list_checking
import DLC_list2excel
from DLC_config_reader import DLC_config_reader_main
from Ui_wlanbt_select import Ui_wlanbt_select_Form


## def function
def str2bool(v):
    return str(v).lower() in ("yes", "true", "t")

def list_diff(li1, li2): 
    # https://magic-panda-engineer.github.io/Python/python-compare-two-lists
    return (list(set(li1).symmetric_difference(set(li2))))

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def compare_paths(path_A, path_B):
    # 計算 path_A 相對於 path_B 的相對路徑
    relative_path = os.path.relpath(path_A, path_B)
    return relative_path

# Start 
print("Please wait...")

# Set config file name and settings (global)
config_filename = "DLC_config.ini" 
settings = QtCore.QSettings(config_filename, QtCore.QSettings.IniFormat)

# for wlanbt set
first_click_loaddate = True
batch_in_folder_path_list = []
AUMIDs_in_folder_path_list = []
modules_list = []

# for package2zip set
class CompressionThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, path_info, batch_path_list, parent=None):
        super().__init__(parent)
        self.path_info = path_info
        self.batch_path_list = batch_path_list

    def run(self):
        driverPackageZip_folder = "ZIP_DriverPackage"
        for i in range(len(self.batch_path_list)):
            self.progress.emit(i)
            ori_package_path = self.batch_path_list[i]
            if str2bool(self.path_info[0]): 
                temp_path = ori_package_path
            else:
                temp_path = compare_paths(ori_package_path, self.path_info[1])

            zip_file_final_path = os.path.join(driverPackageZip_folder, temp_path)
            zip_folder_root = os.path.dirname(zip_file_final_path)
            if not os.path.exists(zip_folder_root):
                os.makedirs(zip_folder_root)
            
            shutil.make_archive(zip_file_final_path, format='zip', root_dir=ori_package_path)
        self.progress.emit(len(self.batch_path_list))
        self.finished.emit()


class wlanbtSelectWindos(QtWidgets.QMainWindow, Ui_wlanbt_select_Form):
    def __init__(self, table_view):
        super(wlanbtSelectWindos, self).__init__()
        self.setupUi(self)
        self.tableWidget_wlan_package_select.setColumnWidth(0, 400)
        self.tableWidget_bt_package_select.setColumnWidth(0, 400)
        self.tableWidget_wlan_package_select.cellClicked.connect(self.wlan_cell_was_clicked)
        self.tableWidget_bt_package_select.cellClicked.connect(self.bt_cell_was_clicked)
        self.pushButton_wlanbt_confirm.clicked.connect(self.when_confirm_buttom_clicked)

        # Set the tableView_wlanbt from the parameter
        self.tableView_wlanbt = table_view
        
    def loaddata(self, wlanbt_path_list):
        # Clear table widget status when every time user click add module button
        self.tableWidget_wlan_package_select.clearSelection()
        self.tableWidget_bt_package_select.clearSelection()
        # set path to GUI
        self.tableWidget_wlan_package_select.setRowCount(len(wlanbt_path_list[1]))
        self.tableWidget_bt_package_select.setRowCount(len(wlanbt_path_list[1]))
        for row in range(0, len(wlanbt_path_list[1])):
            self.tableWidget_wlan_package_select.setItem(row, 0, QtWidgets.QTableWidgetItem(wlanbt_path_list[1][row]))
            self.tableWidget_bt_package_select.setItem(row, 0, QtWidgets.QTableWidgetItem(wlanbt_path_list[1][row]))


    def set_to_wlanbt_tableview(self, modules_list):
        row_count = len(modules_list)
        self.model = QStandardItemModel(row_count * 2, 5)  # 每個模組有兩行，一個用於WLAN，一個用於BT
        self.model.setHorizontalHeaderLabels(["Vendor", "Module", "Function", "Package", "Path"])

        for i in range(row_count):
            vendor_item = QStandardItem(modules_list[i][0])
            vendor_item.setTextAlignment(Qt.AlignCenter)
            module_item = QStandardItem(modules_list[i][1])
            module_item.setTextAlignment(Qt.AlignCenter)

            # 設置WLAN行的資訊
            wlan_row = i * 2
            function_item_WLAN = QStandardItem("WLAN")  # 在每次迴圈中創建新的物件
            function_item_WLAN.setTextAlignment(Qt.AlignCenter)
            self.model.setItem(wlan_row, 0, vendor_item)
            self.model.setItem(wlan_row, 1, module_item)
            self.model.setItem(wlan_row, 2, function_item_WLAN)
            temp_list = (modules_list[i][3].split("\\"))[1] # 僅取 package folder name
            wlan_package_item = QStandardItem(temp_list)
            wlan_package_item.setTextAlignment(Qt.AlignCenter)
            self.model.setItem(wlan_row, 3, wlan_package_item)
            self.model.setItem(wlan_row, 4, QStandardItem(modules_list[i][2]))

            # 設置BT行的資訊
            bt_row = i * 2 + 1
            function_item_BT = QStandardItem("BT")  # 在每次迴圈中創建新的物件
            function_item_BT.setTextAlignment(Qt.AlignCenter)
            self.model.setItem(bt_row, 0, vendor_item.clone())  # 使用clone方法以避免相同對象的重複添加
            self.model.setItem(bt_row, 1, module_item.clone())
            self.model.setItem(bt_row, 2, function_item_BT)
            temp_list = (modules_list[i][5].split("\\"))[1] # 僅取 package folder name
            bt_package_item = QStandardItem(temp_list)
            bt_package_item.setTextAlignment(Qt.AlignCenter)
            self.model.setItem(bt_row, 3, bt_package_item)
            self.model.setItem(bt_row, 4, QStandardItem(modules_list[i][4]))
        self.tableView_wlanbt.setModel(self.model)
        self.tableView_wlanbt.resizeColumnsToContents()


    def testing_function(self, testarg):
        # for temporary test function 
        for i in range(0, len(testarg)):
            print(testarg[i])


    def when_confirm_buttom_clicked(self):
        global modules_list

        try:
            vendor_name = self.comboBox_vender_select.currentText()

            if self.lineEdit_module_name.text() == "":
                QMessageBox.about(self, "Error: Empty values found", "The Module block can not be empty.")
                return 0
            
            module_name = self.lineEdit_module_name.text()
            module_name = re.sub(r"\s+", "", module_name) # remove white space
            module_name_split = module_name.split(",") # e.g.:["Ax211", "Be200"]

            for i in range(0, len(module_name_split)): # format: [Vendor, Module, wlan_real_path, wlan_gui_path, bt_real_path, bt_gui_path]
                modules_info_str_temp = (vendor_name, module_name_split[i], wlanbt_path_list[0][self.wlan_row], 
                                                                            wlanbt_path_list[1][self.wlan_row], 
                                                                            wlanbt_path_list[0][self.bt_row],
                                                                            wlanbt_path_list[1][self.bt_row])
                modules_list.append(modules_info_str_temp)

            # set to tableview
            self.set_to_wlanbt_tableview(modules_list)

        except Exception: # if WLAN/BT Package block values is null
            QMessageBox.about(self, "Error: Null values found", "Please make sure the following two fields have been selected: \n{} \n{} ".format("WLAN Package", "BT Package"))
            return 0
            

    def wlan_cell_was_clicked(self, row, column):
        self.wlan_row = row

    def bt_cell_was_clicked(self, row, column):
        self.bt_row = row


# Main Window
class mywindow(QtWidgets.QMainWindow, Ui_Form):
    #__init__:解構函式，Class被建立後就會預先載入的專案。
    # 馬上執行，這個方法可以用來對物件做一些希望的初始化。
    def __init__(self):
        #這裡需要過載一下mywindow，同時也包含了QtWidgets.QMainWindow的預載入項。
        super(mywindow, self).__init__()
        self.setupUi(self)
        # self.wlanbtSelectWindos_ = wlanbtSelectWindos()
        self.wlanbtSelectWindos_ = wlanbtSelectWindos(self.tableView_wlanbt)
        self.enter_path_lineEdit.setEnabled(False)

        # 監聽 Radio Button 的狀態變化，並連接槽函數
        self.radio_enter_path.toggled.connect(self.toggle_line_edit)

        # greeting message
        cls()
        print("--Program startup--")

        # if config file is exist, load config to GUI
        if os.path.isfile(config_filename):
            self.read_config_to_GUI()

        # button click
        self.run_pushButton.clicked.connect(self.when_run_pushButton_click) # main button 
        self.pushButton_addModule.clicked.connect(self.when_addModule_pushButton_click)
        self.pushButton_updateToCurrentDate.clicked.connect(self.when_updateToCurrentDate_click)
        self.pushButton_clearAllModules.clicked.connect(self.when_clearAllModules_click)
        self.pushButton_packingRun.clicked.connect(self.when_packingRun_click)


    def when_clearAllModules_click(self):
        global modules_list
        modules_list = []
        self.wlanbtSelectWindos_.set_to_wlanbt_tableview(modules_list)

    def when_updateToCurrentDate_click(self):
        self.dateEdit_updateDate.setDate(QtCore.QDate().currentDate())

    def toggle_line_edit(self, state):
        # 當 Radio Button 狀態變化時，判斷其狀態，並設置 Line Edit 的啟用狀態
        self.enter_path_lineEdit.setEnabled(state)

    def msgBox_select(self, title_msg, test_msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title_msg)
        msgBox.setText(test_msg)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.No)

        return msgBox.exec_()

    def when_packingRun_click(self):
        if self.radio_current_path.isChecked():
            isCurrentPath = True
            local_dir_path = os.getcwd()
        elif self.radio_enter_path.isChecked():
            isCurrentPath = False
            local_dir_path = self.enter_path_lineEdit.text()

        if self.radioButton_zipToPackage.isChecked():
            root_folder = os.listdir(local_dir_path)
            package_list = [] 

            for i in range(len(root_folder)): 
                realpath_root = os.path.join(local_dir_path, root_folder[i])
                if os.path.isdir(realpath_root):
                    if root_folder[i][0:2].isdigit():
                        package_list.append(root_folder[i])

            batch_in_folder_path_list_packing, _ = DLC_info_catch.batch_and_aumids_file_get(package_list, [isCurrentPath, local_dir_path])

            title_msg = "Package to ZIP"
            test_msg = "Please confirm the tree view is correct, \nand then click Ok to start the compression process."
            if self.msgBox_select(title_msg, test_msg) == QMessageBox.Ok:
                print("Start compression")
                self.start_compression([isCurrentPath, local_dir_path], batch_in_folder_path_list_packing)

        if self.radioButton_Unzip.isChecked():
            self.when_unzip_enable(self.path_info)

    def start_compression(self, path_info, batch_path_list):
        self.progress = QProgressDialog(self)
        self.progress.setWindowTitle("Please wait")  
        self.progress.setLabelText("Compressing...")
        self.progress.setCancelButtonText("Cancel")
        self.progress.setMinimumDuration(2)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setRange(0, len(batch_path_list))

        self.thread = CompressionThread(path_info, batch_path_list)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.finished.connect(self.compression_finished)
        self.thread.start()

    def compression_finished(self):
        QMessageBox.information(self, "Message", "Compression complete\nPath: ZIP_DriverPackage")

    def export_driver_list(self):
        global batch_in_folder_path_list
        global AUMIDs_in_folder_path_list
        # Serach all folder at root_folder, Use folder to detect.
        root_folder = os.listdir(dir_path) # all file and folder under current path
        package_list = [] # list of root foder

        for i in range(0, len(root_folder)): 
            realpath_root = os.path.join(dir_path, root_folder[i])
            # detect is it driverPackage folder or others.(to do fix check function)
            # The Package_list output format as follow: ['01_Chipset_Intel', '02_ME_Intel', '03_IRST_Intel', '04_SerialIO_Intel', '05_DTT_Intel', '05_ICSS_Intel'... "19_AICamera_Morpho"]
            if os.path.isdir(realpath_root):
                if root_folder[i][0:2].isdigit(): #暴力分法，看前兩個字元是不是數字，之後再優化
                    package_list.append(root_folder[i])

        # Batch / AUMIDs file path list, use .bat/ AUMIDs.txt to detect.
        # Main output 1: list of bat file path.
        # Main output 2 : list of AUMIDS file path. list amount same as Mina output 1. 
        # Those 2 output will feed in wlanbtSelectWindos_ to continue progress,
        batch_in_folder_path_list, AUMIDs_in_folder_path_list = DLC_info_catch.batch_and_aumids_file_get(package_list, self.path_info)
        final_item_list, final_bat_path_list, final_aumids_path_list = DLC_info_catch.final_list_sort(batch_in_folder_path_list, AUMIDs_in_folder_path_list, modules_list)
        # for i in range(0, len(final_item_list)):
        #     print(f"final item:{final_item_list[i]}\nbatch path:{final_bat_path_list[i]}\naumids path:{final_aumids_path_list[i]}\n")

        all_list = DLC_info_catch.all_List_get(final_item_list, final_bat_path_list, final_aumids_path_list, self.os_info)
        output_file_name = DLC_list2excel.create_list(self.list_info, self.os_info, final_item_list, all_list)
        QMessageBox.about(self, "Export List", "File output completed, file name is: \n{}".format(str(output_file_name)))
        

    def when_addModule_pushButton_click(self):
        global wlanbt_path_list

        if self.radio_current_path.isChecked():
            isCurrentPath = True
            local_dir_path = os.getcwd()
        elif self.radio_enter_path.isChecked():
            isCurrentPath = False
            local_dir_path = self.enter_path_lineEdit.text()

        if os.path.exists(local_dir_path):
            root_folder = os.listdir(local_dir_path) # all file and folder under current path
            package_list = [] # list of root foder        

            for i in range(0, len(root_folder)): 
                realpath_root = os.path.join(local_dir_path, root_folder[i])
                # print(realpath_root)
                # detect is it driverPackage folder or others.(to do fix check function)
                # The Package_list output format as follow: ['01_Chipset_Intel', '02_ME_Intel', '03_IRST_Intel', '04_SerialIO_Intel', '05_DTT_Intel', '05_ICSS_Intel'... "19_AICamera_Morpho"]
                if os.path.isdir(realpath_root):
                    if root_folder[i][0:2].isdigit(): #暴力分法，看前兩個字元是不是數字，之後再優化
                        package_list.append(root_folder[i])
        else:
            QMessageBox.about(self, "Path Error", "The enter path isn't exist.")
            return 0

        batch_in_folder_path_list, AUMIDs_in_folder_path_list = DLC_info_catch.batch_and_aumids_file_get(package_list, [isCurrentPath, local_dir_path])
        wlanbt_list_realpath = DLC_info_catch.search_wlanbt(batch_in_folder_path_list) # format: List
        wlanbt_list_for_gui = [r"{0}\{1}".format(os.path.basename(os.path.dirname(path)), os.path.basename(path)) for path in wlanbt_list_realpath]
        # wlanbt_list_for_gui = [os.path.join(os.path.basename(os.path.dirname(path)), os.path.basename(path)) for path in wlanbt_list_realpath] # 將完整path列表解析成最末尾兩個Path   
        
        wlanbt_path_list = [] # output: [[realpath_1, realpath_2, ...], [forGuiPath_1, forGuiPath_2, ...]]
        wlanbt_path_list.append(wlanbt_list_realpath)
        wlanbt_path_list.append(wlanbt_list_for_gui)

        self.wlanbtSelectWindos_.loaddata(wlanbt_path_list)
        self.wlanbtSelectWindos_.lineEdit_module_name.setText("") # 每次點選時
        self.wlanbtSelectWindos_.show()

    # main button
    def when_run_pushButton_click(self):
        global batch_in_folder_path_list
        global AUMIDs_in_folder_path_list
        global dir_path

        # save config.ini
        self.config_save()
        time.sleep(1) # For config.ini file, save buffering
        
        # after click run button load all config settings 
        self.list_info, self.os_info, self.other_setting, self.wlanbt_info, self.path_info= DLC_config_reader_main()

        if str2bool(self.path_info[0]):
            dir_path = os.getcwd() # get current path (as know as driver package path)
        else:
            dir_path = self.path_info[1] #e.g. "C:\Users\EddieYW_Su\Desktop\A5Test"


        if not os.path.exists(dir_path):
            QMessageBox.about(self, "Path Error", "The enter path isn't exist.")
            return 0

        # if list checking is True, run List checking function.
        # if export driver list is True, run export driver list function.
        # other setting is still under development.
        if str2bool(self.other_setting[0]):
            self.export_driver_list() # create driver list
            return 0

        elif str2bool(self.other_setting[1]): # ListChecking=true
            DLC_list_checking.list_checking_main()
            QMessageBox.about(self, "List checking", "Checking Complete")
            return 0

        else: 
            QMessageBox.about(self, "Sorry", "This feature is still under development.")
            return 0


    def when_package2zip_enable(self, path_info, batch_path_list):
        driverPackageZip_folder = "ZIP_DriverPackage"

        # progressBar UI
        progress = QProgressDialog(self) 
        progress.setWindowTitle("Please wait")  
        progress.setLabelText("Compressing...")
        progress.setCancelButtonText("Cancel")
        progress.setMinimumDuration(2)
        progress.setWindowModality(Qt.WindowModal)
        progress.setRange(0, len(batch_path_list)) # set progressBar range 

        # Zip the file and place it in the corresponding folder
        for i in range(0, len(batch_path_list)):
            progress.setValue(i) 
            if progress.wasCanceled():
                QMessageBox.warning(self,"WARNING","User interrupt") 
                break 

            # compression main
            ori_package_path = batch_path_list[i] 
            if str2bool(path_info[0]): # if use program current path (path_info[0])
                temp_path = ori_package_path
            else:
                temp_path = compare_paths(ori_package_path, path_info[1]) # if use specify path, then calculate the relative path of "current_path" and "specify path"

            zip_file_final_path = os.path.join(driverPackageZip_folder, temp_path) # e.g. ZIP_DriverPackage\14_WLANBT_Intel\BT\BT_Intel_22.150.0.6
            zip_folder_root = zip_file_final_path.split("\\")
            zip_folder_root.pop() # cuz folder rule
            zip_folder_root = os.path.join(*zip_folder_root) # e.g. ZIP_DriverPackage\14_WLANBT_Intel\BT, # * mean each list element 
            # Prepare the corresponding folder
            if not os.path.exists(zip_folder_root):
                os.makedirs(zip_folder_root)
                print("mkdir: ", zip_folder_root)
            
            shutil.make_archive(zip_file_final_path, format='zip', root_dir=ori_package_path)

        # when compression done
        else:
            progress.setValue(len(batch_in_folder_path_list))
            QMessageBox.information(self,"Message","Compression complete\nPath: {}".format(driverPackageZip_folder))


    def config_save(self):
        settings.clear()
        # save
        customer_content = self.customer_comboBox.currentText()
        projectName_content = self.projectName_lineEdit.text()
        listVersion_content = self.listVersion_lineEdit.text()
        updateDate_content = self.dateEdit_updateDate.date().toString("yyyy/MM/dd")
        osEdition_content = self.osEdition_lineEdit.text()
        osVersion_content = self.osVersion_lineEdit.text()
        osBuild_content = self.osBuild_lineEdit.text()
        
        # module info save
        if modules_list != []: 
            for i, module in enumerate(modules_list):
                module_key = f"WlanBtInfo/Module_{i+1}" # f-string 寫法，等價於 module_key = "WlanBtInfo/Module_{}".format(str(i+1)) 
                settings.beginGroup(module_key)
                settings.setValue("Vendor", module[0])
                settings.setValue("Name", module[1])
                settings.setValue("WlanRealPath", module[2])
                settings.setValue("WlanGUIPath", module[3])
                settings.setValue("BTRealPath", module[4])
                settings.setValue("BTGUIPath", module[5])
                settings.endGroup()
        else: # 若module_list 為空，儲存預設的empty str給config.ini，避免開程式時讀值error
            settings.beginGroup("WlanBtInfo/Module_1")
            settings.setValue("Vendor", "")
            settings.setValue("Name", "")
            settings.setValue("WlanRealPath", "") 
            settings.setValue("WlanGUIPath", "")
            settings.setValue("BTRealPath", "")
            settings.setValue("BTGUIPath", "")
            settings.endGroup()

        exportDriverList_bool_content = self.radioButton_exportDriverList.isChecked()
        listChecking_bool_content = self.radioButton_listChecking.isChecked()
        listUpdate_bool_content = self.radioButton_listUpdate.isChecked()
        # package2zip_bool_content = self.package2zip_checkBox.isChecked()

        if self.radio_current_path.isChecked():
            is_current_path = True
        elif self.radio_enter_path.isChecked():
            is_current_path = False

        enter_path_content = self.enter_path_lineEdit.text()

        settings.setValue("List_Info/Customer", customer_content)
        settings.setValue("List_Info/ProjectName", projectName_content)
        settings.setValue("List_Info/ListVersion", listVersion_content)
        settings.setValue("List_Info/UpdateDate", updateDate_content)
        settings.setValue("OS_Info/OSEdition", osEdition_content)
        settings.setValue("OS_Info/OSVersion", osVersion_content)
        settings.setValue("OS_Info/OSBuild", osBuild_content)
        settings.setValue("Other_Setting/ExportDriverList", exportDriverList_bool_content)
        settings.setValue("Other_Setting/ListChecking", listChecking_bool_content)
        settings.setValue("Other_Setting/ListUpdate", listUpdate_bool_content)
        settings.setValue("Path_Info/IsCurrentPath", is_current_path)
        settings.setValue("Path_Info/PackagePath", enter_path_content)

        print("Config Save Successfully")
        QMessageBox.about(self, "Save", "Save Successfully")


    def read_config_to_GUI(self):
        global modules_list

        # if has DLC_config.ini file, load setting in GUI
        self.projectName_lineEdit.setText(settings.value("List_Info/ProjectName"))
        self.listVersion_lineEdit.setText(settings.value("List_Info/ListVersion"))
        date_str = settings.value("List_Info/UpdateDate")
        qdate = QtCore.QDate.fromString(date_str, "yyyy/MM/dd")
        self.dateEdit_updateDate.setDate(qdate)
        self.osEdition_lineEdit.setText(settings.value("OS_Info/OSEdition"))
        self.osVersion_lineEdit.setText(settings.value("OS_Info/OSVersion"))
        self.osBuild_lineEdit.setText(settings.value("OS_Info/OSBuild"))
        self.radioButton_exportDriverList.setChecked(str2bool(settings.value("Other_Setting/ExportDriverList")))
        self.radioButton_listChecking.setChecked(str2bool(settings.value("Other_Setting/ListChecking")))
        self.radioButton_listUpdate.setChecked(str2bool(settings.value("Other_Setting/ListUpdate")))
        #self.package2zip_checkBox.setChecked(str2bool(settings.value("Other_Setting/Package2Zip")))
        is_current_path = str2bool(settings.value("Path_Info/IsCurrentPath")) # 判斷該值是否為True
        if is_current_path:
            self.radio_current_path.setChecked(True)
        else:
            self.radio_enter_path.setChecked(True)
        self.enter_path_lineEdit.setText(settings.value("Path_Info/PackagePath"))


        # read modules 本來應該用 beginGroup 取key值，但有一個暫時未知的 bug 無法取值，先採取如下的切分方法取值
        allkeys_ = settings.allKeys() # 先列出 config.ini 中的所有的key，輸出為list
        num_list=[]

        modules1_str_check = settings.value(f"WlanBtInfo/Module_1/Vendor")
        if  not modules1_str_check: # 檢查字串是否為空，若為空，代表 modules info 僅存了預設的Empty value
            modules_list = [] #直接將 modules_list 清空

        else: #若有值，再讀取 modules info
            # 先取Modules 的數量 # 由於格式為: WlanBtInfo/Module_{i}/Vendor
            for key_ in allkeys_:                          # 遍歷所有key
                if key_.startswith("WlanBtInfo/Module_"):  # 找到以"WlanBtInfo/Module_"為開頭的key
                    _ = key_.split("_")[1]                 # 切分("_")取後值: {i}/Vendor
                    num_list.append(int(_.split("/")[0]))  # 切分("/")取前值: {i}，並把每次數字紀錄到 num_list

            num_modules = max(num_list) # 取num_list中最大值，即為module數量
                    
            #根據 config.ini 中的 module 數量，讀取每個 module info
            for i in range(1, num_modules+1):
                vendor_temp = settings.value(f"WlanBtInfo/Module_{i}/Vendor")
                moduleName_temp = settings.value(f"WlanBtInfo/Module_{i}/Name")
                wlan_real_path = settings.value(f"WlanBtInfo/Module_{i}/WlanRealPath")
                wlan_gui_path = settings.value(f"WlanBtInfo/Module_{i}/WlanGUIPath")
                bt_real_path = settings.value(f"WlanBtInfo/Module_{i}/BTRealPath")
                bt_gui_path = settings.value(f"WlanBtInfo/Module_{i}/BTGUIPath")
                
                # 將資訊存為跟函數:when_confirm_buttom_clicked 相同格式，並同樣的append到modules_list
                modules_info_str_temp = (vendor_temp, moduleName_temp, wlan_real_path, 
                                                                            wlan_gui_path, 
                                                                            bt_real_path,
                                                                            bt_gui_path)
                modules_list.append(modules_info_str_temp)
            # set to tableview
            self.wlanbtSelectWindos_.set_to_wlanbt_tableview(modules_list)


if __name__ == '__main__': # Main progress start
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())

