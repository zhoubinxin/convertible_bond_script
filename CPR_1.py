# code为交易代码 cv为转股价值 cpr为转股溢价率 balance为债券余额 issue为债券评级 name为债券名称

from iFinDPy import *
from WindPy import w
import datetime
import sys
import pandas as pd
import time
import numpy as np
import os
import math


# 文件相关操作
class FileHandler:
    def __init__(self):
        self.directory_path = 'data'
        # 创建data目录，用于存储数据
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)
            print(f'创建文件夹 {self.directory_path}')

    def save_to_excel(self, excel_name, data):
        file_path = os.path.join(os.getcwd(), f'{excel_name}.xlsx')

        max_attempts = 5
        attempt = 1

        while attempt <= max_attempts:
            try:
                # 检查文件是否存在
                if os.path.exists(file_path):
                    # 如果文件存在，读取现有数据
                    df = pd.read_excel(file_path)
                    # 添加新的数据
                    new_data_df = pd.DataFrame(data)
                    df = pd.concat([df, new_data_df], ignore_index=True)

                else:
                    # 如果文件不存在，创建新的DataFrame
                    df = pd.DataFrame(data)

                # 保存DataFrame到Excel
                df.to_excel(file_path, index=False)
                print('数据保存成功')
                break


            except Exception as e:
                print(f"无法写入文件 '{excel_name}'.xlsx，请确保没有其他程序正在使用该文件。错误详情：{e}")

                if attempt < max_attempts:
                    print(f"尝试重新写入，剩余尝试次数: {max_attempts - attempt}")
                    attempt += 1
                    time.sleep(5)
                else:
                    print("写入文件失败")
                    print(data)
                    break

    def get_json_data(self, json_name, key):
        json_name = json_name.strftime("%Y%m%d")
        file_path = os.path.join(os.getcwd(), f'{self.directory_path}/{json_name}.json')

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                if key in data:
                    return data[key]

        return False

    def save_json_data(self, json_name, data, key):
        json_name = json_name.strftime("%Y%m%d")
        file_path = os.path.join(os.getcwd(), f'{self.directory_path}/{json_name}.json')

        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump({key: data}, file, indent=4, ensure_ascii=False)
                print(f'json数据保存成功：{json_name} {key}')
        else:
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
                existing_data[key] = data
                with open(file_path, 'w') as file:
                    json.dump(existing_data, file, indent=4, ensure_ascii=False)
                    print(f'json数据更新成功：{json_name} {key}')


class CPR:
    def __init__(self):
        self.ths = Ths()
        self.wind = Wind()
        self.file_handler = FileHandler()

    # 登录
    def login(self, username, password):
        # 登录同花顺
        self.ths.login(username, password)
        # 登录Wind
        self.wind.login()

    # 转股溢价率中位数
    def get_median(self, start_date, end_date, data_consider):
        date_list = []
        median = []

        for current_date in range((end_date - start_date).days + 1):
            current_date = start_date + timedelta(days=current_date)

            date_list.append(str(current_date))

            if current_date.weekday() in [5, 6]:
                median.append(None)
                continue
            # 交易代码
            code = self.get_code(current_date)
            cpr = self.get_cpr(code, current_date)

            if cpr is None:
                median.append(None)
                continue

            cpr_list = []
            for i in range(len(code)):
                if cpr[i] is not None:
                    cpr_list.append(cpr[i])
            if len(cpr_list) != 0:
                median.append(np.median(cpr_list))
            else:
                median.append(None)

        data_median = {
            "日期": date_list,
            "转股溢价率%": median
        }
        return data_median

    def get_code(self, current_date):
        data_code = self.file_handler.get_json_data(current_date, "code")
        if not data_code:
            data_code = self.ths.get_code(current_date)
            if not data_code:
                data_code = self.wind.get_code(current_date)

                if data_code:
                    self.file_handler.save_json_data(current_date, data_code, "code")

        return data_code

    def get_cpr(self, code, current_date):
        data_cpr = self.file_handler.get_json_data(current_date, "cpr")
        if not data_cpr:
            data_cpr = self.ths.get_cpr(code, current_date)
            if not data_cpr:
                data_cpr = self.wind.get_cpr(code, current_date)

                if data_cpr:
                    self.file_handler.save_json_data(current_date, data_cpr, "cpr")
        return data_cpr


# 同花顺数据获取
class Ths:
    # 登录函数
    def login(self, username, password):
        thsLogin = THS_iFinDLogin(username, password)
        if thsLogin != 0:
            print('同花顺登录失败')
        else:
            print('同花顺登录成功')

    def get_code(self, current_date):
        # 获取交易代码
        data_code = None
        return data_code

    def get_cpr(self, code, current_date):
        # 获取CPR数据
        data_cpr = None
        return data_cpr


# Wind数据获取
class Wind:
    def login(self):
        original_stdout = sys.stdout

        with open('dummy_file.txt', 'w') as dummy_file:
            sys.stdout = dummy_file

            out_data = w.start()

        sys.stdout = original_stdout

        if out_data.ErrorCode != 0:
            print(f'Wind登录失败：{out_data.Data}')
        else:
            print('Wind登录成功')

    def get_code(self, current_date):
        file_handler = FileHandler()
        query = f"date={current_date};sectorid=a101020600000000"
        data_code = w.wset("sectorconstituent", query)

        if data_code.ErrorCode != 0:
            print(f'Wind获取交易代码失败：{data_code.Data}')
            return None
        else:
            file_handler.save_json_data(current_date, data_code.Data[2], "name")
            return data_code.Data[1]

    def get_cpr(self, code, current_date):
        file_handler = FileHandler()
        str_date = current_date.strftime("%Y%m%d")
        query = f"tradeDate={str_date}"

        data_cpr = w.wss(code, "convpremiumratio", query)

        if data_cpr.ErrorCode != 0:
            print(f'Wind获取CPR失败：{data_cpr.Data}')
            return None
        else:
            new_cpr = []
            for cpr in data_cpr.Data[0]:
                # 判断cpr是否为Nan
                if not math.isnan(cpr):
                    new_cpr.append(cpr)
                else:
                    new_cpr.append(None)
            return new_cpr


# 主函数
def main():
    # 同花顺登录信息
    username = ""
    password = ""

    data_consider = {
        # 转股价值
        "consider_value": False,
        "max_value": 120,
        "min_value": 100,
        # 债券余额，单位为亿
        "consider_balance": False,
        "max_balance": 10,
        "min_balance": 3,
        # 债券评级
        "consider_issue": False,
        "issue": "AA+"
    }

    cpr = CPR()
    file_handler = FileHandler()

    cpr.login(username, password)

    # 数据周期
    start_date = datetime.date(2024, 1, 17)
    end_date = datetime.date(2024, 1, 17)

    # 获取中位数
    excel_name = "转股溢价率中位数"
    data_median = cpr.get_median(start_date, end_date, data_consider)

    # 保存数据
    file_handler.save_to_excel(excel_name, data_median)


if __name__ == '__main__':
    main()
