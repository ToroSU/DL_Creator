import re
import os
import zipfile
import xml.etree.ElementTree as ET

# Version dev1.6.3 for new SOW format:
# SOW Date:2024/05
# Driver List templet version:v3
# ODM Driver 宣導事項:20240502 

# check list, Used to check if there is a preferred inf file
# 引入方式可以後續修正，以另外的公開文件來修改
# Audio Codec: HWID/Driver version/Driver build date填寫時參考Codec資料夾內的inf(以專案是否support ISST決定，例支援ISST需參考HDXSSTASUS.inf，不支援ISST需參考HDXASUS.inf)
# IntelliGo APO: HWID以及Driver version請填寫HDX_AsusExt_XPERI4_DSP_iGo_Ext.inf/ HDX_AsusExt_XPERI4_DSP_iGo_Ext_Capx.inf/HDX_AsusExt_XPERI4_DSP_iGo_Ext_Capx_DMVP_VPNR.inf中專案對應的項目
# Dolby: HWID以及Driver version請填寫dax3_ext_rtk.inf 中專案對應的項目
# Dirac: HWID/Driver version/Driver build date填寫時參考DiracExt.inf
# BT/WLAN: Intel Inf 請參考branch out documentation
# Intel_DPTF: Load inf：dptf_acpi.inf
# RTK LAN: NDIS架構: rt640x64.inf, NetAdapter架構:RTL 8125: rt25cx21x64.inf/ RTL 8168: rt68cx21x64.inf
# Intel_MEI: HWID/Driver version/Driver build date填寫時參考heci.inf
# Intel_HID: HWID填寫時請注意檢查Intel HidEventFilter.inf 有針對不同platform指定不同IDs, 若有BIOS 宣告不正確, 也請告知貴司BIOS做修正
# 

inf_check_list = ['AlderLakePCH-PSystem.inf', 'heci.inf', 'iaStorVD.inf', 'iaLPSS2_GPIO2_ADL.inf', 
                'iaLPSS2_I2C_ADL.inf', 'iigd_dch_d.inf', 'iigd_dch.inf', 'intcaudiobus.inf', 
                'HDXSSTASUS.inf', 'e1d.inf', 'HidEventFilter.inf', 'gna.inf', 'ISH.inf', 'Netwtw08.INF', 
                'ibtusb.inf', 'ICPSComponent.inf', 'mtkwl6ex.inf', 'mtkbtfilter.inf', 'RtsUer.inf', 
                'RtAsus.inf', 'snDMFT.inf', 'WbfUsbDriver.inf', 'HDX_AsusExt_XPERI4_DSP_iGo_Ext_Capx_DMVP_VPNR.inf', 'AsusNUMPADFilter.inf', 
                'AsusPTPFilter.inf', 'dax3_ext_rtk.inf', 'RaptorLakePCH-SSystem.inf', 'iaLPSS2_GPIO2_RPL.inf',
                'iaLPSS2_I2C_ADL.inf', "DiracExt.inf", "dptf_acpi.inf"]

inf_check_list_lower = [temp.lower() for temp in inf_check_list] # Convert inf_check_list to lowercase

def str2bool(v):
    return str(v).lower() in ("yes", "true", "t")

def file_reader(file_):
    # Open the .inf file. If open faild, try to use "utf-16" decode and ignore the error.
    try:  #utf-8 & utf-16 
        f = open(file_, encoding="utf-8")
        lines_ = f.readlines()
        f.close()
    except:
        try :
            f = open(file_, encoding="utf-16-le") # UTF16-LE
            # print(file_, " not utf-8 encode")
            lines_ = f.readlines()
            f.close()
        except :
            f = open(file_, encoding="iso_8859_1") # ANSI
            lines_ = f.readlines()
            f.close()

    return lines_


