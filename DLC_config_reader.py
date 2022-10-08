import os
import configparser
# Reference of ConfigParser https://docs.python.org/3/library/configparser.html


def if_config_file_exist(file_name):
    config = configparser.ConfigParser()
    config.read(file_name)

    try:
        list_info = config["List Info"]
        list_info_return = [list_info["Customer"],
                            list_info["ProjectName"],
                            list_info["ListVersion"],
                            list_info["UpdateDate"]]

        os_info = config["OS Info"]
        os_info_return = [os_info["OSEdition"],
                          os_info["OSVersion"],
                          os_info["OSBuild"]]

        data_source = config["Data Source"]
        data_source_return = [data_source["FromSystem"],
                              data_source["FromPackage"],
                              data_source["PackagePath"]]

        other_setting = config["Other Setting"]
        other_setting_return = [other_setting["ExportDriverList"],
                                other_setting["DriverComfirm"],
                                other_setting["Package2Zip"]]

        wlanbt_info = config["WLANBT Info"]
        wlanbt_info_return = [wlanbt_info["Total"],
                              wlanbt_info["Intel"],
                              wlanbt_info["Azwave_MTK"],
                              wlanbt_info["Azwave_Realtek"],
                              wlanbt_info["Liteon_Realtek"],
                              wlanbt_info["Liteon_Qualcomm"]]

        return list_info_return, os_info_return, data_source_return, other_setting_return, wlanbt_info_return

    except:
        print("Error") # TODO: get error location and show to user.

def if_config_file_not_exits():

    list_info_return = ["T", "Test_01T", "0.01", "1970/01/01"]
    os_info_return = ["Win11", "21H2R", "22000.318"]
    data_source_return = ["No", "Yes", ""]
    other_setting_return = ["Yes", "No", "No"]
    wlanbt_info_return = ["4", "ax201", "", "", "", ""]

    return list_info_return, os_info_return, data_source_return, other_setting_return, wlanbt_info_return


## Main
def DLC_config_reader_main():
    config_filename = "DLC_config.ini"

    # Try to read config.ini file, if can't read file, use default setting
    if os.path.isfile(config_filename):
        print("Read config file successfully.")
        list_info_return, os_info_return, data_source_return, other_setting_return, wlanbt_info_return = if_config_file_exist(config_filename)
        return list_info_return, os_info_return, data_source_return, other_setting_return, wlanbt_info_return
    else:
        print("Read config file failed.")
        list_info_return, os_info_return, data_source_return, other_setting_return, wlanbt_info_return = if_config_file_not_exits()
        return list_info_return, os_info_return, data_source_return, other_setting_return, wlanbt_info_return
