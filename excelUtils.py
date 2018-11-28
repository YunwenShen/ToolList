# -*- coding: utf-8 -*-
import xlrd


def read_excel(file_name: str, sheet_name: str, rowList: list, colList: list):
    """
    读取指定行列的excel内容
    :param file_name: 文件名称
    :param sheet_name: sheet名称
    :param rowList: 行列表（行数）
    :param colList: 列表书（列数）
    :return:
    """
    wb = xlrd.open_workbook(file_name)
    ws = wb.sheet_by_name(sheet_name)
    mapList = []
    # 获取循环的最大行数
    for row in rowList:
        for col in colList:
            map = dict()
            map["value"] = ws.row_values(row)[col["index"]]
            map["row"] = row
            map["colName"] = col["name"]
            map["col"] = col["index"]
            mapList.append(map)
    return mapList


if __name__ == "__main__":
    pass