def name_split_get(input):
    # Split folder name for subsequent analysis
    path_split = (input.split("\\")) # e.g. ["14_WLANBT_Intel", "WLAN", "WiFi_Intel_22.150.0.3"] ## for full path:['C:', 'Users', 'EddieYW_Su', 'Desktop', 'A5Test', '03_IRST_Intel', 'RST_PV_19.5.7.1058.1_SV2_SV1_Win10']
    #folder_root_name = path_split[0] # e.g. 03_IRST_Intel
    folder_root_name = path_split[-2] # test for full path
    name_split = folder_root_name.split("_") # e.g. ['03', 'IRST', 'Intel']
    
    return path_split, folder_root_name, name_split


def ver_date_get(inf_file):
    driver_ver='DriverVer'
    lines_ = file_reader(inf_file)
    for line in lines_:
        if driver_ver in line:
            driver_ver_line = line # e.g. DriverVer = 05/30/2022,22.150.0.6
            try:
                driver_ver_line = driver_ver_line.split('=')[1] # e.g. 05/30/2022,22.150.0.6
                date_, ver_ = driver_ver_line.split(',')
                date_str = re.sub(r"^\s+|\s+$", "", date_) # remove white-space

                if ";" in ver_:
                    ver_str = ver_.split(';')[0] 
                    ver_str = re.sub(r"^\s+|\s+$", "", ver_str)
                else:
                    ver_str = re.sub(r"^\s+|\s+$", "", ver_)
            except:
                continue

            return ver_str, date_str


def obtain_used_module(wlanbt_info):
    # get used wlanbt module : output: [[0, "Wlan", "Ax201"], [0, "Bluetooth", "Ax201"]....]
    wlanbt_module_list = []

    for i in range(0, len(wlanbt_info)):
        temp_ = wlanbt_info[i].replace('"', '') #去掉雙引號 這邊很78要注意用單引號框起來
        temp_ = temp_.replace(" ", "")
        temp_ = temp_.split(",")
        for j in range(0, len(temp_)):
            for wlan_bt_ in ["Wlan", "Bluetooth"]:
                temp_list = []
                temp_list.append(i)
                temp_list.append(wlan_bt_)
                temp_list.append(temp_[j])
                wlanbt_module_list.append(temp_list)
    
    wlanbt_total_count = 0
    use_wlanbt_list = []
    for item_ in (wlanbt_module_list): # wlanbt_module_list format:[wlanbt_i, ["Wlan", "Bluetooth"], module(e.g.Ax201)]
        if item_[2] != "":  # wlanbt_i=0~4, 0:intel, 1:AzwveMTK... also see config.ini file
            wlanbt_total_count += 1
            use_wlanbt_list.append(item_)

    return use_wlanbt_list, wlanbt_total_count


def search_wlanbt(package_list_):
    wlanbt_list_for_gui = []
    for i in range(0, len(package_list_)):
        path_split, folder_root_name, name_split = name_split_get(package_list_[i])
        if any("wlanbt" in s.lower() for s in name_split):
            wlanbt_list_for_gui.append(package_list_[i])
    return wlanbt_list_for_gui


