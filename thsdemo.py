import ast
import csv
import datetime
import os
import time

from chinese_calendar import is_workday
from dotenv import load_dotenv

from ths import THS


def main():
    load_dotenv()
    username = os.environ['THSUSER']
    password = os.environ['THSPASS']
    ths = THS(username, password)
    # 数据周期
    start_date = datetime.date(2024, 4, 17)
    end_date = datetime.date(2024, 4, 17)

    for date in range((end_date - start_date).days + 1):
        date = start_date + datetime.timedelta(days=date)
        if is_trade_day(date):
            data = ths.get_data_free(date)
            if data is not None:
                save_to_csv(data, date)
            else:
                raise Exception(f'无法获取数据，日期：{date}')
            time.sleep(3)


def save_to_csv(data, date):
    data = ast.literal_eval(data['rows'])

    if len(data) == 0:
        return

    # 默认列名
    header = ['代码', '名称', 'f016v_pub205', 'bondid_bond063', 'f003v_bond063', '交易日期', '前收盘价', '开盘价',
              '最高价', '最低价', '收盘价', '涨跌',
              '涨跌幅(%)', '已计息天数', '应计利息', '剩余期限(年)', '当期收益率(%)', '纯债到期收益率(%)', '纯债价值',
              '纯债溢价',
              '纯债溢价率(%)', '转股价格', 'f004n_bond063', '转股比例', '转换价值', '转股溢价', '转股溢价率(%)',
              '转股市盈率',
              '转股市净率', '套利空间', '平价/底价', '期限(年)', '发行日期', '票面利率/发行参考利率(%)', '交易市场',
              '债券类型']

    # 要保存的CSV文件名
    file_name = date.strftime('%Y%m%d')
    csv_file = f'data/{file_name}.csv'

    # 写入CSV文件
    try:
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)

            # 写入列名
            writer.writerow(header)

            # 写入数据
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print('请创建data目录')

    print(f'{date} 数据已保存')


def is_trade_day(date):
    if is_workday(date):
        if date.isoweekday() < 6:
            return True
    return False


def test():
    load_dotenv()
    username = os.environ['THSUSER']
    password = os.environ['THSPASS']
    ths = THS(username, password)


if __name__ == '__main__':
    main()
