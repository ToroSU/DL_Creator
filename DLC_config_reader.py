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
                                other_setting["Package2Zip"]]

        wlanbt_info = config["WLANBT_Info"]
        wlanbt_info_return = [wlanbt_info["Intel"],
                              wlanbt_info["AzwaveMTK"],
                              wlanbt_info["AzwaveRTK"],
                              wlanbt_info["LiteonRTK"],
                              wlanbt_info["LiteonQualc"]]
        
        path_info = config["Path_Info"]

        # Normalize path before returning
        package_path = os.path.normpath(path_info["PackagePath"]) # If normalization is not done here, the output path will contain extra backslashes, e.g.,C:\\\\Users\\\\tester\\\\Desktop\\\\A5Test'
        path_info_return = [path_info["IsCurrentPath"], package_path]

        return list_info_return, os_info_return, other_setting_return, wlanbt_info_return, path_info_return

    except:
        print("Error") # TODO: get error location and show to user.


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