def final_list_sort(raw_path_list_input, raw_AUMIDs_list_input, modules_list):
    # 先以相同規則創建出 item_list
    raw_item_list = []
    for i in range(0, len(raw_path_list_input)):
        path_split, folder_root_name, name_split = name_split_get(raw_path_list_input[i]) # name_split : e.g. ['03', 'IRST', 'Intel']
        name_split.pop(0) # pop up the item first split:"00"~"xx"
        item_str = " ".join(name_split) # e.g. IRST Intel
        raw_item_list.append(item_str)

    # 尋找 raw_path_list_input 中含有 "WLANBT" 關鍵字的項目，並記錄index
    keyword_ = "wlanbt"
    indexes_of_path_with_the_keyword = [] # find index of path with keyword:"WLANBT" e.g. [6, 7, 8, 9, 10]
    for i in range(0, len(raw_path_list_input)):
        if keyword_ in raw_path_list_input[i].lower():
            indexes_of_path_with_the_keyword.append(i)

    first_index = indexes_of_path_with_the_keyword[0] # the index of the first found keyword (這個要放在前面，不然會有reverse的奇怪bug，懶得解)
    del_i = indexes_of_path_with_the_keyword # 解惑下一行，python 中list, dict, class這類型態使用=會指向同一個list, dict, class，因此需要進行額外處理。
    del_i.reverse() # reverse the index list to remove found target (first_index 放在這行後面會被 reverse)
    

    # 同步刪除 raw_path_list_input, raw_AUMIDs_list_input, raw_item_list，因為這三個 list 為對應關係
    for i in del_i:
        del raw_path_list_input[i]
        del raw_AUMIDs_list_input[i]
        del raw_item_list[i]

    # 插入由使用者在 wlanbt select GUI 選定的 driver path, 及當時自動生成的 item string (item string: e.g. Bluetooth (Ax201)), AUMIDS 插入"NA"
    wlanbt_final_item_list = []
    wlanbt_final_path_list = []
    for i in range(0, len(modules_list)):
        wlan_str_temp = f"Wlan ({modules_list[i][1]})"
        bt_str_temp = f"Bluetooth ({modules_list[i][1]})"
        wlan_path_temp = modules_list[i][2]
        bt_path_temp = modules_list[i][4]
        #item part
        wlanbt_final_item_list.append(wlan_str_temp)
        wlanbt_final_item_list.append(bt_str_temp)
        #path part
        wlanbt_final_path_list.append(wlan_path_temp)
        wlanbt_final_path_list.append(bt_path_temp)

    raw_item_list[first_index:first_index] = wlanbt_final_item_list # 插入 wlanbt item
    raw_path_list_input[first_index:first_index] = wlanbt_final_path_list # 插入 wlanbt path
    aumids_insert_NA_list = []
    # 計算wlanbt 的數量，加入同等數量的"NA"
    for i in range(0, len(wlanbt_final_item_list)):
        aumids_insert_NA_list.append("NA") 
    
    raw_AUMIDs_list_input[first_index:first_index] = aumids_insert_NA_list

    # 單純改變數名稱
    final_item_list = raw_item_list
    final_bat_path_list = raw_path_list_input
    final_aumids_path_list = raw_AUMIDs_list_input

    return final_item_list, final_bat_path_list, final_aumids_path_list


def category_list_get(item_list):
    category_list = item_list
    
    return category_list

def get_appx_version(appx_bundle_path):
    """ get the version from appxbundle file """

    namespaces = { # namespace for appxbundle file
    'a1': 'http://schemas.microsoft.com/appx/manifest/foundation/windows10',
    '': 'http://schemas.microsoft.com/appx/2013/bundle',
    'b4': 'http://schemas.microsoft.com/appx/2018/bundle',
    'b5': 'http://schemas.microsoft.com/appx/2019/bundle'
    }
    
    with zipfile.ZipFile(appx_bundle_path, 'r') as zip_file:
        # 找到 AppxManifest.xml 檔案
        for file_name in zip_file.namelist():
            if file_name.endswith('AppxBundleManifest.xml'):
                # 讀取 AppxBundleManifest.xml 的內容
                with zip_file.open(file_name) as manifest_file:
                    manifest_xml = manifest_file.read()
                    
                # 解析 XML 資訊
                root = ET.fromstring(manifest_xml)
                package_elements = root.findall(f"./{{{namespaces['']}}}Packages/{{{namespaces['']}}}Package")

                for package_element in package_elements:
                    version = package_element.get('Version')

                    return version

            elif file_name.endswith('AppxManifest.xml'):
                # 讀取 AppxBundleManifest.xml 的內容
                with zip_file.open(file_name) as manifest_file:
                    manifest_xml = manifest_file.read()
                    
                # 解析 XML 資訊
                root = ET.fromstring(manifest_xml)
                
                package_elements = root.findall(f"./{{{namespaces['a1']}}}Identity")
                for package_element in package_elements:
                    version = package_element.get('Version')

                    return version


