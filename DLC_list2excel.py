import openpyxl
from openpyxl.utils import get_column_letter

def creat_list(list_info, os_info, data_input, data_all_input):
    ## Creat list and save as Excel
    # fn = 'test_excel.xlsx'
    list_ver = "v" + list_info[2]
    fn_temp = [list_info[1], os_info[0], os_info[1], "x64", "Drv", list_ver]
    fn_temp = "_".join(fn_temp)
    fn = fn_temp + ".xlsx"
    wb = openpyxl.Workbook()
    wb_1 = wb.create_sheet("The lastest release ", 0) # 新增工作表並指定放置位置
    wb_2 = wb.create_sheet("Release note", 0)

    # Define cell color and fill it
    cell_A1_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="FFFF00")
    title_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="4F81BD")
    blank_color_fill = openpyxl.styles.fills.PatternFill(patternType="solid", start_color="DCE6F1")
    # cell_A1_color = openpyxl.styles.colors.Color(rgb='00FFFF00') # another coding style
    # cell_A1_color_fill = openpyxl.styles.fills.PatternFill(patternType='solid', fgColor=cell_A1_color)

    wb_1["A1"].fill = cell_A1_color_fill

    for row in wb_1["A2:W2"]: # this line for fill cell color by column
        for cell in row:
            cell.fill = title_color_fill

    for i in range(0, len(data_input), 2): # odd column
        for row in wb_1["A{}:W{}".format(str(i+3), str(i+3))]: # +3 for cell column number in Driver list
            for cell in row:
                cell.fill = blank_color_fill

    # border
    thin = openpyxl.styles.Side(border_style="thin", color="000000") 
    border = openpyxl.styles.Border(left=thin, right=thin, top=thin, bottom=thin)

    for row in wb_1["A2:W{}".format(str(len(data_input)+2))]:
        for cell in row:
            cell.border = border

    # font define
    title_font = openpyxl.styles.Font(size=12, bold=False, name='Arial Unicode MS', color="FFFFFF")
    content_font = openpyxl.styles.Font(size=10, bold=False, name='Verdana', color="000000")

    # list title at excel cell:"A1"
    cell_A1_title = [str(list_info[1]), "Driver List -", str(os_info[0]), str(os_info[1]), "Version:", str(list_info[2]), "- Update Date:", str(list_info[3])]
    cell_A1_title = " ".join(cell_A1_title)
    wb_1["A1"].value = str(cell_A1_title)
    wb_1["A1"].font = content_font

    # colume_title : Each column title at "The lastest release" (row 2)
    row2_column_title = ["Category", "Description", "Provider/ODM", "Vendor", "List of Support model name", "Driver type", "HSA", "APP ID", "APP Name",
                         "Support side link", "Extension ID", "Support OS", "WHQL", "Check version mechanism", "Hardware ID", "Driver version", "Driver Date",
                         "VersionRegKey", "Silent install command", "Match FW Version", "Need reboot(Y/N)", "Driver package", "Remark"]

    for i in range(len(row2_column_title)):
        wb_1.cell(column=i+1, row=2).value = str(row2_column_title[i])
        wb_1.cell(column=i+1, row=2).font = title_font

    # all list to excel  
    for i in range(0, len(data_all_input)):
        for j in range(0, len(data_all_input[i])):
            wb_1.cell(column=i+1, row=j+3).value = str(data_all_input[i][j])
            wb_1.cell(column=i+1, row=j+3).font = content_font

    # set column width
    dims = {}
    for row in wb_1.rows:
        for cell in row:
            if cell.value:
                dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))
    for col, value in dims.items():
        if value <= 13:
            wb_1.column_dimensions[col].width = 13
        else:
            wb_1.column_dimensions[col].width = value

    wb_1.column_dimensions["A"].width = 35 # A column 不自動調整欄寬(因為A1)

    wb.save(fn)
    