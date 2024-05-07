import openpyxl
from openpyxl.styles import Alignment
from openpyxl.worksheet.datavalidation import DataValidation

# Version dev1.6.2 for new SOW format:
# SOW Date:2024/05
# Driver List templet version:v3
# ODM Driver 宣導事項:20240502 

list_templet_version = "v3"

def set_border(ws, cell_range):
    # border around
    # ref.: https://jingwen-z.github.io/how-to-munipulate-excel-workbook-by-python/
    rows = ws[cell_range]
    side = openpyxl.styles.Side(border_style="thick", color="000000") 

    rows = list(rows)
    max_y = len(rows) - 1  # index of the last row
    for pos_y, cells in enumerate(rows):
        max_x = len(cells) - 1  # index of the last cell
        for pos_x, cell in enumerate(cells):
            border = openpyxl.styles.Border(
                left=cell.border.left,
                right=cell.border.right,
                top=cell.border.top,
                bottom=cell.border.bottom
            )
            if pos_x == 0:
                border.left = side
            if pos_x == max_x:
                border.right = side
            if pos_y == 0:
                border.top = side
            if pos_y == max_y:
                border.bottom = side

            # set new border only if it's one of the edge cells
            if pos_x == 0 or pos_x == max_x or pos_y == 0 or pos_y == max_y:
                cell.border = border