def infFile_ver_date_list_get(item_list_path):
    # 待完成指定inf功能，目前是選程式找到的其中一個inf來使用
    # Description 搜尋功能未完成
    infFile_lsit = []
    driverVersion_list = []
    driverDate_list = []
    file_break = False
    aumids_break = False
    for root_i in range(0, len(item_list_path)):
        for root, dirs, files in os.walk(item_list_path[root_i]):
            for file in files:
                if file[-4:].lower() == ".inf": # 轉換小寫，因為intel wlan的是愚蠢的大寫INF 除錯超久可悲
                    inf_file_path = os.path.join(root, file)
                    driverVersion_str, driverDate_str = ver_date_get(inf_file_path)
                    file_str = file
                    file_break = True
                    break

                elif file == "AUMIDs.txt":
                    file_str = "AUMIDs"
                    aumids_break = True
                    break

            if file_break or aumids_break: # 有拿到inf或aumids就跳出
                file_break = False
                aumids_break = False
                break

        infFile_lsit.append(file_str)
        driverVersion_list.append(driverVersion_str)
        driverDate_list.append(driverDate_str)

    return infFile_lsit, driverVersion_list, driverDate_list


def infFile_ver_date_list_get_with_checklist(item_list_path):
    # 配合check list 優化inf正確性
    # Description 搜尋功能未完成
    inf_File_list = []
    driverVersion_list = []
    driverDate_list = []
    # file_break = False
    # aumids_break = False
    for root_i in range(0, len(item_list_path)):
        inf_File_list_root = []
        driverVersion_list_root = []
        driverDate_list_root = []
        for root, dirs, files in os.walk(item_list_path[root_i]):
            for file in files:
                # TODO 加入check list的小判斷，後續可以改掉或優化，
                # 先把所有inf 列出，再看列出的inf有無在check中，若有:紀錄後跳出，若無:則使用list第一項
                if file[-4:].lower() == ".inf": # 轉換小寫，因為intel wlan的是愚蠢的大寫INF 除錯超久可悲
                    inf_file_path = os.path.join(root, file)
                    driverVersion_str, driverDate_str = ver_date_get(inf_file_path)
                    driverVersion_list_root.append(driverVersion_str)
                    driverDate_list_root.append(driverDate_str)
                    inf_File_list_root.append(file)

                elif ".appxbundle" in file or ".msix" in file:
                    file_str = "" # if appxbundle file exist, set as empty string 
                    appVersion = get_appx_version(os.path.join(root, file))
                    driverVersion_str = appVersion
                    driverDate_str = ""

                    break

        for i in range(0, len(inf_File_list_root)): # TODO reverse detect method, from inf_check_list_lower for loop name.
            if inf_File_list_root[i].lower() in inf_check_list_lower:
                file_str = inf_File_list_root[i]
                driverVersion_str = driverVersion_list_root[i]
                driverDate_str = driverDate_list_root[i]
                break
            
            else:
                file_str = inf_File_list_root[0]
                driverVersion_str = driverVersion_list_root[0]
                driverDate_str = driverDate_list_root[0]
                        
        inf_File_list.append(file_str)
        driverVersion_list.append(driverVersion_str)
        driverDate_list.append(driverDate_str)

    return inf_File_list, driverVersion_list, driverDate_list


def software_item_analysis(item_list_path):
    software_item_path = []
    # versionregKey_list = [] # for O column (2022/10/04), # 目前是瑕疵品，不知道怎麼完成，暫定寫死 (詳見輸出結果)
    # 2024/05/10 僅 CardReader 為Software item，非SOW，為客戶提供之資訊 
    folder_check_once = False
    for i in range(0, len(item_list_path)):
        path_split, folder_root_name, name_split = name_split_get(item_list_path[i])
        if name_split[1].lower() == "cardreader":
            software_item_path.append("True")
        else:
            software_item_path.append("NA")
    return software_item_path


