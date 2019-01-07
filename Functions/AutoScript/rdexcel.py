from selenium import webdriver
import xlrd


def readRow(row_num):
    workbook = xlrd.open_workbook(r'C:\ZZBK\backup\test1.xlsx')
    # 获取所有sheet
    print(workbook.sheet_names())
    # [u'sheet1', u'sheet2']
    sheet2_name = workbook.sheet_names()[0]

    # 根据sheet索引或者名称获取sheet内容
    target_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
    # sheet2 = workbook.sheet_by_name('sheet2')

    # 获取整行和整列的值（数组）
    rows = target_sheet.row_values(row_num)  # 获取第四行内容
    # cols = target_sheet.col_values(2)  # 获取第三列内容
    print(rows)
    return rows
    # print(cols)