def create_list(list_info, os_info, data_input, data_all_input):
    ## Creat list and save as Excel
    list_ver = "v" + list_info[2]
    year_month_day = list_info[3].replace("/", "") # Modify the date format to name the file. e.g. 2024/05/06 to 20240506
    fn_temp = [list_info[1], "Driver List", os_info[0] +" " + os_info[1], list_ver, year_month_day, list_templet_version]
    fn_temp = "_".join(fn_temp)
    fn = fn_temp + ".xlsx"

    wb = openpyxl.Workbook()
    wb_1 = wb.create_sheet("The lastest release", 0) # Add worksheet and specify location
    wb_2 = wb.create_sheet("Release note", 0)

    # Set the drop-down Menu content
    provider_ODM_dropdown_list = ["ODM", "ASUS"]
    driver_type_dropdown_list = ["DC", "DCH", "DCHU"]
    HSA_dropdown_list = ["Yes", "No"]
    WHQL_dropdown_list = ["Yes", "No"]
    CVM_dropdown_list = ["Hardware", "Software", "StoreApp"] # CVM is mean: Check version mechanism
    install_method_dropdown_list = ["online", "offline"]
    need_reboot_dropdown_list = ["Yes", "No"]


    # Define cell color and fill it
    cell_A1_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="FFFF00")
    title_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="4F81BD")
    blank_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="DCE6F1")
    gray_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="C0C0C0")
    yellow_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="FFFF00") # same as cell_A1_color_fill
    
    wb_1.merge_cells("A1:W1") # merge cells
    wb_1["A1"].fill = cell_A1_color_fill

    for row in wb_1["A2:W2"]: # This line for fill cell color by column
        for cell in row:
            cell.fill = title_color_fill

    for i in range(0, len(data_input), 2): # Odd column
        for row in wb_1["A{}:W{}".format(str(i+3), str(i+3))]: # +3 for cell column number in Driver list
            for cell in row:
                cell.fill = blank_color_fill

    # Border
    thin = openpyxl.styles.Side(border_style="thin", color="000000") 
    thick = openpyxl.styles.Side(border_style="thick", color="000000") 
    border = openpyxl.styles.Border(left=thin, right=thin, top=thin, bottom=thin)
    thick_border = openpyxl.styles.Border(left=thick, right=thick, top=thick, bottom=thick)

    for row in wb_1["A2:W{}".format(str(len(data_input)+2))]:
        for cell in row:
            cell.border = border

    # Font define
    title_font = openpyxl.styles.Font(size=12, bold=False, name='Arial Unicode MS', color="FFFFFF")
    content_font = openpyxl.styles.Font(size=10, bold=False, name='Verdana', color="000000")
    sheetRN_content_font = openpyxl.styles.Font(size=12, bold=False, name='Verdana', color="000000")
    sheetRN_cell_font = openpyxl.styles.Font(size=12, bold=False, name='Calibri', color="000000")
    sheetRN_cell_font_red = openpyxl.styles.Font(size=12, bold=False, name='Calibri', color="FF0000")

    # Alignment define
    content_align = Alignment(horizontal = "center")
    content_column_non_align_list = [1, 2, 15, 16, 22, 23] # column : [A, B, O, P, V, W] do not participate in alignment.
    content_column_non_align_list = [temp - 1 for temp in content_column_non_align_list] # Do -1 for excel format in python for loop.

    # List title at excel cell:"A1"
    cell_A1_title = [str(list_info[1]), "Driver List -", str(os_info[0]), str(os_info[1]), "- DriverList Version:", str(list_info[2]), "- Release Date:", str(list_info[3])]
    cell_A1_title = " ".join(cell_A1_title)
    wb_1["A1"].value = str(cell_A1_title)
    wb_1["A1"].font = content_font

    ## row2_column_title : Each column title at "The lastest release" (row 2)
    row2_column_title = ["Category", "Description", "Provider/ ODM Company or ASUS", "Vendor", "Driver type", "HSA", "APP ID (If supported)", "APP Name",
                         "Support side link", "Support OS", "WHQL", "Check version mechanism", "Hardware ID", "Target INF Name", "Driver version", "Driver Date",
                         "VersionRegKey", "Install command", "Install method", "Match FW Version", "Need reboot(Y/N)", "Driver package", "Remark"]


    for i in range(len(row2_column_title)):
        wb_1.cell(column=i+1, row=2).value = str(row2_column_title[i])
        wb_1.cell(column=i+1, row=2).font = title_font

    # All list to excel, modify font and alignment
    for i in range(0, len(data_all_input)): # i = number of columns.
        wb_1.cell(column=i+1, row=2).alignment = content_align
        for j in range(0, len(data_all_input[i])): # j = number of rows.
            if i in content_column_non_align_list: # column which do not participate in alignment.
                wb_1.cell(column=i+1, row=j+3).value = str(data_all_input[i][j])
                wb_1.cell(column=i+1, row=j+3).font = content_font
            else:
                wb_1.cell(column=i+1, row=j+3).value = str(data_all_input[i][j])
                wb_1.cell(column=i+1, row=j+3).font = content_font
                wb_1.cell(column=i+1, row=j+3).alignment = content_align


    # Set the drop-down Menu to specified cell
    dv_provider_ODM = DataValidation(type="list", formula1='"%s"' % ','.join(provider_ODM_dropdown_list), showDropDown=False, allowBlank=True)
    dv_driver_type = DataValidation(type="list", formula1='"%s"' % ','.join(driver_type_dropdown_list), showDropDown=False, allowBlank=True)
    dv_HSA = DataValidation(type="list", formula1='"%s"' % ','.join(HSA_dropdown_list), showDropDown=False, allowBlank=True)
    dv_WHQL = DataValidation(type="list", formula1='"%s"' % ','.join(WHQL_dropdown_list), showDropDown=False, allowBlank=True)
    dv_CVM = DataValidation(type="list", formula1='"%s"' % ','.join(CVM_dropdown_list), showDropDown=False, allowBlank=True)
    dv_IM = DataValidation(type="list", formula1='"%s"' % ','.join(install_method_dropdown_list), showDropDown=False, allowBlank=True)
    dv_need_reboot = DataValidation(type="list", formula1='"%s"' % ','.join(need_reboot_dropdown_list), showDropDown=False, allowBlank=True)

    # add data validation to workbook
    wb_1.add_data_validation(dv_provider_ODM)
    wb_1.add_data_validation(dv_driver_type)
    wb_1.add_data_validation(dv_HSA)
    wb_1.add_data_validation(dv_WHQL)
    wb_1.add_data_validation(dv_CVM)
    wb_1.add_data_validation(dv_IM)
    wb_1.add_data_validation(dv_need_reboot)

    # Specifying the applied range
    applied_row_end = len(data_all_input[0]) + 2 # len(data_all_input)為輸出 row 數，由於從 3 row 開始記，因此要+2
    dv_provider_ODM.sqref = "C3:C{}".format(applied_row_end)
    dv_driver_type.sqref = "E3:E{}".format(applied_row_end)
    dv_HSA.sqref = "F3:F{}".format(applied_row_end)
    dv_WHQL.sqref = "K3:K{}".format(applied_row_end)
    dv_CVM.sqref = "L3:L{}".format(applied_row_end)
    dv_IM.sqref = "S3:S{}".format(applied_row_end)
    dv_need_reboot.sqref = "U3:U{}".format(applied_row_end)
    
    # Set column width
    dims = {}
    for row in wb_1.rows:
        for cell in row:
            if cell.value:
                dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))
    for col, value in dims.items():
        if value <= 20:
            wb_1.column_dimensions[col].width = 20
        else:
            wb_1.column_dimensions[col].width = value + 7

    wb_1.column_dimensions["A"].width = 30 # A column do not automatically adjust column width (Cause A1)


    # create release note sheet (sheetRN) (wb_2)
    os_edition = str(os_info[0]) # e.g. Win11
    os_version = str(os_info[1]) # 22H2
    os_build = str(os_info[2]) # 22621.3
    update_date = str(list_info[3]) # 2022/11/18
    list_version = str(list_info[2]) # 0.01
    subject_str = "First release for {} OS.".format(os_version)

    ## Version dev1.6.2 for new SOW test.

    sheetRN_title_str = "ASUSTek Computer Inc."
    sheetRN_DLvControlRule_str = "Driver List Version control rule : SR/ER --> start from 0.01 ; PR --> Start from 1.00 ; MP --> Start from 2.00"
    sheetRN_column_title_list = ["Version", "Release Date", "Subject", "OS", "Remark"]
    sheetRN_column_ini_content_list = [list_version, update_date, subject_str, os_edition, ""]
    sheetRN_column_width_list = [9, 14, 104, 23, 45]


    for i in range(0, len(sheetRN_column_title_list)):
        wb_2.cell(column=i+1, row=2).value = str(sheetRN_column_title_list[i])
        wb_2.cell(column=i+1, row=2).font = sheetRN_cell_font

        wb_2.cell(column=i+1, row=3).value = str(sheetRN_column_ini_content_list[i])
        wb_2.cell(column=i+1, row=3).font = sheetRN_cell_font

        wb_2.cell(column=i+1, row=2).alignment = Alignment(horizontal = "center", vertical = "center")
        wb_2.cell(column=i+1, row=3).alignment = Alignment(horizontal = "center", vertical = "center") 

        col = wb_2.cell(column=i+1, row=2).column_letter
        wb_2.column_dimensions[col].width = sheetRN_column_width_list[i]
    
    wb_2.merge_cells("A1:E1") # merge cells
    wb_2["A1"].value = str(sheetRN_title_str)
    wb_2["A1"].font = sheetRN_cell_font
    wb_2["A1"].alignment = Alignment(horizontal = "center", vertical = "center") 
    wb_2["C5"].value = str(sheetRN_DLvControlRule_str)
    wb_2["C5"].font = sheetRN_cell_font_red
    
    for row in wb_2["A1:E1"]: # This line for fill cell color by column
        for cell in row:
            cell.fill = yellow_color_fill

    for row in wb_2["A2:E2"]: # This line for fill cell color by column
        for cell in row:
            cell.fill = gray_color_fill

    # set border
    for row in wb_2["A2:E3"]:
        for cell in row:
            cell.border = border

    BORDER_LIST = ["A2:E2"]
    for pos in BORDER_LIST: 
        set_border(wb_2, pos)


    # Save to exccel file
    try:
        del wb["Sheet"] # Delete default sheet which name is "Sheet"
        wb.save(fn)
    except:
        print("\nExcel WARNING : Please try closing the excel file and RE-RUN the program.")