def provider_list_get(item_list_path):
    # follow ODM Driver 宣導事項:20240502 
    # 除Intel Graphics 4IDs Driver、NVIDIA DT/AIO/NX Driver及PTP driver和Dolby driver由ASUS提供外，其於Driver皆由ODM自行與Driver廠商申請取得
    # ICPS APP 請ODM提供"檔案和版號" ，ICPS Driver 則提供"版號即可"，ASUS 會將driver DUA後release給ODM
    # Output : "ODM" or "ASUS"
    provider_list = []
    asus_own_driver=["graphics", "graphic", "numpad", "touchpad", "ptp", "dolby"]
    for i in range(0, len(item_list_path)):
        path_split, folder_root_name, name_split = name_split_get(item_list_path[i])
        provider_list.append("ODM") # 先預設都是 ODM
        for j in range(0, len(name_split)):
            name_split[j] = name_split[j].lower()
            if name_split[j] in asus_own_driver:
                provider_list[i] = "ASUS" # 發現為 ASUS Own 的再替換為 ASUS
                break

    return provider_list


def vendor_list_get(item_list_path):
    vendor_list = []
    for i in range(0, len(item_list_path)):
        path_split, folder_root_name, name_split = name_split_get(item_list_path[i])

        if len(name_split) >= 3 :
            vendor_list.append(name_split[2])
        else:
            vendor_list.append(" ")
    
    return vendor_list


def listOfsupportModelName_list_get(item_list_path):
    # to be clarified
    listOfsupportModelName_list = []
    for i in range(0, len(item_list_path)):
        listOfsupportModelName_list.append("")
    
    return listOfsupportModelName_list


def driverType_list_get(item_list_path):
    driverType_list = []
    for i in range(0, len(item_list_path)):
        driverType_list.append("DCH")

    return driverType_list


def hsa_list_get(item_list_path, aumids_path_list):
    hsa_list = []
    aumids_path_list.append("NA") # just for i+1 margin debug
    for i in range(0, len(item_list_path)):
        if aumids_path_list[i+1] != "NA":
            path_split, folder_root_name, name_split = name_split_get(aumids_path_list[i+1])
            
            name_split.pop(0)
            # item = " ".join(name_split) # e.g. ICPS Intel UI
            hsa_temp_str = "Yes"
            hsa_list.append(hsa_temp_str)
        else:
            hsa_list.append("No")

    return hsa_list


def appID_list_get(item_list_path, aumids_path_list):
    appID_list = []
    for i in range(0, len(aumids_path_list)):
        if aumids_path_list[i] != "NA":
            aumids_file_path = os.path.join(aumids_path_list[i], "AUMIDs.txt")
            lines_ = file_reader(aumids_file_path)
            appID_str = lines_[0].rstrip('\r\n')
            appID_list.append(appID_str)
        else:
            appID_list.append("")

    return appID_list


def appName_list_get(item_list_path, aumids_path_list):
    # complete by hard coding.
    appName_list = []
    appName_check_list_IGCC = ["graphics", "graphic", "vga"]
    appName_check_list_RealtekConsole = ["realtek", "rtk"]
    appName_check_list_ICPS = ["icps"]
    appName_check_list_Dolby = ["dolby"]
    appName_check_list_Intelligo = ["intelligo", "inteligo", "igo"]

    for i in range(0, len(item_list_path)):
        path_split, folder_root_name, name_split = name_split_get(item_list_path[i])

        if aumids_path_list[i]  != "NA":
            for j in range(0, len(name_split)): # just convert string lsit to lower. e.g. ['03', 'irst', 'intel']
                name_split[j] = name_split[j].lower()
                if name_split[j] in appName_check_list_IGCC:
                    appName_str = "Intel® Graphics Command Center"
                    break

                elif name_split[j] in appName_check_list_RealtekConsole:
                    appName_str = "Realtek Audio Console"
                    break

                elif name_split[j] in appName_check_list_ICPS:
                    appName_str = "Intel® Connectivity Performance Suite"
                    break

                elif name_split[j] in appName_check_list_Dolby:
                    appName_str = "Dolby Access"
                    break

                elif name_split[j] in appName_check_list_Intelligo:
                    appName_str = "ASUS AI Noise-canceling"
                    break
                
                else:
                    appName_str = "Error"
        else:
            appName_str = ""

        appName_list.append(appName_str)
    
    return appName_list


