import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment

def creat_list(list_info, os_info, data_input, data_all_input):
    ## Creat list and save as Excel
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
    border = openpyxl.styles.Border(left=thin, right=thin, top=thin, bottom=thin)

    for row in wb_1["A2:W{}".format(str(len(data_input)+2))]:
        for cell in row:
            cell.border = border

    # Font define
    title_font = openpyxl.styles.Font(size=12, bold=False, name='Arial Unicode MS', color="FFFFFF")
    content_font = openpyxl.styles.Font(size=10, bold=False, name='Verdana', color="000000")

    # Alignment define
    content_align = Alignment(horizontal = "center")
    content_column_non_align_list = [1, 2, 16, 17, 22] # column : [A, B, H, V] do not participate in alignment.
    content_column_non_align_list = [temp - 1 for temp in content_column_non_align_list] # Do -1 for excel format in python for loop.

    # List title at excel cell:"A1"
    cell_A1_title = [str(list_info[1]), "Driver List -", str(os_info[0]), str(os_info[1]), "Version:", str(list_info[2]), "- Update Date:", str(list_info[3])]
    cell_A1_title = " ".join(cell_A1_title)
    wb_1["A1"].value = str(cell_A1_title)
    wb_1["A1"].font = content_font

    # row2_column_title : Each column title at "The lastest release" (row 2)
    row2_column_title = ["Category", "Description", "Provider/ODM", "Vendor", "List of Support model name", "Driver type", "HSA", "APP ID", "APP Name",
                         "Support side link", "Extension ID", "Support OS", "WHQL", "Check version mechanism", "Hardware ID", "Driver version", "Driver Date",
                         "VersionRegKey", "Silent install command", "Match FW Version", "Need reboot(Y/N)", "Driver package", "Remark"]

    for i in range(len(row2_column_title)):
        wb_1.cell(column=i+1, row=2).value = str(row2_column_title[i])
        wb_1.cell(column=i+1, row=2).font = title_font

    # All list to excel, modify font and alignment
    for i in range(0, len(data_all_input)): # i = number of columns.
        wb_1.cell(column=i+1, row=2).alignment = content_align
        for j in range(0, len(data_all_input[i])): # j = number of rows.
            if i in content_column_non_align_list:
                wb_1.cell(column=i+1, row=j+3).value = str(data_all_input[i][j])
                wb_1.cell(column=i+1, row=j+3).font = content_font
            else:
                wb_1.cell(column=i+1, row=j+3).value = str(data_all_input[i][j])
                wb_1.cell(column=i+1, row=j+3).font = content_font
                wb_1.cell(column=i+1, row=j+3).alignment = content_align


    # Set column width
    dims = {}
    for row in wb_1.rows:
        for cell in row:
            if cell.value:
                dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))
    for col, value in dims.items():
        if value <= 15:
            wb_1.column_dimensions[col].width = 20
        else:
            wb_1.column_dimensions[col].width = value + 7

    wb_1.column_dimensions["A"].width = 30 # A column do not automatically adjust column width (Cause A1)

    try:
        wb.save(fn)
    except:
        print("\nExcel WARNING : Please try closing the excel file and RE-RUN the program.")
    