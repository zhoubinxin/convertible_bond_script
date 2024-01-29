# code为交易代码 cv为转股价值 cpr为转股溢价率
# balance为债券余额 issue为债券评级 name为债券名称
# ytm为纯债到期收益率 rfp为涨跌幅

from iFinDPy import *
from WindPy import w
import datetime
import sys
import pandas as pd
import time
import numpy as np
import os
import math
from interval import Interval
import io
from tqdm import tqdm


# 文件相关操作
class FileHandler:
    def __init__(self):
        self.directory_path = os.path.join(os.getcwd(), 'data')
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
        file_path = rf'{self.directory_path}\{json_name}.json'

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                if key in data:
                    return data[key]

        return False

    def save_json_data(self, json_name, data, key):
        json_name = json_name.strftime("%Y%m%d")
        file_path = rf'{self.directory_path}\{json_name}.json'

        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump({key: data}, file, indent=4, ensure_ascii=False)
                # print(f'json数据保存成功：{json_name} {key}')
        else:
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
                existing_data[key] = data
                with open(file_path, 'w') as file:
                    json.dump(existing_data, file, indent=4, ensure_ascii=False)
                    # print(f'json数据更新成功：{json_name} {key}')


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

        total_days = (end_date - start_date).days + 1
        with tqdm(total=total_days, desc="进度", dynamic_ncols=True) as pbar:
            for current_date in range(total_days):
                current_date = start_date + timedelta(days=current_date)
                pbar.set_postfix_str(current_date)
                date_list.append(str(current_date))

                if current_date.weekday() in [5, 6]:
                    median.append(None)
                    continue

                # 交易代码
                code = self.get_code(current_date)
                if code is None:
                    median.append(None)
                    continue
                # 转股溢价率
                cpr = self.get_cpr(code, current_date)

                length = len(code)
                if cpr is None:
                    median.append(None)
                    continue

                cv_condition = [True] * length
                balance_condition = [True] * length
                issue_condition = [True] * length

                if data_consider['consider_cv']:
                    cv = self.get_cv(code, current_date)
                    cv_range = data_consider['cv_range']
                    for i in range(length):
                        if cv[i] is None or not cv[i] in cv_range:
                            cv_condition[i] = False

                if data_consider['consider_balance']:
                    balance = self.get_balance(code, current_date)
                    balance_range = data_consider['balance_range']
                    for i in range(length):
                        if balance[i] is None or not balance[i] in balance_range:
                            balance_condition[i] = False

                if data_consider['consider_issue']:
                    issue = self.get_issue(code, current_date)
                    issue_range = data_consider['issue']
                    for i in range(length):
                        if issue[i] is None or issue[i] != issue_range:
                            issue_condition[i] = False

                cpr_list = []
                for i in range(length):
                    if cpr[i] is not None and cv_condition[i] and balance_condition[i] and issue_condition[i]:
                        # print(code[i], cpr[i], cv[i], balance[i], issue[i])
                        cpr_list.append(cpr[i])
                if len(cpr_list) != 0:
                    median.append(np.median(cpr_list))
                else:
                    median.append(None)

                pbar.update(1)

        data_median = {
            "日期": date_list,
            "转股溢价率%": median
        }
        return data_median

    # 涨跌幅中位数
    def get_rfp_median(self, start_date, end_date, data_consider):
        date_list = []
        median = []

        total_days = (end_date - start_date).days + 1
        with tqdm(total=total_days, desc="进度", dynamic_ncols=True) as pbar:
            for current_date in range(total_days):
                current_date = start_date + timedelta(days=current_date)
                pbar.set_postfix_str(current_date)
                date_list.append(str(current_date))

                if current_date.weekday() in [5, 6]:
                    median.append(None)
                    continue

                # 交易代码
                code = self.get_code(current_date)
                if code is None:
                    median.append(None)
                    continue

                # 涨跌幅
                rfp = self.get_rfp(code, current_date)

                length = len(code)
                if rfp is None:
                    median.append(None)
                    continue

                cv_condition = [True] * length
                balance_condition = [True] * length
                issue_condition = [True] * length
                ytm_condition = [True] * length

                if data_consider['consider_cv']:
                    cv = self.get_cv(code, current_date)
                    cv_range = data_consider['cv_range']
                    for i in range(length):
                        if cv[i] is None or not cv[i] in cv_range:
                            cv_condition[i] = False

                if data_consider['consider_balance']:
                    balance = self.get_balance(code, current_date)
                    balance_range = data_consider['balance_range']
                    for i in range(length):
                        if balance[i] is None or not balance[i] in balance_range:
                            balance_condition[i] = False

                if data_consider['consider_issue']:
                    issue = self.get_issue(code, current_date)
                    issue_range = data_consider['issue']
                    for i in range(length):
                        if issue[i] is None or issue[i] != issue_range:
                            issue_condition[i] = False

                if data_consider['consider_ytm']:
                    ytm = self.get_ytm(code, current_date)
                    ytm_range = data_consider['ytm_range']
                    for i in range(length):
                        if ytm[i] is None or not ytm[i] in ytm_range:
                            ytm_condition[i] = False

                rfp_list = []
                for i in range(length):
                    if rfp[i] is not None and cv_condition[i] and balance_condition[i] and issue_condition[i] and ytm_condition[i]:
                        # print(code[i], cpr[i], cv[i], balance[i], issue[i])
                        rfp_list.append(rfp[i])
                if len(rfp_list) != 0:
                    median.append(np.median(rfp_list))
                else:
                    median.append(None)

                pbar.update(1)

        data_median = {
            "日期": date_list,
            "涨跌幅%": median
        }
        return data_median

    def get_number(self, start_date, end_date, data_consider):
        date_list = []
        data_sum = []
        data_ytm = []

        total_days = (end_date - start_date).days + 1
        with tqdm(total=total_days, desc="进度", dynamic_ncols=True) as pbar:
            for current_date in range(total_days):
                current_date = start_date + timedelta(days=current_date)
                pbar.set_postfix_str(current_date)

                date_list.append(str(current_date))

                if current_date.weekday() in [5, 6]:
                    data_ytm.append(None)
                    data_sum.append(None)
                    continue

                # 交易代码
                code = self.get_code(current_date)
                if code is None:
                    data_sum.append(None)
                    data_ytm.append(None)
                    continue

                length = len(code)
                data_sum.append(length)

                ytm_condition = [True] * length

                ytm = self.get_ytm(code, current_date)

                if data_consider['consider_ytm']:
                    ytm_range = data_consider['ytm_range']
                    for i in range(length):
                        if ytm[i] is None or not ytm[i] in ytm_range:
                            ytm_condition[i] = False

                ytm_sum = 0
                for i in range(length):
                    if ytm_condition[i]:
                        ytm_sum = ytm_sum + 1

                data_ytm.append(ytm_sum)

                pbar.update(1)

        data_number = {
            "日期": date_list,
            f"纯债到期收益率>{data_consider['ytm_range'].lower_bound}%的转债个数": data_ytm,
            "转债总数": data_sum
        }
        return data_number

    def get_code(self, current_date):
        data_code = self.file_handler.get_json_data(current_date, "code")
        if not data_code:
            data_code = self.ths.get_code(current_date)

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

    def get_cv(self, code, current_date):
        data_cv = self.file_handler.get_json_data(current_date, "cv")
        if not data_cv:
            data_cv = self.ths.get_cv(code, current_date)
            if not data_cv:
                data_cv = self.wind.get_cv(code, current_date)

            if data_cv:
                self.file_handler.save_json_data(current_date, data_cv, "cv")

        return data_cv

    def get_balance(self, code, current_code):
        data_balance = self.file_handler.get_json_data(current_code, "balance")

        if not data_balance:
            data_balance = self.ths.get_balance(code, current_code)
            if not data_balance:
                data_balance = self.wind.get_balance(code, current_code)

            if data_balance:
                self.file_handler.save_json_data(current_code, data_balance, "balance")

        return data_balance

    def get_issue(self, code, current_date):
        data_issue = self.file_handler.get_json_data(current_date, "issue")

        if not data_issue:
            data_issue = self.ths.get_issue(code, current_date)
            if not data_issue:
                data_issue = self.wind.get_issue(code, current_date)

            if data_issue:
                self.file_handler.save_json_data(current_date, data_issue, "issue")

        return data_issue

    def get_ytm(self, code, current_date):
        data_ytm = self.file_handler.get_json_data(current_date, "ytm")

        if not data_ytm:
            data_ytm = self.ths.get_ytm(current_date)
            if not data_ytm:
                data_ytm = self.wind.get_ytm(code, current_date)

            if data_ytm:
                self.file_handler.save_json_data(current_date, data_ytm, "ytm")

        return data_ytm

    def get_rfp(self, code, current_date):
        data_rfp = self.file_handler.get_json_data(current_date, "rfp")

        if not data_rfp:
            data_rfp = self.ths.get_rfp(current_date)
            if not data_rfp:
                data_rfp = self.wind.get_rfp(code, current_date)

            if data_rfp:
                self.file_handler.save_json_data(current_date, data_rfp, "rfp")

        return data_rfp

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
        # 获取转股溢价率
        data_cpr = None
        return data_cpr

    def get_cv(self, code, current_date):
        # 获取转股价值
        data_cv = None
        return data_cv

    def get_balance(self, code, current_date):
        # 获取债券余额
        data_balance = None
        return data_balance

    def get_issue(self, code, current_date):
        data_issue = None
        return data_issue

    def get_ytm(self, current_date):
        str_date = current_date.strftime("%Y%m%d")
        query = f'edate={str_date};zqlx=全部'
        # THS_DR('p00868','edate=20240122;zqlx=全部','p00868_f023:Y','format:list')
        data_ytm = THS_DR('p00868', query, 'p00868_f023:Y', 'format:list')
        if data_ytm.errorcode != 0:
            print(f"iFind获取纯债到期收益率失败{data_ytm}")
            return None
        else:
            new_ytm = []
            data_ytm = data_ytm.data[0]['table']['p00868_f023']
            for ytm in data_ytm:
                if ytm == "--":
                    new_ytm.append(None)
                else:
                    new_ytm.append(float(ytm))
            return new_ytm

    def get_rfp(self, current_date):
        str_date = current_date.strftime("%Y%m%d")
        query = f'edate={str_date};zqlx=全部'
        # THS_DR('p00868', 'edate=20240129;zqlx=全部', 'p00868_f005:Y', 'format:list')
        data_rfp = THS_DR('p00868', query, 'p00868_f005:Y', 'format:list')
        if data_rfp.errorcode != 0:
            print(f"iFind获取涨跌幅失败{data_rfp}")
            return None
        else:
            new_rfp = []
            data_rfp = data_rfp.data[0]['table']['p00868_f005']
            for rfp in data_rfp:
                if rfp == "--":
                    new_rfp.append(None)
                else:
                    new_rfp.append(float(rfp))
            return new_rfp