def supportSideLink_list_get(item_list_path):
    # to be clarified
    supportSideLink_list = []
    for i in range(0, len(item_list_path)):
        supportSideLink_list.append("")
    
    return supportSideLink_list


def extensionID_list_get(item_list_path):
    # to be clarified
    extensionID_list = []
    for i in range(0, len(item_list_path)):
        extensionID_list.append("")
    
    return extensionID_list


def supportOS_list_get(item_list_path, os_info):
    # ODM Driver 宣導事項:20240502
    # 此Driver支援的作業系統版本 ex: Win11 22H2
    supportOS_list = []
    for i in range(0, len(item_list_path)):
        supportOS_str = " ".join(os_info[0:2]) # 0: Win11, 1: 22H2
        supportOS_list.append(supportOS_str)

    return supportOS_list   


def whql_list_get(item_list_path, aumids_path_list, os_info):
    # After ODM Driver 宣導事項:20240502, the WHQL cell just has "Yes" or "No"
    # TODO: to be clarified how to get driver whql info, all set "Yes" now.
    whql_list = []
    for i in range(0, len(item_list_path)):
        if aumids_path_list[i] != "NA":
            whql_list.append("Yes")
        else:
            whql_list.append("Yes")

    return whql_list


def checkVersionMechanism_list_get(item_list_path, software_path_list, aumids_path_list):
    checkVersionMechanism_list = []
    for i in range(0, len(item_list_path)):
        if aumids_path_list[i] != "NA":
            string_ = "StoreApp"
        elif software_path_list[i] != "NA" and aumids_path_list[i] == "NA":
            string_ = "Software"
        else:
            string_ = "Hardware"
        
        checkVersionMechanism_list.append(string_)

    return checkVersionMechanism_list


def hardwareID_list_get(item_list_path):
    # to be clarified
    hardwareID_list = []
    for i in range(0, len(item_list_path)):
        hardwareID_list.append("")
    
    return hardwareID_list


def driverVersion_list_get():
    # pending
    pass


def driverDate_list_get():
    # pending
    pass

def versionRegKey_list_get(item_list_path, software_path_list):
    # 若Check Mechanism為"Software"則可由此欄位確認" VersionRegKey"之設定
    # for Q column (2024/05/08), # complete by hard coding. (can also check function: software_item_analysis)
    versionRegKey_list = []
    versionRegKey_check_list_igo = ["inteligo", "intelligo", "igo"]
    versionRegKey_check_list_dolby = ["dolby"]
    versionRegKey_check_list_cardreader = ["cardreader", "card"]
    versionRegKey_check_list_cardreader_realtek = ["realtek", "rtk"]
    versionRegKey_check_list_cardreader_genesys = ["genesys", "gene"]

    for i in range(0, len(item_list_path)):
        path_split, folder_root_name, name_split = name_split_get(item_list_path[i])

        if software_path_list[i]  != "NA":
            name_split = [item.lower() for item in name_split]
            if any(item in name_split for item in versionRegKey_check_list_igo):
                versionRegKey_str = "SOFTWARE\\Intelligo\\APO_Component\\DisplayVersion"

            elif any(item in name_split for item in versionRegKey_check_list_dolby):
                versionRegKey_str = "SOFTWARE\\ASUS\\Dolby_Atmos_for_PC_driver\\DisplayVersion"
            
            elif any(item in name_split for item in versionRegKey_check_list_cardreader) and any(item in name_split for item in versionRegKey_check_list_cardreader_realtek):
                versionRegKey_str =  "SOFTWARE\\Realtek\\Cardreader\\Version"
            
            elif any(item in name_split for item in versionRegKey_check_list_cardreader) and any(item in name_split for item in versionRegKey_check_list_cardreader_genesys):
                versionRegKey_str =  "HKEY_LOCAL_MACHINE\SOFTWARE\Genesys\Cardreader"

            else:
                versionRegKey_str = "Error"
        else:
            versionRegKey_str = "/"

        versionRegKey_list.append(versionRegKey_str)
    
    return versionRegKey_list

    

