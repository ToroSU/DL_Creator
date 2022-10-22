import DLC_info_catch
from DLC_list2excel import creat_list
from DLC_config_reader import DLC_config_reader_main
import os
import time

# -*- coding: utf-8 -*-
""" File Name : run_main.py
The function of this program is automatically create "Driver List" from "Driver Package".
Update Date: 2022/10/06

"""

## def function
def str2bool(v):
    return str(v).lower() in ("yes", "true", "t")

def list_diff(li1, li2): 
    # https://magic-panda-engineer.github.io/Python/python-compare-two-lists
    return (list(set(li1).symmetric_difference(set(li2))))


start = time.time()
## Main
# TODO: GUI creat config.ini 
dir_path = os.getcwd() # get current path (as know as driver package path)
list_info, os_info, date_source, other_setting, wlanbt_info = DLC_config_reader_main()


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

## Analyze the folder name to choose catch method, then create item list of driver list.
# We focus on WLANBT folder now. (Cause this item will add another item in driver list)
# TODO VGA, Azwave_Realtek , Liteon_Realtek , Liteon_Qualcomm 
wlanbt_path_list = DLC_info_catch.wlanbt_analysis(batch_in_folder_path_list) # output format: [[intel wlan], [intel bt], [mtk wlan],
                                                                             #                 [mtk bt], [liteon wlan], [liteon bt]]

# Detect wlanbt module (e.g ax201, ax211) amount and wlanbt folder amount
# If wlan/bt folder of each vendor has different quantities, program will create a Warning message : wlan bt Folder maybe had erred
# item_list: list all item which need be in "Category column"
item_list, item_list_path, aumids_path_list= DLC_info_catch.wlanbt_item_add(batch_in_folder_path_list, AUMIDs_in_folder_path_list, wlanbt_path_list, wlanbt_info)

for i in range(0, len(wlanbt_path_list), 2):
    if len(wlanbt_path_list[i]) != len(wlanbt_path_list[i+1]):
        print("WARNING: Folder {}, WLAN and BT path maybe had erred!".format(wlanbt_path_list[i][0].split("\\")[0]))


## Obtain all list for final output.
print("\n-------------v Message Text v-------------\n")
all_list = DLC_info_catch.all_List_get(item_list, item_list_path, aumids_path_list, os_info)

## Output to Excel file.
if str2bool(other_setting[0]):
    creat_list(list_info, os_info, item_list, all_list) # input(list_info, os_info, <item_list>)
    print("\nFile output completed, path is: {}".format(dir_path))

else:
    print("\nExportDriverList= {}, do not export excel files.".format(other_setting[0]))


# Show information
end = time.time()
print("\nRuntime of the main program is {:.2f} s".format(end-start))

print("The program will automatically close after 30 seconds, or you can close the program manually.")
time.sleep(30)
