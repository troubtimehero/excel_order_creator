# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/8/31 16:50
# software: PyCharm

"""
文件说明：

"""
import xlsxwriter


class MyExcelOrder(object):

    def __init__(self, filename):
        self.head_line = 0
        self.body_line = 0
        # Create an new Excel file and add a worksheet.
        self.workbook = xlsxwriter.Workbook(filename)
        self.worksheet = self.workbook.add_worksheet()

        self.fm_table_title = self.workbook.add_format()
        self.fm_table_title.set_align('center')
        self.fm_table_title.set_align('vcenter')
        self.fm_table_title.set_bold(True)
        self.fm_table_title.set_border()
        self.fm_table_title.set_font('宋体')
        self.fm_table_title.set_font_size(10)

        self.fm_table_cell = self.workbook.add_format()
        self.fm_table_cell.set_align('center')
        self.fm_table_cell.set_align('vcenter')
        self.fm_table_cell.set_border()
        self.fm_table_cell.set_font('宋体')
        self.fm_table_cell.set_font_size(10)

        pass

    def new_sheet(self):
        self.worksheet = self.workbook.add_worksheet()

    # def write_head(self) -> int:
    #     return self.head_line
    #
    # def write_foot(self):
    #     pass
    #
    # def write(self, *args, **kwargs):
    #     start_row = self.write_head()

        pass

    def close(self):
        self.workbook.close()