# Wind数据获取
class Wind:
    def login(self):
        original_stdout = sys.stdout

        with io.StringIO() as dummy_file:
            sys.stdout = dummy_file
            # output = dummy_file.getvalue()

            out_data = w.start()

        sys.stdout = original_stdout

        if out_data.ErrorCode != 0:
            print(f'Wind登录失败：{out_data.Data}')
        else:
            print('Wind登录成功')

    def data_processing(self, wind_data):
        result = []
        for data in wind_data:
            # 判断数据是否为Nan
            if data is not None and not math.isnan(data):
                result.append(data)
            else:
                result.append(None)


        return result

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
        str_date = current_date.strftime("%Y%m%d")
        query = f"tradeDate={str_date}"

        data_cpr = w.wss(code, "convpremiumratio", query)

        if data_cpr.ErrorCode != 0:
            print(f'Wind获取转股溢价率失败：{data_cpr}')
            return None
        else:
            return self.data_processing(data_cpr.Data[0])

    def get_cv(self, code, current_date):
        str_date = current_date.strftime("%Y%m%d")
        query = f"tradeDate={str_date}"

        data_cv = w.wss(code, "convvalue", query)

        if data_cv.ErrorCode != 0:
            print(f'Wind获取转股价值失败：{data_cv}')
            return None
        else:
            return self.data_processing(data_cv.Data[0])

    def get_balance(self, code, current_date):
        str_date = current_date.strftime("%Y%m%d")
        query = f"tradeDate={str_date}"

        data_balance = w.wss(code, "outstandingbalance", query)
        if data_balance.ErrorCode != 0:
            print(f'Wind获取债券余额失败：{data_balance}')
            return None
        else:
            return self.data_processing(data_balance.Data[0])

    def get_issue(self, code, current_date):
        str_date = current_date.strftime("%Y%m%d")
        query = f"tradeDate={str_date}"

        data_issue = w.wss(code, "amount", query)

        if data_issue.ErrorCode != 0:
            print(f'Wind获取债券评级失败：{data_issue}')
            return None
        else:
            return data_issue.Data[0]

    def get_ytm(self, code, current_date):
        data_ytm = None
        return data_ytm

    def get_rfp(self, code, curent_date):
        data_rfp = None
        return data_rfp