def silentInstallCommand_list_get(item_list_path):
    # 此欄位需與Driver package欄位的安裝檔案之install command相符，目前command一致為install.bat
    silentInstallCommand_list = []
    for i in range(0, len(item_list_path)):
        silentInstallCommand_list.append("Install.bat")

        batch_file_path = os.path.join(item_list_path[i], "Install.bat")
        if not os.path.isfile(batch_file_path):
            print("WARNING: ", "Install.bat is not included in :", item_list_path[i])
    
    return silentInstallCommand_list

def installMethod_list_get(item_list_path):
    # ASUS image安裝流程預設為offline安裝, 此安裝模式會在winpe中使用dism工具將*.inf 嵌入作業系統中, 若驅動程式安裝包中含有客製化指令及設定,則此項目請選擇online
    installMethod_list = []
    for i in range(0, len(item_list_path)):
        installMethod_list.append("") # 此項目取決於 Compal owner 是否有客制化需求，先空白
    
    return installMethod_list


def matchFwVersion_list_get(item_list_path):
    # 若無需搭配特定FW則設定為N/A
    matchFwVersion_list = []
    for i in range(0, len(item_list_path)):
        matchFwVersion_list.append("N/A")
    
    return matchFwVersion_list


def needReboot_list_get(item_list_path, aumids_path_list):
    # 若Driver安裝後需要reboot設定Y， 不需要reboot設定N
    # ODM Driver 宣導事項:20240502 與 Templet 內容有衝突，先不管 (Templet dropdown: Yes/No, ODM: Y/N)
    needReboot_list = []
    default_needReboot_item = ["graphics", "sst", "isst", "audio", "intelligo"]
    for i in range(0, len(item_list_path)):
        path_split, folder_root_name, name_split = name_split_get(item_list_path[i])

        for j in range(0, len(name_split)): # just convert string lsit to lower. e.g. ['03', 'irst', 'intel']
            name_split[j] = name_split[j].lower()
            if name_split[j] in default_needReboot_item and aumids_path_list[i] == "NA":
                needReboot_string = "Yes"
                break
            else:
                needReboot_string = "No"

        needReboot_list.append(needReboot_string)

    return needReboot_list
        

def driverPackage_list_get(item_list_path):
    driverPackage_list = []
    for i in range(0, len(item_list_path)):
        path_split = item_list_path[i].split("\\")
        driverPackage_path = path_split[-1]
        driverPackage_zip = driverPackage_path + ".zip"
        driverPackage_list.append(driverPackage_zip)
    
    return driverPackage_list


def remark_list_get(item_list_path):
    # just for create excel now
    remark_list = []
    for i in range(0, len(item_list_path)):
        remark_list.append("")
    
    return remark_list


def batch_and_aumids_file_get(package_list, path_info):
    # Batch / AUMIDs file path list, use .bat/ AUMIDs.txt to detect.
    # TODO bat file exist (maybe todo ...)
    batch_in_folder_path_list = []  # Main output 1: list of bat file path .
    AUMIDs_in_folder_path_list = [] # Main output 2 : list of AUMIDS file path. list amount same as Main output 1. 
    aumid_check = False # If aumid and bat file are in same folder, this para. will set as True.
    bat_check_list = ["SilentInstall.bat", "uninstall_all.bat"]

    for root_i in range(0, len(package_list)):
        if str2bool(path_info[0]):
            path_root = package_list[root_i]
        else:
            path_root=os.path.join(path_info[1], package_list[root_i]) # path_info[1] = C:\\Users\\EddieYW_Su\\Desktop\\A5Test

        for root, dirs, files in os.walk(path_root):
            for file in files:
                if file.lower() == "install.bat" and file not in bat_check_list: 
                    bat_root_checkpoint = root
                    batch_in_folder_path_list.append(root) # e.g. 14_WLANBT_Azwave_MTK\BT\BT_Azwave_MTK_MT7921_1.3.15.143
                    if not aumid_check: 
                        AUMIDs_in_folder_path_list.append("NA")
                    else:
                        aumid_check = False

                if file == "AUMIDs.txt":  # 有bug 檢查中10/01
                    if os.path.split(root)[0] == bat_root_checkpoint:
                        aumid_check = False
                        try: # 這邊寫法不好，應該透過If Else 判斷而非try except 後續修正
                            AUMIDs_in_folder_path_list.pop()
                            AUMIDs_in_folder_path_list.append(root)
                        except:
                            AUMIDs_in_folder_path_list.append(root)
                    else:
                        AUMIDs_in_folder_path_list.append(root)
                        aumid_check = True
                        
    return batch_in_folder_path_list, AUMIDs_in_folder_path_list


