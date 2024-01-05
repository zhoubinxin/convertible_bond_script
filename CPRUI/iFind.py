import numpy as np
import pandas as pd
from iFinDPy import *
import datetime
import time


# 登录函数
def login(username, password):
    thsLogin = THS_iFinDLogin(username, password)
    return thsLogin


# 获取数据
def get_data(edate):
    get_str = 'edate=' + edate + ';zqlx=全部'
    # jydm交易代码 f027转换价值 f022转股溢价率
    data_p00868 = THS_DR('p00868', get_str, 'jydm:Y,p00868_f027:Y,p00868_f022:Y', 'format:list')
    if data_p00868.data is None:
        print(data_p00868.errmsg)

    return data_p00868


# 获取债券余额数据和债券评级
def get_bond(jydm, date):
    print(date+jydm)
    # ths_bond_balance_cbond债券余额数据 ths_issue_credit_rating_cbond债券评级
    data = THS_DS(jydm, 'ths_bond_balance_cbond;ths_issue_credit_rating_cbond', ';', '', date, date, 'format:list')

    if data.data is None:
        print(data.errmsg)
        return None, None

    return data.data[0]['table']['ths_bond_balance_cbond'], data.data[0]['table']['ths_issue_credit_rating_cbond']


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
def calculate_median(data, date, userdata):
    max_value = float(userdata['max_value']) if userdata['max_value'] else float('inf')
    min_value = float(userdata['min_value']) if userdata['min_value'] else 0.0
    max_balance = float(userdata['max_balance']) if userdata['max_balance'] else float('inf')
    min_balance = float(userdata['min_balance']) if userdata['min_balance'] else 0.0

    print(max_value)
    print(min_value)
    print(userdata['consider_value'])
    float_values = []

    data_jydm = data['jydm']
    data_f022 = data['p00868_f022']
    data_f027 = data['p00868_f027']

    for jydm, f027, f022 in zip(data_jydm, data_f027, data_f022):
        if '--' in f027 or '--' in f022:
            continue

        data_balance = None
        data_issue = None
        if userdata['consider_balance'] or userdata['consider_issue']:
            data_balance, data_issue = get_bond(jydm, date)
            if data_balance is None:
                continue
            if len(data_balance) == 0:
                continue
            else:
                data_balance = data_balance[0]

            data_issue = data_issue[0]

        f027_value = float(f027)
        f022_value = float(f022)

        value_condition = (not userdata['consider_value']) or (
                    min_value < f027_value <= max_value)
        balance_condition = (not userdata['consider_balance']) or (min_balance < data_balance)
        issue_condition = (not userdata['consider_issue']) or (data_issue == userdata['issue'])

        if value_condition and balance_condition and issue_condition:
            float_values.append(f022_value)

    return np.median(float_values) if float_values else ""


# 获取数据
def get_interval_data(start_date, end_date):
    delta = datetime.timedelta(days=1)
    data_list = []

    while start_date <= end_date:
        print(start_date)
        edate = start_date.strftime("%Y%m%d")
        data = get_data(edate)
        if data.data is not None:
            data_list.append((start_date.strftime("%Y-%m-%d"), data))
        start_date += delta

    return data_list
