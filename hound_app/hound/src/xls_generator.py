import xlwt
from xlwt import XFStyle
from xlwt import Font

class XlsGenerator:
    def create_headers(columns, workbook, row_num):
        font_style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        font_style.font = font
        for col_num in range(len(columns)):
            workbook.write(row_num, col_num, columns[col_num], font_style)
        row_num += 1
        return row_num

    def create_content(workbook, row_num, row, format):
        for col_num in range(len(row)):
            workbook.write(row_num, col_num, str(row[col_num]), format)
        row_num += 1
        return row_num
