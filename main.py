# 纯债到期收益率大于x的转债个数/当天所有转债数
import datetime

from tqdm import tqdm

from convertible_bond import convertible_bond as cb
from convertible_bond import filehandler as fh


def main():
    # 起始日期
    start_date = datetime.date(2023, 2, 1)
    # 结束日期
    end_date = datetime.date(2023, 5, 15)

    # 0 -> calculate_ratio
    # 1 -> median
    # 2 -> avg
    flag = 0
    # 计算median、avg需要填入列名
    column = "涨跌幅(%)"

    # 文件名
    file_name = ""

    # 筛选条件
    conditions = {
        "main": [
            "债券类型 = '可转债'",
            "`纯债到期收益率(%)` > 3",
            "((`转换价值` - `纯债价值`) / `纯债价值`) > 0.2"
        ],
        "ratio_total": [
            "债券类型 = '可转债'"
        ]
    }

    name_list = [
        ("日期", "纯债到期收益率 > 3% 的转债个数", "转债总数"),
        ("日期", "中位数"),
        ("日期", "平均数")
    ]

    # 文件名附加日期
    if start_date == end_date:
        excel_name = file_name + str(start_date)
    else:
        excel_name = file_name + str(start_date) + "~" + str(end_date)

    # 增加列名
    data_list = [name_list[flag]]

    if flag == 1 or flag == 2:
        if column == "":
            column = input("请输入列名：")

    total_days = (end_date - start_date).days + 1
    with tqdm(total=total_days, desc="进度", dynamic_ncols=True) as pbar:
        for current_date in range(total_days):
            current_date = start_date + datetime.timedelta(days=current_date)

            str_date = current_date.strftime('%Y%m%d')
            pbar.set_postfix_str(str_date)

            # 计算数据
            if flag == 0:
                data_tuple = cb.calculate_ratio(current_date, conditions)
            if flag == 1:
                # 计算中位数
                data_tuple = cb.calculate_math(current_date, column, conditions['main'], 'median')
            if flag == 2:
                # 计算平均数
                data_tuple = cb.calculate_math(current_date, column, conditions['main'], 'avg')

            data_list.append(data_tuple)
            pbar.update(1)

    # 保存数据到Excel
    fh.save_tuple_to_excel(excel_name, data_list)


if __name__ == '__main__':
    main()
