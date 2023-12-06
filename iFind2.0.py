"""
使用文档
在calculate_median函数中修改转换价值范围

Author：binxin
Date：2023/11/18 14:44
"""
import numpy as np
import pandas as pd
from iFinDPy import *
import datetime


# 登录函数
def login(username, password):
    thsLogin = THS_iFinDLogin(username, password)
    if thsLogin != 0:
        print('登录失败')
    else:
        print('登录成功')


# 获取数据
def get_data(edate):
    get_str = 'edate=' + edate + ';zqlx=全部'
    data_p00868 = THS_DR('p00868', get_str, 'p00868_f027:Y,p00868_f022:Y', 'format:list')
    return data_p00868


# 保存数据到Excel
def save_to_excel(file_name, str_date, premium):
    if not os.path.exists(file_name):
        data = {"日期": [str_date], "转股溢价率%": [premium]}
        df = pd.DataFrame(data)
    else:
        df = pd.read_excel(file_name)
        new_data = pd.DataFrame({"日期": [str_date], "转股溢价率%": [premium]})
        df = pd.concat([df, new_data], ignore_index=True)

    df.to_excel(file_name, index=False)


# 计算中位数
def calculate_median(data):
    max_value = 101
    min_value = 99
    float_values = []

    data_f022 = data['p00868_f022']
    data_f027 = data['p00868_f027']

    for f027, f022 in zip(data_f027, data_f022):
        if '--' in f027 or '--' in f022:
            continue

        f027_value = float(f027)
        f022_value = float(f022)

        if min_value <= f027_value <= max_value:
            float_values.append(f022_value)

    return np.median(float_values) if float_values else None


# 获取数据 - 单日
def get_today_data():
    today = datetime.date.today()
    edate = today.strftime("%Y%m%d")
    return get_data(edate)


# 获取数据 - 区间
def get_interval_data(start_date, end_date):
    delta = datetime.timedelta(days=1)
    data_list = []

    while start_date <= end_date:
        edate = start_date.strftime("%Y%m%d")
        data = get_data(edate)
        if data.data is not None:
            data_list.append((start_date.strftime("%Y/%m/%d"), data))
        start_date += delta

    return data_list


# 主函数
def main():
    username = "zyzqsx112"
    password = "935b43"
    login(username, password)

    # 获取本日数据
    today_data = get_today_data()
    if today_data.data is not None:
        today_median = calculate_median(today_data.data[0]['table'])
        if today_median is not None:
            save_to_excel("转股溢价率记录(转换价值).xlsx", datetime.date.today().strftime("%Y/%m/%d"), today_median)

    # 获取区间时间内的数据
    # start_date = datetime.date(2023, 11, 1)
    # end_date = datetime.date(2023, 11, 18)
    # interval_data = get_interval_data(start_date, end_date)
    #
    # for date, data in interval_data:
    #     median_value = calculate_median(data.data[0]['table'])
    #     if median_value is not None:
    #         save_to_excel("转股溢价率记录(转换价值).xlsx", date, median_value)


if __name__ == '__main__':
    main()
