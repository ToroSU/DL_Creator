from ctypes import alignment
import openpyxl
from openpyxl.styles import Alignment

def update_list():
    pass

def creat_list(list_info, os_info, data_input, data_all_input):
    # Creat list and save as Excel
    list_ver = "v" + list_info[2]
    fn_temp = [list_info[1], os_info[0], os_info[1], "x64", "Drv", list_ver]
    fn_temp = "_".join(fn_temp)
    fn = fn_temp + ".xlsx"

    wb = openpyxl.Workbook()
    wb_1 = wb.create_sheet("The lastest release ", 0) # Add worksheet and specify location
    wb_2 = wb.create_sheet("Release note", 0)

    # Define cell color and fill it
    cell_A1_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="FFFF00")
    title_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="4F81BD")
    blank_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="DCE6F1")
    wb_2_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="BFBFBF")
    
    wb_1["A1"].fill = cell_A1_color_fill # Fill cell A1
    
    for row in wb_1["A2:W2"]: # This line for fill cell color by column
        for cell in row:
            cell.fill = title_color_fill

    for i in range(0, len(data_input), 2): # Fill in by interval, +3 for cell column number in Driver list
        for row in wb_1["A{}:W{}".format(str(i+3), str(i+3))]:
            for cell in row:
                cell.fill = blank_color_fill

    for row in wb_2["A4:F4"]: 
        for cell in row:
            cell.fill = wb_2_color_fill


    # Border
    thin = openpyxl.styles.Side(border_style="thin", color="000000") 
    border = openpyxl.styles.Border(left=thin, right=thin, top=thin, bottom=thin)

    for row in wb_1["A2:W{}".format(str(len(data_input)+2))]:
        for cell in row:
            cell.border = border
    
    for row in wb_2["A4:F5"]:
        for cell in row:
            cell.border = border


    # Font define
    title_font = openpyxl.styles.Font(size=12, bold=True, name='Arial Unicode MS', color="FFFFFF")
    content_font = openpyxl.styles.Font(size=10, bold=False, name='Verdana', color="000000")
    wb_2_font = openpyxl.styles.Font(size=12, bold=False, name='Calibri', color="000000")

    # Alignment define
    content_align_horizon = Alignment(horizontal = "center")
    content_column_non_align_list = [1, 2, 16, 17, 22] # column : [A, B, P, Q, V] do not participate in alignment.
    content_column_non_align_list = [temp - 1 for temp in content_column_non_align_list] # Do -1 for excel format in python for loop.

    # wb_2, row4_column_title: Each column title at "Release note" (row 4)
    row4_column_title = ["Version", "Release Date", "Subject", "OS", "Version", "Remark"]

    for i in range(0, len(row4_column_title)):
        wb_2.cell(column=i+1, row=4).value = str(row4_column_title[i])

    wb_2["A5"].value = str(list_info[2]) # list version: 0.01
    wb_2["B5"].value = str(list_info[3]) # Release date: 2022/10/13
    wb_2["C5"].value = str("First release") 
    wb_2["D5"].value = str(os_info[0]) # OS: Win11
    wb_2["E5"].value = str(os_info[2]) # OS version: 22621.3

    for i in range(0, 6): # column A to F
        for j in range(0, 5): # row 1 to 5
            wb_2.cell(column=i+1, row=j+1).font = wb_2_font

    # wb_2, cell:"A1", "F1"
    wb_2.merge_cells("A1:E1")
    wb_2_cell_A1_title = "\"Driver List-{}\" Model Release Notes".format(os_info[0])
    wb_2["A1"].value = str(wb_2_cell_A1_title)
    wb_2["A1"].alignment = content_align_horizon

    wb_2_cell_F1 = "Update Date:{}".format(list_info[3]) #e.g. Update Date:2022/10/13
    wb_2["F1"].value = str(wb_2_cell_F1)
    wb_2["F1"].alignment = Alignment(horizontal = "right")


    # wb_1, List title at excel cell:"A1"
    cell_A1_title = [str(list_info[1]), "Driver List -", str(os_info[0]), str(os_info[1]), "Version:", str(list_info[2]), "- Update Date:", str(list_info[3])]
    cell_A1_title = " ".join(cell_A1_title)
    wb_1["A1"].value = str(cell_A1_title)
    wb_1["A1"].font = content_font


    # wb_1, row2_column_title : Each column title at "The lastest release" (row 2)
    row2_column_title = ["Category", "Description", "Provider/ODM", "Vendor", "List of Support model name", "Driver type", "HSA", "APP ID", "APP Name",
                         "Support side link", "Extension ID", "Support OS", "WHQL", "Check version mechanism", "Hardware ID", "Driver version", "Driver Date",
                         "VersionRegKey", "Silent install command", "Match FW Version", "Need reboot(Y/N)", "Driver package", "Remark"]

    for i in range(len(row2_column_title)):
        wb_1.cell(column=i+1, row=2).value = str(row2_column_title[i])
        wb_1.cell(column=i+1, row=2).font = title_font

    # All list to excel, modify font and alignment
    for i in range(0, len(data_all_input)): # i = number of columns.
        wb_1.cell(column=i+1, row=2).alignment = content_align_horizon
        for j in range(0, len(data_all_input[i])): # j = number of rows.
            if i in content_column_non_align_list: # column which do not participate in alignment.
                wb_1.cell(column=i+1, row=j+3).value = str(data_all_input[i][j])
                wb_1.cell(column=i+1, row=j+3).font = content_font
            else:
                wb_1.cell(column=i+1, row=j+3).value = str(data_all_input[i][j])
                wb_1.cell(column=i+1, row=j+3).font = content_font
                wb_1.cell(column=i+1, row=j+3).alignment = content_align_horizon

    for i in range(0, len(row4_column_title)): # wb_2, row 4, row 5 alignment
        wb_2.cell(column=i+1, row=4).alignment = content_align_horizon
        wb_2.cell(column=i+1, row=5).alignment = content_align_horizon

    wb_2["C5"].alignment = Alignment(horizontal = "left")

    # Set wb_1 column width
    dims = {}
    for row in wb_1.rows: # wb_1
        for cell in row:
            if cell.value:
                dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))
    for col, value in dims.items():
        if value <= 20:
            wb_1.column_dimensions[col].width = 20
        else:
            wb_1.column_dimensions[col].width = value + 7

    wb_1.column_dimensions["A"].width = 30 # A column do not automatically adjust column width (Cause A1)

    # Set wb_2 column width
    wb_2.column_dimensions["A"].width = 15
    wb_2.column_dimensions["B"].width = 15
    wb_2.column_dimensions["C"].width = 100
    wb_2.column_dimensions["D"].width = 15
    wb_2.column_dimensions["E"].width = 15
    wb_2.column_dimensions["F"].width = 30

    # Delete default sheet which name is "Sheet"
    del wb["Sheet"]

    # Save to exccel file
    try:
        wb.save(fn)
        wb.close()
    except:
        print("\nExcel WARNING : Please try closing the excel file and RE-RUN the program.")
    