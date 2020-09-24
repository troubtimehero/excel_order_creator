# author:阿豪
# contact: cyhol@qq.com
# datetime:2020/8/31 17:14
# software: PyCharm

"""
文件说明：

"""
import os
from contextlib import contextmanager

from app.goods_manager import goods_mgr
from image.resize import get_scale_to_tar_size
from writer.excel_writer import MyExcelOrder
from app.settings import get_cfg_sell, get_cfg_prod
from writer.to_rmb import Cnumber


class ZRYOrder(MyExcelOrder):
    _title_info_sell = ['序号', '类型', '图片', '商品名称', '单位', '单价', '优惠价', '数量', '金额', '备注']
    _head_fill_sell = [("sf_company", 1), ("sf_order_no", 3), ("sf_tel", 5), ("sf_customer", 7), ("sf_address", 9)]

    _title_info_prod = ['序号', '类型', '图片', '商品名称', '单位', '数量', '备注']
    _head_fill_prod = [("sf_customer", 1), ("sf_order_no", 3)]

    def _write_head_sell(self, head: dict):
        # 跳过第一行
        cur_row = 1

        fm_bold = self.workbook.add_format({'bold': True})
        fm_bold.set_font_size(get_cfg_sell(["标题", "字体大小"]))
        fm_bold.set_align('center')
        fm_bold.set_align('vcenter')
        self.worksheet.set_row(cur_row, get_cfg_sell(["标题", "行高"]))
        self.worksheet.merge_range(cur_row, 0, cur_row, len(get_cfg_sell(["商品", "各列宽度"])) - 1, get_cfg_sell(["标题", "文字"]), fm_bold)

        cur_row += 1
        fm_center = self.workbook.add_format()
        # fm_center.set_align('left')
        fm_center.set_align('vcenter')

        rec_info = get_cfg_sell(["收货信息"])[:]
        for sf in self._head_fill_sell:
            rec_info[sf[1]]["文字"] = head.get(sf[0], "")

        row_count = 0
        for info in rec_info:
            pos, merge = info["位置"], info["合并"]
            row_count = max(row_count, pos[0])
            pos = pos[0]-1, pos[1]-1
            if merge[0] == 0 and merge[1] == 0:
                self.worksheet.write(cur_row + pos[0], pos[1], info["文字"], fm_center)
            else:
                self.worksheet.merge_range(cur_row+pos[0], pos[1], cur_row+pos[0]+merge[0], pos[1]+merge[1], info["文字"], fm_center)
            self.worksheet.set_row(cur_row + pos[0], get_cfg_sell(["收货信息行高"]))

        self.head_line = cur_row + row_count

    def _write_foot_sell(self, foot: dict):
        # Write some numbers, with row/column notation.
        cur_row = self.head_line + self.body_line
        fm_bold = self.workbook.add_format({'bold': True, 'text_wrap': 1, 'align': 'vcenter'})
        for line in get_cfg_sell(["表尾"]):
            self.worksheet.merge_range(cur_row, 0, cur_row, 9, '\n'.join(line), fm_bold)
            self.worksheet.set_row(cur_row, 50)
            cur_row += 1

    def _write_body_sell(self, body: dict):
        cur_row = self.head_line
        self.worksheet.set_row(cur_row, get_cfg_sell(["商品", "表头高"]))

        for i, ti in enumerate(self._title_info_sell):
            self.worksheet.set_column(i, i, width=get_cfg_sell(["商品", "各列宽度", self._title_info_sell[i]]))
            self.worksheet.write(cur_row, i, self._title_info_sell[i], self.fm_table_title)

        line_height = get_cfg_sell(["商品", "行高"])

        image_cell_width = int(get_cfg_sell(["商品", "各列宽度", "图片"])) * 7.5
        cur_row += 1
        total_price = 0
        good_type = None, cur_row
        for index, gi in enumerate(goods_mgr.get_info_list()):
            count = body.get(str(index))
            if count:
                # 同类型名称，合并单元格
                if good_type[0] and good_type[0] != gi.type_:
                    self.worksheet.merge_range(good_type[1], 1, cur_row-1, 1, good_type[0], self.fm_table_cell)
                    good_type = gi.type_, cur_row
                elif not good_type[0]:
                    good_type = gi.type_, good_type[1]

                # gi = GoodInfo   # ###########################################
                self.worksheet.set_row(cur_row, line_height)

                self.worksheet.write(cur_row, 0, cur_row-self.head_line, self.fm_table_cell)
                self.worksheet.write(cur_row, 1, gi.type_, self.fm_table_cell)

                self.worksheet.write(cur_row, 2, '', self.fm_table_cell)
                image_path = os.path.join(os.path.abspath('.'), 'app', 'static', gi.local_path)
                scale, dis_width = get_scale_to_tar_size(image_path, get_cfg_sell(["商品", "图片限宽"]), get_cfg_sell(["商品", "图片限高"]))
                img_opt = {'x_offset': 1+(image_cell_width-dis_width)/2, 'y_offset': 2, 'x_scale': scale, 'y_scale': scale}
                print(img_opt)
                self.worksheet.insert_image(cur_row, 2, image_path, options=img_opt)

                self.worksheet.write(cur_row, 3, gi.name, self.fm_table_cell)
                self.worksheet.write(cur_row, 4, gi.unit, self.fm_table_cell)
                self.worksheet.write(cur_row, 5, float(gi.price), self.fm_table_cell)
                self.worksheet.write(cur_row, 6, float(gi.rate), self.fm_table_cell)
                self.worksheet.write(cur_row, 7, int(count), self.fm_table_cell)
                self.worksheet.write_formula(cur_row, 8, f'=G{cur_row+1}*H{cur_row+1}', self.fm_table_cell)
                self.worksheet.write(cur_row, 9, '', self.fm_table_cell)
                cur_row += 1

                total_price += float(gi.rate) * int(count)

        self.worksheet.merge_range(good_type[1], 1, cur_row-1, 1, good_type[0], self.fm_table_cell)

        self.worksheet.set_row(cur_row, line_height)
        self.worksheet.merge_range(cur_row, 0, cur_row, 1, "合计", self.fm_table_cell)
        self.worksheet.write(cur_row, 2, "大写：", self.fm_table_cell)
        self.worksheet.merge_range(cur_row, 3, cur_row, 5, "", self.fm_table_cell)
        # self.worksheet.write_formula(cur_row, 3, f"=I{cur_row+1}", self.fm_table_cell)
        self.worksheet.write(cur_row, 3, Cnumber().cwchange(total_price) if total_price > 0 else "", self.fm_table_cell)
        self.worksheet.write(cur_row, 6, "", self.fm_table_cell)
        self.worksheet.write(cur_row, 7, "", self.fm_table_cell)
        self.worksheet.write_formula(cur_row, 8, f'SUM(I{self.head_line+2}:I{cur_row})', self.fm_table_cell)
        self.worksheet.write(cur_row, 9, "", self.fm_table_cell)
        cur_row += 1

        self.worksheet.set_row(cur_row, line_height)
        self.worksheet.merge_range(cur_row, 0, cur_row, 1, "备注", self.fm_table_cell)
        self.worksheet.merge_range(cur_row, 2, cur_row, len(self._title_info_sell) - 1, "", self.fm_table_cell)
        cur_row += 1

        self.worksheet.merge_range(cur_row, len(self._title_info_sell) - 3, cur_row, len(self._title_info_sell) - 2, "业务员：")
        self.worksheet.write(cur_row, len(self._title_info_sell) - 1, body.get("sf_salesman", ""))

        self.body_line = cur_row + 1 - self.head_line

    def write_order_sell(self, sheet_name, table: dict):
        self.new_sheet(sheet_name)
        self._write_head_sell(table)
        self._write_body_sell(table)
        self._write_foot_sell(table)

    # ##########################################################

    def _write_head_prod(self, head: dict):
        # 跳过第一行
        cur_row = 1

        fm_bold = self.workbook.add_format({'bold': True})
        fm_bold.set_font_size(get_cfg_prod(["标题", "字体大小"]))
        fm_bold.set_align('center')
        fm_bold.set_align('vcenter')
        self.worksheet.set_row(cur_row, get_cfg_prod(["标题", "行高"]))
        self.worksheet.merge_range(cur_row, 0, cur_row, len(get_cfg_prod(["商品", "各列宽度"])) - 1, get_cfg_prod(["标题", "文字"]), fm_bold)

        cur_row += 1
        fm_center = self.workbook.add_format()
        # fm_center.set_align('left')
        fm_center.set_align('vcenter')

        rec_info = get_cfg_prod(["收货信息"])[:]
        for sf in self._head_fill_prod:
            rec_info[sf[1]]["文字"] = head.get(sf[0], "")

        row_count = 0
        for info in rec_info:
            pos, merge = info["位置"], info["合并"]
            row_count = max(row_count, pos[0])
            pos = pos[0]-1, pos[1]-1
            if merge[0] == 0 and merge[1] == 0:
                self.worksheet.write(cur_row + pos[0], pos[1], info["文字"], fm_center)
            else:
                self.worksheet.merge_range(cur_row+pos[0], pos[1], cur_row+pos[0]+merge[0], pos[1]+merge[1], info["文字"], fm_center)
            self.worksheet.set_row(cur_row + pos[0], get_cfg_prod(["收货信息行高"]))

        self.head_line = cur_row + row_count

    def _write_foot_prod(self, foot: dict):
        # Write some numbers, with row/column notation.
        cur_row = self.head_line + self.body_line
        fm_bold = self.workbook.add_format({'bold': True, 'text_wrap': 1, 'align': 'vcenter'})
        for line in get_cfg_prod(["表尾"]):
            self.worksheet.merge_range(cur_row, 0, cur_row, 9, '\n'.join(line), fm_bold)
            self.worksheet.set_row(cur_row, 50)
            cur_row += 1

    def _write_body_prod(self, body: dict):
        cur_row = self.head_line
        self.worksheet.set_row(cur_row, get_cfg_prod(["商品", "表头高"]))

        for i, ti in enumerate(self._title_info_prod):
            self.worksheet.set_column(i, i, width=get_cfg_prod(["商品", "各列宽度", self._title_info_prod[i]]))
            self.worksheet.write(cur_row, i, self._title_info_prod[i], self.fm_table_title)

        line_height = get_cfg_prod(["商品", "行高"])

        image_cell_width = int(get_cfg_prod(["商品", "各列宽度", "图片"])) * 7.5
        cur_row += 1
        good_type = None, cur_row
        for index, gi in enumerate(goods_mgr.get_info_list()):
            count = body.get(str(index))
            if count:
                # 同类型名称，合并单元格
                if good_type[0] and good_type[0] != gi.type_:
                    self.worksheet.merge_range(good_type[1], 1, cur_row-1, 1, good_type[0], self.fm_table_cell)
                    good_type = gi.type_, cur_row
                elif not good_type[0]:
                    good_type = gi.type_, good_type[1]

                # gi = GoodInfo   # ###########################################
                self.worksheet.set_row(cur_row, line_height)

                self.worksheet.write(cur_row, 0, cur_row-self.head_line, self.fm_table_cell)
                self.worksheet.write(cur_row, 1, gi.type_, self.fm_table_cell)

                self.worksheet.write(cur_row, 2, '', self.fm_table_cell)
                image_path = os.path.join(os.path.abspath('.'), 'app', 'static', gi.local_path)
                scale, dis_width = get_scale_to_tar_size(image_path, get_cfg_prod(["商品", "图片限宽"]), get_cfg_prod(["商品", "图片限高"]))
                img_opt = {'x_offset': 1+(image_cell_width-dis_width)/2, 'y_offset': 2, 'x_scale': scale, 'y_scale': scale}
                self.worksheet.insert_image(cur_row, 2, image_path, options=img_opt)

                # print(f'cn:{gi.name}, en:{gi.name_en}')
                self.worksheet.write(cur_row, 3, gi.name if gi.name_en == "" else f'{gi.name}\n{gi.name_en}', self.fm_table_cell)
                self.worksheet.write(cur_row, 4, gi.unit, self.fm_table_cell)
                self.worksheet.write(cur_row, 5, int(count), self.fm_table_cell)
                self.worksheet.write(cur_row, 6, '', self.fm_table_cell)
                cur_row += 1

        self.worksheet.merge_range(good_type[1], 1, cur_row-1, 1, good_type[0], self.fm_table_cell)

        # self.worksheet.set_row(cur_row, line_height)
        # self.worksheet.merge_range(cur_row, 0, cur_row, 1, "合计", self.fm_table_cell)
        # self.worksheet.write(cur_row, 2, "大写：", self.fm_table_cell)
        # self.worksheet.merge_range(cur_row, 3, cur_row, 5, "", self.fm_table_cell)
        # self.worksheet.write(cur_row, 6, "", self.fm_table_cell)
        # self.worksheet.write(cur_row, 7, "", self.fm_table_cell)
        # self.worksheet.write_formula(cur_row, 8, f'=SUM(I{self.head_line+2}:I{cur_row})', self.fm_table_cell)
        # self.worksheet.write(cur_row, 9, "", self.fm_table_cell)
        # cur_row += 1

        self.worksheet.set_row(cur_row, line_height)
        self.worksheet.merge_range(cur_row, 0, cur_row, 1, "备注", self.fm_table_cell)
        self.worksheet.merge_range(cur_row, 2, cur_row, len(self._title_info_prod) - 1, "", self.fm_table_cell)
        cur_row += 1

        self.worksheet.merge_range(cur_row, len(self._title_info_prod) - 3, cur_row, len(self._title_info_prod) - 2, "业务员：")
        self.worksheet.write(cur_row, len(self._title_info_prod) - 1, body.get("sf_salesman", ""))

        self.body_line = cur_row + 1 - self.head_line

    def write_order_prod(self, sheet_name, table: dict):
        self.new_sheet(sheet_name)
        self._write_head_prod(table)
        self._write_body_prod(table)
        self._write_foot_prod(table)

    # ######################

    # @contextmanager
    # def __call__(self, *args, **kwargs):
    #     print("__call__")
    #     yield
    #     print("close")
    #     self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
