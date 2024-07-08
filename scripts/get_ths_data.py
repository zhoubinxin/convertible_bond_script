import csv
import json
from datetime import datetime, timedelta
from time import sleep

import requests
from chinese_calendar import is_workday
from environs import Env
from sqlalchemy import create_engine, inspect


class THS:
    def __init__(self, trade_day):
        self.trade_day = trade_day
        self.access_token = self.get_access_token()

    def get_data(self):
        url = "https://quantapi.51ifind.com/api/v1/data_pool"
        headers = {"Content-Type": "application/json", "access_token": self.access_token}

        formData = {"reportname": "p00868", "functionpara": {"edate": self.trade_day, "zqlx": "全部"},
                    "outputpara": "jydm,jydm_mc,p00868_f002,p00868_f016,p00868_f007,p00868_f006,p00868_f001,"
                                  "p00868_f028,p00868_f011,p00868_f005,p00868_f014,p00868_f008,p00868_f003,"
                                  "p00868_f026,p00868_f023,p00868_f004,p00868_f012,p00868_f017,p00868_f024,"
                                  "p00868_f019,p00868_f027,p00868_f018,p00868_f022,p00868_f021,p00868_f015,"
                                  "p00868_f010,p00868_f025,p00868_f009,p00868_f029,p00868_f013,p00868_f020,p00868_f030"}

        response = requests.post(url, headers=headers, data=json.dumps(formData))

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            send_msg(f"可转债: {response.json()}")
            return None

    def get_access_token(self, retries=3, delay=5):
        env = Env()
        env.read_env()
        bx_token = env.str('BX_TOKEN')
        worker_url = "https://api.bxin.top/kv"
        data = {
            "action": "read",
            "token": bx_token,
            "key": "ths_token"
        }

        response = requests.post(worker_url, json=data)

        response = response.json()
        refresh_token = response['data']['value']

        url = 'https://ft.10jqka.com.cn/api/v1/get_access_token'
        headers = {"ContentType": "application/json", "refresh_token": refresh_token}

        attempt = 0
        while attempt < retries:
            try:
                response = requests.post(url=url, headers=headers)
                response = json.loads(response.content)
                if response['errorcode'] != 0:
                    send_msg(f"可转债：{response}")
                    access_token = None
                else:
                    access_token = response['data']['access_token']

                return access_token
            except requests.exceptions.SSLError:
                attempt += 1
                if attempt < retries:
                    sleep(delay)
                else:
                    send_msg("可转债：获取access_token失败，请检查网络")
                    return None


def save_to_csv(data, yesterday):
    desired_data = []
    row = data["tables"][0]["table"]
    jydm = row["jydm"]

    for i in range(len(jydm)):
        row_data = [row["jydm"][i], row["jydm_mc"][i], row["p00868_f002"][i], row["p00868_f016"][i],
                    row["p00868_f007"][i],
                    row["p00868_f006"][i], row["p00868_f001"][i], row["p00868_f028"][i], row["p00868_f011"][i],
                    row["p00868_f005"][i], row["p00868_f014"][i], row["p00868_f008"][i], row["p00868_f003"][i],
                    row["p00868_f026"][i], row["p00868_f023"][i], row["p00868_f004"][i], row["p00868_f012"][i],
                    row["p00868_f017"][i], row["p00868_f024"][i], row["p00868_f019"][i], row["p00868_f027"][i],
                    row["p00868_f018"][i], row["p00868_f022"][i], row["p00868_f021"][i], row["p00868_f015"][i],
                    row["p00868_f010"][i], row["p00868_f025"][i], row["p00868_f009"][i], row["p00868_f029"][i],
                    row["p00868_f013"][i], row["p00868_f020"][i], row["p00868_f030"][i]]

        # 使用null代替--
        row_data = ["null" if val == "--" else val for val in row_data]

        desired_data.append(row_data)

    new_headers = ["代码", "名称", "交易日期", "前收盘价", "开盘价", "最高价", "最低价", "收盘价", "涨跌",
                   "涨跌幅(%)",
                   "已计息天数", "应计利息", "剩余期限(年)", "当期收益率(%)", "纯债到期收益率(%)", "纯债价值",
                   "纯债溢价", "纯债溢价率(%)", "转股价格", "转股比例", "转换价值", "转股溢价", "转股溢价率(%)",
                   "转股市盈率", "转股市净率", "套利空间", "平价/底价", "期限(年)", "发行日期",
                   "票面利率/发行参考利率(%)", "交易市场", "债券类型"]

    with open(f'data/{yesterday}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(new_headers)
        csvwriter.writerows(desired_data)


def save_to_db(data, trade_day):
    env = Env()
    env.read_env()
    config = env.json('MYSQL')
    engine = create_engine(
        f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db']}")

    # 创建inspect对象
    inspector = inspect(engine)

    if not inspector.has_table(trade_day):
        data.to_sql(trade_day, con=engine, if_exists='replace', index=False)

    # 关闭数据库连接
    engine.dispose()
    return True


def is_trade_day(date):
    """
    判断是否是交易日

    :param date:
    :return:
    """
    if is_workday(date):
        if date.isoweekday() < 6:
            return True
    return False


def send_msg(message, action="qywx", webhook="H", msg_type="text", url="https://api.xbxin.com/msg"):
    data = {
        "message": message,
        "action": action,
        "webhook": webhook,
        "msg_type": msg_type,
    }

    requests.post(url, json=data)


def main():
    # today = datetime(2024, 6, 28)
    today = datetime.now()
    trade_day = today - timedelta(days=1)
    if is_trade_day(trade_day):
        trade_day = trade_day.strftime("%Y%m%d")
        ths = THS(trade_day)
        data = ths.get_data()
        if data is not None:
            save_to_csv(data, trade_day)
            try:
                save_to_db(data, trade_day)
            except Exception as e:
                send_msg(f"可转债（数据库相关）：{e}")
        else:
            send_msg("可转债：获取交易数据失败")


if __name__ == '__main__':
    main()
