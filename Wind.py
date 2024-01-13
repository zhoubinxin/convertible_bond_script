import os
import numpy as np
import pandas as pd
from WindPy import w
import datetime
import time
import json
import math


class FileHandler:
    def __init__(self):
        self.directory_path = 'data'
        # 判断目录是否存在，如果不存在则创建
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)
            print(f'创建文件夹 {self.directory_path}')

    def save_to_json(self, ths_date, data):
        json_file_path = f'data/{ths_date}.json'
        # 将数据列表保存为JSON文件
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

        print(f'数据已保存到 {json_file_path}')

    def save_to_excel(self, file_name, str_date, premium):
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


class Wind:
    def get_data_basics(self, start_date, end_date):
        file_handler = FileHandler()
        data_list = []
        print("基本数据获取")

        for current_date in range((end_date - start_date).days + 1):
            current_date = start_date + datetime.timedelta(days=current_date)

            if current_date.weekday() in [5, 6]:
                data_list.append((current_date.strftime("%Y-%m-%d"), None))
                continue

            edate = current_date.strftime("%Y%m%d")
            json_file_path = f'data/{edate}.json'

            if os.path.exists(json_file_path):
                # 指定JSON文件路径
                print(f'{current_date} 文件读取')
                # 从JSON文件读取数据
                with open(json_file_path, 'r') as json_file:
                    data = json.load(json_file)

                data_list.append((current_date.strftime("%Y-%m-%d"), data))
            else:
                print(f'{current_date} 接口获取')

                # 获取交易代码
                get_str = f"date={edate};sectorid=a101020600000000"
                data_bond = w.wset("sectorconstituent", get_str)  # date,wind_code,sec_name
                if data_bond.ErrorCode != 0:
                    print(data_bond.ErrorCode)
                wind_code = data_bond.Data[1]
                # sec_name = data_bond.Data[2]

                # 获取转股溢价率
                edate = start_date.strftime("%Y%m%d")
                get_str = f"tradeDate={edate}"
                # convpremiumratio,convvalue 转股溢价率，转换价值
                wind_data = w.wss(wind_code, "convpremiumratio,convvalue", get_str)
                if wind_data.ErrorCode != 0:
                    print(wind_data.ErrorCode)
                    data_list.append((current_date.strftime("%Y-%m-%d"), None))
                else:
                    # 将数据转换为字符串，处理NaN
                    p00868_f022 = [str(value) if not math.isnan(value) else '--' for value in
                                   wind_data.Data[0]]
                    p00868_f027 = [str(value) if not math.isnan(value) else '--' for value in wind_data.Data[1]]

                    data = {"table": {"jydm": wind_code, "p00868_f027": p00868_f027, "p00868_f022": p00868_f022}}
                    file_handler.save_to_json(edate, [data])
                    data_list.append((current_date.strftime("%Y-%m-%d"), [data]))

        return data_list


class CPR:
    def calculate_median(self, data, name, date):
        # 转股价值
        consider_value = True
        max_value = 120
        min_value = 100

        # 债券余额范围
        consider_balance = False
        max_balance = 100
        min_balance = 5

        # 债券评级
        consider_issue = False
        issue = "AA+"

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

            value_condition = (not consider_value) or (min_value < value <= max_value)
            # balance_condition = (not consider_balance) or (min_balance < data_balance)
            # issue_condition = (not consider_issue) or (data_issue == issue)

            if value_condition:
                values.append(premiumratio)

        return np.median(values) if values else ""


# 主函数
def main():
    wind = Wind()
    file_handler = FileHandler()
    cpr = CPR()
    w.start()

    start_date = datetime.date(2024, 1, 10)
    end_date = datetime.date(2024, 1, 10)
    data_basics = wind.get_data_basics(start_date, end_date)

    # interval_data = get_interval_data(start_date, end_date)

    # for date, name, data in interval_data:
    #     median_value = calculate_median(data, name, date)
    #     # print(median_value)
    #     if median_value is not None:
    #         save_to_excel("转股溢价率记录（Wind）.xlsx", date, median_value)


if __name__ == '__main__':
    main()
