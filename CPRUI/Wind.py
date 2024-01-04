import os

import numpy as np
import pandas as pd
from WindPy import w
import datetime
import time


def get_data(start_date):
    # 获取股票代码
    edate = start_date.strftime("%Y-%m-%d")
    get_str = f"date={edate};sectorid=a101020600000000"
    data_bond = w.wset("sectorconstituent", get_str)  # date,wind_code,sec_name
    if data_bond.ErrorCode != 0:
        print(data_bond.ErrorCode)
    wind_code = data_bond.Data[1]
    sec_name = data_bond.Data[2]

    # 获取转股溢价率
    edate = start_date.strftime("%Y%m%d")
    get_str = f"tradeDate={edate}"
    wind_data = w.wss(wind_code, "convpremiumratio,convvalue", get_str)  # convpremiumratio,convvalue 转股溢价率，转换价值
    if wind_data.ErrorCode != 0:
        print(wind_data.ErrorCode)

    return sec_name, wind_data.Data


def get_interval_data(start_date, end_date):
    delta = datetime.timedelta(days=1)
    data_list = []

    while start_date <= end_date:
        print(start_date)
        name, data = get_data(start_date)
        if data is not None:
            data_list.append((start_date.strftime("%Y-%m-%d"), name, data))
        start_date += delta

    return data_list


def calculate_median(data, name, date, userdata):
    max_value = float(userdata['max_value']) if userdata['max_value'] else float('inf')
    min_value = float(userdata['min_value']) if userdata['min_value'] else 0.0
    max_balance = float(userdata['max_balance']) if userdata['max_balance'] else float('inf')
    min_balance = float(userdata['min_balance']) if userdata['min_balance'] else 0.0

    values = []
    convpremiumratio = data[0]
    convvalue = data[1]

    for premiumratio, value in zip(convpremiumratio, convvalue):
        if premiumratio is None or value is None:
            continue

        if np.isnan(premiumratio) or np.isnan(value):
            continue

        # data_balance = None
        # data_issue = None
        # if consider_balance or consider_issue:
        #     data_balance, data_issue = get_bond(jydm, date)

        value_condition = (not userdata['consider_value']) or (
                min_value < value <= max_value)
        # balance_condition = (not userdata['consider_balance']) or (min_balance < data_balance)
        # issue_condition = (not userdata['consider_issue']) or (data_issue == userdata['issue'])

        if value_condition:
            values.append(premiumratio)

    return np.median(values) if values else ""


def save_to_excel(file_name, str_date, premium):
    print(f'数据保存中{str_date}')
    while True:
        try:
            if not os.path.exists(file_name):
                data = {"日期": [str_date], "转股溢价率%": [premium]}
                df = pd.DataFrame(data)
            else:
                df = pd.read_excel(file_name)
                new_data = pd.DataFrame({"日期": [str_date], "转股溢价率%": [premium]})
                df = pd.concat([df, new_data], ignore_index=True)

            df.to_excel(file_name, index=False)
            break  # 如果成功写入，跳出循环
        except PermissionError:
            print(f"请关闭文件 '{file_name}'")
            time.sleep(5)


# 主函数
def main():
    w.start()

    start_date = datetime.date(2023, 5, 1)
    end_date = datetime.date(2023, 5, 30)
    interval_data = get_interval_data(start_date, end_date)

    for date, name, data in interval_data:
        median_value = calculate_median(data, name, date)
        # print(median_value)
        if median_value is not None:
            save_to_excel("转股溢价率记录（Wind）.xlsx", date, median_value)


if __name__ == '__main__':
    main()
