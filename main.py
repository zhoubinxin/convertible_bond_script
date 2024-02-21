# 纯债到期收益率大于x的转债个数/当天所有转债数
import datetime

from tqdm import tqdm

from convertible_bond import convertible_bond as cb
from convertible_bond import filehandler as fh
from convertible_bond import mysqlhandler as mysql


def main():
    # 起始日期
    start_date = datetime.date(2023, 2, 1)
    # 结束日期
    end_date = datetime.date(2023, 5, 15)

    # calculate_ratio
    #   ratio
    # calculate_math:
    #   median  计算中位数
    #   avg     计算平均数
    # is_complete
    #   check   检查数据表是否完整
    ctype = "check"
    # 使用 calculate_math 函数需要填入列名
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

    name_list = {
        "ratio": ("日期", "纯债到期收益率 > 3% 的转债个数", "转债总数"),
        "median": ("日期", "中位数"),
        "avg": ("日期", "平均数"),
        "check": ("数据表", "缺失数据"),
    }

    # 文件名附加日期
    if start_date == end_date:
        excel_name = file_name + str(start_date)
    else:
        excel_name = file_name + str(start_date) + "~" + str(end_date)

    # 设置列名
    try:
        data_list = [name_list[ctype]]
    except KeyError:
        print("不存在方法：", ctype)
        return

    total_days = (end_date - start_date).days + 1
    with tqdm(total=total_days, desc="进度", dynamic_ncols=True) as pbar:
        for current_date in range(total_days):
            current_date = start_date + datetime.timedelta(days=current_date)

            str_date = current_date.strftime('%Y%m%d')
            pbar.set_postfix_str(str_date)

            # 计算数据
            if ctype == "ratio":
                data_tuple = cb.calculate_ratio(current_date, conditions)
            elif ctype == "check":
                data_tuple = mysql.is_complete(current_date)
            else:
                if column == "":
                    column = input("请输入列名：")
                data_tuple = cb.calculate_math(current_date, column, conditions['main'], ctype)

            if data_tuple:
                data_list.append(data_tuple)
            pbar.update(1)

    # 保存数据到Excel
    fh.save_tuple_to_excel(excel_name, data_list)


if __name__ == '__main__':
    main()