# 主函数
def main():
    # 同花顺登录信息
    username = ""
    password = ""

    data_consider = {
        # 转股价值
        "consider_cv": False,
        "cv_range": Interval(90, 100, lower_closed=True, upper_closed=True),
        # 债券余额，单位为亿
        "consider_balance": False,
        "balance_range": Interval(3, 30, lower_closed=True, upper_closed=True),
        # 债券评级
        "consider_issue": False,
        "issue": "AA+",
        # 纯债到期收益率
        "consider_ytm": True,
        "ytm_range": Interval(3, float('inf'), lower_closed=False),
    }

    cpr = CPR()
    file_handler = FileHandler()

    cpr.login(username, password)

    # 数据周期
    start_date = datetime.date(2021, 2, 16)
    end_date = datetime.date(2021, 2, 16)

    # 获取中位数
    # excel_name = "转股溢价率中位数"
    # data = cpr.get_median(start_date, end_date, data_consider)
    # excel_name = "涨跌幅中位数"
    # data = cpr.get_rfp_median(start_date, end_date, data_consider)

    # 纯债到期收益率大于x的转债个数/当天所有转债数
    excel_name = "纯债到期收益率个数"
    data = cpr.get_number(start_date, end_date, data_consider)

    # 保存数据
    file_handler.save_to_excel(excel_name, data)


if __name__ == '__main__':
    main()