def all_List_get(item_list, item_list_path, aumids_path_list, os_info):
    all_list = []

    category_list = category_list_get(item_list)
    infFile_list, driverVersion_list_temp, driverDate_list_temp  = infFile_ver_date_list_get_with_checklist(item_list_path)
    software_path_list = software_item_analysis(item_list_path)

    provider_list = provider_list_get(item_list_path)
    vendor_list = vendor_list_get(item_list_path)
    listOfsupportModelName_list = listOfsupportModelName_list_get(item_list_path)
    driverType_list = driverType_list_get(item_list_path)
    hsa_list = hsa_list_get(item_list_path, aumids_path_list)
    appID_list = appID_list_get(item_list_path, aumids_path_list)
    appName_list = appName_list_get(item_list_path, aumids_path_list)
    supportSideLink_list = supportSideLink_list_get(item_list_path)
    extensionID_list = extensionID_list_get(item_list_path)
    supportOS_list = supportOS_list_get(item_list_path, os_info)
    whql_list = whql_list_get(item_list_path, aumids_path_list, os_info)
    checkVersionMechanism_list = checkVersionMechanism_list_get(item_list_path, software_path_list, aumids_path_list)
    hardwareID_list = hardwareID_list_get(item_list_path)
    driverVersion_list = driverVersion_list_temp
    driverDate_list = driverDate_list_temp
    versionRegKey_list = versionRegKey_list_get(item_list_path, software_path_list)
    silentInstallCommand_list = silentInstallCommand_list_get(item_list_path)
    installMethod_list = installMethod_list_get(item_list_path)
    matchFwVersion_list = matchFwVersion_list_get(item_list_path)
    needReboot_list = needReboot_list_get(item_list_path, aumids_path_list)
    driverPackage_list = driverPackage_list_get(item_list_path)
    remark_list = remark_list_get(item_list_path)
    
    # List append to tuple, format:[[category list], [description list], [provider list]...] sorting by excel column spec.
    all_list.append(category_list) #1
    all_list.append(remark_list) # 先預設空白 先用remark list填充(空白)，後續以inf回填 見remark
    all_list.append(provider_list) 
    all_list.append(vendor_list) 
    all_list.append(driverType_list) #5 E
    all_list.append(hsa_list)
    all_list.append(appID_list)
    all_list.append(appName_list)
    all_list.append(supportSideLink_list)
    all_list.append(supportOS_list) #10 J
    all_list.append(whql_list)
    all_list.append(checkVersionMechanism_list)
    all_list.append(hardwareID_list)
    all_list.append(infFile_list)
    all_list.append(driverVersion_list) #15 O
    all_list.append(driverDate_list)
    all_list.append(versionRegKey_list)
    all_list.append(silentInstallCommand_list)
    all_list.append(installMethod_list)
    all_list.append(matchFwVersion_list) # 20 T
    all_list.append(needReboot_list) 
    all_list.append(driverPackage_list)
    all_list.append(remark_list) # TODO: 實際為Remark, 目前用以檢查inf 回填用. 由於Asus有新增"Target .INF name" 欄位，後續用該欄檢查即可。

    return all_list 
