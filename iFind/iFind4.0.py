import numpy as np
import pandas as pd
from iFinDPy import *
import datetime
import time
import json


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
    # jydm交易代码 f027转换价值 f022转股溢价率
    data_p00868 = THS_DR('p00868', get_str, 'jydm:Y,p00868_f027:Y,p00868_f022:Y', 'format:list')
    # print(data_p00868)
    if data_p00868.data is None:
        print(data_p00868.errmsg)

    return data_p00868


# 获取债券余额数据和债券评级
def get_bond(jydm, date):
    print(f'{date} 债券余额数据和债券评级')
    # ths_bond_balance_cbond债券余额数据 ths_issue_credit_rating_cbond债券评级
    data = THS_DS(jydm, 'ths_bond_balance_cbond;ths_issue_credit_rating_cbond', ';', '', date, date, 'format:list')

    if data.data is None:
        print(data.errmsg)
        return None, None

    data_balances = [item['table']['ths_bond_balance_cbond'][0] for item in data.data]
    data_issues = [item['table']['ths_issue_credit_rating_cbond'][0] for item in data.data]

    return data_balances, data_issues


# 保存数据到Excel
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


# 计算中位数
def calculate_median(data, date):
    # 转换价值
    consider_value = False
    max_value = 120
    min_value = 100

    # 债券余额范围
    consider_balance = True
    max_balance = 300000000
    min_balance = 5

    # 债券评级
    consider_issue = False
    issue = "AA+"

    float_values = []

    data_jydm = data['jydm']
    data_f022 = data['p00868_f022']
    data_f027 = data['p00868_f027']

    if consider_balance or consider_issue:
        data_balances, data_issues = get_bond(data_jydm, date)

    for i in range(len(data_jydm)):
        f027 = data_f027[i]
        f022 = data_f022[i]
        if '--' in f027 or '--' in f022:
            continue

        if consider_balance or consider_issue:
            data_balance = data_balances[i]
            data_issue = data_issues[i]
            if data_balance is None:
                continue

        f027_value = float(f027)
        f022_value = float(f022)

        value_condition = (not consider_value) or (min_value < f027_value <= max_value)
        balance_condition = (not consider_balance) or (data_balance < max_balance)
        issue_condition = (not consider_issue) or (data_issue == issue)

        if value_condition and balance_condition and issue_condition:
            float_values.append(f022_value)

    return np.median(float_values) if float_values else ""


def file_exist(date):
    # 文件夹路径
    directory_path = 'data'

    # 文件名
    file_to_check = f'{date}.json'

    # 完整的文件路径
    file_path = os.path.join(directory_path, file_to_check)

    # 判断目录是否存在，如果不存在则创建
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f'创建了 {directory_path} 目录。')

    # 判断文件是否存在
    if os.path.exists(file_path):
        return True
    else:
        return False


def save_to_json(date, data):
    json_file_path = f'data/{date}.json'
    # 将数据列表保存为JSON文件
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

    print(f'数据已保存到 {json_file_path}')


# 获取数据
def get_interval_data(start_date, end_date):
    delta = datetime.timedelta(days=1)
    data_list = []

    while start_date <= end_date:
        print(start_date)
        edate = start_date.strftime("%Y%m%d")
        if file_exist(edate):
            # 指定JSON文件路径
            json_file_path = f'data/{edate}.json'
            print(f'从文件{json_file_path}中读取数据')
            # 从JSON文件读取数据
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            data_list.append((start_date.strftime("%Y-%m-%d"), data))
        else:
            data = get_data(edate)
            if data.data is not None:
                save_to_json(edate, data.data)
                data_list.append((start_date.strftime("%Y-%m-%d"), data.data))
        start_date += delta

    return data_list


# 主函数
def main():
    username = ""
    password = ""
    login(username, password)

    start_date = datetime.date(2018, 9, 10)
    end_date = datetime.date(2018, 9, 10)
    interval_data = get_interval_data(start_date, end_date)

    for date, data in interval_data:
        median_value = calculate_median(data[0]['table'], date)
        # print(median_value)
        if median_value is not None:
            save_to_excel("转股溢价率记录.xlsx", date, median_value)


if __name__ == '__main__':
    main()
