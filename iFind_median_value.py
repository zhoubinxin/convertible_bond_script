"""
Author：binxin
Date：2023/11/7 11:57
"""
import numpy as np
import pandas as pd
from iFinDPy import *
import datetime

# 登录函数
def login():
    # 输入用户的账号和密码
    thsLogin = THS_iFinDLogin("zyzqsx112", "935b43")
    # print(thsLogin)
    if thsLogin != 0:
        print('登录失败')
    else:
        print('登录成功')


def save_to_excel(str_date, premium):
    # 定义文件名
    file_name = "转股溢价率记录(转换价值).xlsx"

    # 检查文件是否存在
    if not os.path.exists(file_name):
        # 如果文件不存在，创建一个新的DataFrame
        data = {"日期": [str_date], "转股溢价率%": [premium]}
        df = pd.DataFrame(data)
    else:
        # 如果文件已经存在，读取现有数据
        df = pd.read_excel(file_name)

        # 将新数据插入DataFrame
        new_data = pd.DataFrame({"日期": [str_date], "转股溢价率%": [premium]})
        df = pd.concat([df, new_data], ignore_index=True)

    # 将数据保存到Excel文件
    df.to_excel(file_name, index=False)

    # print(f"数据已保存到{file_name}")


def getMedian(data):
    max = 101
    min = 99
    float_values = []

    data_f022 = data['p00868_f022']
    data_f027 = data['p00868_f027']
    for f027, f022 in zip(data_f027, data_f022):
        if '--' in f027 or '--' in f022:
            continue

        f027_value = float(f027)
        f022_value = float(f022)

        if min <= f027_value <= max:
            float_values.append(f022_value)

    if len(float_values) == 0:
        return None
    else:
        return np.median(float_values)


def getData(edate):
    getstr = 'edate=' + edate + ';zqlx=全部'
    # 可转债行情,输入参数:截至日期(edate)、债券类型(zqlx)-iFinD数据接口
    data_p00868 = THS_DR('p00868', getstr, 'p00868_f027:Y,p00868_f022:Y', 'format:list')
    # print(data_p00868.data[0]['table']['p00868_f022'])
    # print(data_p00868)
    return data_p00868


def main():
    # 登录函数
    login()

    # for year in range(2018, 2019):
    #     for month in range(2, 3):
    #         print(f"{year}年{month}月")
    #         for day in range(27, 32):
    #             edate = f"{year:04d}{month:02d}{day:02d}"
    #             str_date = f"{year:04d}/{month:02d}/{day:02d}"
    #
    #             zgyjl = getData(edate)
    #
    #             if zgyjl.data is not None:
    #                 zgyjl_median = getMedian(zgyjl.data[0]['table'])
    #
    #                 if zgyjl_median is None:
    #                     save_to_excel(str_date, '')
    #                 else:
    #                     save_to_excel(str_date, zgyjl_median)

    # 获取当前日期
    today = datetime.date.today()
    edate = today.strftime("%Y%m%d")
    str_date = today.strftime("%Y/%m/%d")

    # edate = '20231106'
    # str_date = '2023/11/06'
    zgyjl = getData(edate)
    if zgyjl.data is not None:
        zgyjl_median = getMedian(zgyjl.data[0]['table'])

        if zgyjl_median is None:
            save_to_excel(str_date, '')
        else:
            save_to_excel(str_date, zgyjl_median)


if __name__ == '__main__':
    main()
