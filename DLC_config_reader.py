import os
import configparser
# Reference of ConfigParser https://docs.python.org/3/library/configparser.html


def if_config_file_exist(file_name):
    config = configparser.ConfigParser()
    config.read(file_name)

    try:
        list_info = config["List_Info"]
        list_info_return = [list_info["Customer"],
                            list_info["ProjectName"],
                            list_info["ListVersion"],
                            list_info["UpdateDate"]]

        os_info = config["OS_Info"]
        os_info_return = [os_info["OSEdition"],
                          os_info["OSVersion"],
                          os_info["OSBuild"]]

        other_setting = config["Other_Setting"]
        other_setting_return = [other_setting["ExportDriverList"],
                                other_setting["ListChecking"],
                                other_setting["ListUpdate"]]

        # Check for WLANBT module info
        wlanbt_info_return=[]
        num_list=[]


        for key_ in config["WlanBtInfo"]:
            _ = key_.split("_")[1]                 # 切分("_")取後值: {i}/Vendor
            num_list.append(int(_.split("\\")[0]))  # 切分("\\")取前值: {i}，並把每次數字紀錄到 num_list # 這裡跟gui-run_main的規則有點不同，因為import的module不同

        num_modules = max(num_list) # 取num_list中最大值，即為module數量
        
        for i in range(1, num_modules+1):
            vendor_temp = config["WlanBtInfo"][rf"Module_{i}\Vendor"] # r means original string, to avoid unicode error
            moduleName_temp = config["WlanBtInfo"][rf"Module_{i}\Name"]
            wlan_real_path = config["WlanBtInfo"][rf"Module_{i}\WlanRealPath"]
            wlan_gui_path = config["WlanBtInfo"][rf"Module_{i}\WlanGUIPath"]
            bt_real_path = config["WlanBtInfo"][rf"Module_{i}\BTRealPath"]
            bt_gui_path = config["WlanBtInfo"][rf"Module_{i}\BTGUIPath"]
            # 將資訊存為跟函數:when_confirm_buttom_clicked 相同格式，並同樣的append到modules_list
            modules_info_str_temp = (vendor_temp, moduleName_temp, wlan_real_path, 
                                                                        wlan_gui_path, 
                                                                        bt_real_path,
                                                                        bt_gui_path)

            wlanbt_info_return.append(modules_info_str_temp)


            path_info = config["Path_Info"]

            # Normalize path before returning
            package_path = os.path.normpath(path_info["PackagePath"])
            path_info_return = [path_info["IsCurrentPath"], package_path]


        return list_info_return, os_info_return, other_setting_return, wlanbt_info_return, path_info_return

    except Exception as e:
        print("Error:", e)


## Main
def DLC_config_reader_main():
    config_filename = "DLC_config.ini"

    # Try to read config.ini file, if can't read file, use default setting
    if os.path.isfile(config_filename):
        print("Read config file successfully.")
        list_info_return, os_info_return, other_setting_return, wlanbt_info_return, path_info_return = if_config_file_exist(config_filename)
        return list_info_return, os_info_return, other_setting_return, wlanbt_info_return, path_info_return
    else:
        print("Read config file failed.")
