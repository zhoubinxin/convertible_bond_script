"""
Author：binxin
Date：2023/11/6 20:40
"""
from types import NoneType

import numpy as np
from iFinDPy import *
from datetime import datetime
import pandas as pd
import time as _time
import json
from threading import Thread, Lock, Semaphore
import requests
import os
import openpyxl
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook

sem = Semaphore(5)  # 此变量用于控制最大并发数
dllock = Lock()  # 此变量用来控制实时行情推送中落数据到本地的锁


# 登录函数
def thslogindemo():
    # 输入用户的帐号和密码
    thsLogin = THS_iFinDLogin("zyzqsx112", "935b43")
    print(thsLogin)
    if thsLogin != 0:
        print('登录失败')
    else:
        print('登录成功')


def save_to_excel(date, premium):
    # 定义文件名
    file_name = "转股溢价率记录.xlsx"

    # 检查文件是否存在
    if not os.path.exists(file_name):
        # 如果文件不存在，创建一个新的DataFrame
        data = {"日期": [date], "转股溢价率%": [premium]}
        df = pd.DataFrame(data)
    else:
        # 如果文件已经存在，读取现有数据
        df = pd.read_excel(file_name)

        # 将新数据插入DataFrame
        new_data = pd.DataFrame({"日期": [date], "转股溢价率%": [premium]})
        df = pd.concat([df, new_data], ignore_index=True)

    # 将数据保存到Excel文件
    df.to_excel(file_name, index=False)

    # print(f"数据已保存到{file_name}")


def getmedian(data):
    float_values = []
    for value in data:
        if value != '--':
            try:
                float_value = float(value)
                float_values.append(float_value)
            except ValueError:
                print(f"数据 '{value}' 无法转为float类型")

    return np.median(float_values)


def getData(edate):
    getstr = 'edate=' + edate + ';zqlx=全部'
    print(getstr)
    # 可转债行情,输入参数:截至日期(edate)、债券类型(zqlx)-iFinD数据接口
    data_p00868 = THS_DR('p00868','edate=20231206;zqlx=全部','jydm:Y,jydm_mc:Y,p00868_f027:Y,p00868_f022:Y','format:list')
    print(type(data_p00868))
    print(data_p00868.data)
    # print(data_p00868.data[0]['table']['p00868_f022'])
    return data_p00868


def main():
    # 登录函数
    thslogindemo()

    # for year in range(2017, 2018):
    #     for month in range(3, 13):
    #         print(f"{year}年{month}月")
    #         for day in range(1, 32):
    #             edate = f"{year:04d}{month:02d}{day:02d}"
    #             date = f"{year:04d}/{month:02d}/{day:02d}"
    #
    #             zgyjl = getData(edate)
    #
    #             if type(zgyjl.data) is not NoneType:
    #                 zgyjl_median = getmedian(zgyjl.data[0]['table']['p00868_f022'])
    #
    #                 save_to_excel(date, zgyjl_median)

    edate = '20170229'
    date = '2021/02/29'
    zgyjl = getData(edate)
    print(type(zgyjl.data))
    if type(zgyjl.data) is not NoneType:
        zgyjl_median = getmedian(zgyjl.data[0]['table']['p00868_f022'])

        save_to_excel(date, zgyjl_median)


if __name__ == '__main__':
    main()
