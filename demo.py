# 纯债到期收益率大于x的转债个数/当天所有转债数
import datetime
from tqdm import tqdm
from convertible_bond import convertible_bond as cb
from convertible_bond import filehandler as fh


def main():
    # 数据周期
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 1, 31)

    excel_name = "2020"

    data_consider = {
        # 转股价值
        "consider_cv": False,
        "cv_range": "",
        # 债券余额，单位为亿
        "consider_balance": False,
        "balance_range": "",
        # 债券评级
        "consider_issue": False,
        "issue": "",
        # 纯债到期收益率
        "consider_ytm": True,
        "ytm_range": "`纯债到期收益率(%)` > 3",
    }

    data_list = [
        ("日期", "纯债到期收益率 > 3% 的转债个数", "转债总数")
    ]

    total_days = (end_date - start_date).days + 1
    with tqdm(total=total_days, desc="进度", dynamic_ncols=True) as pbar:
        for current_date in range(total_days):
            current_date = start_date + datetime.timedelta(days=current_date)

            if current_date.weekday() in [5, 6]:
                data_list.append((str(current_date), None, None))
                continue

            str_date = current_date.strftime('%Y%m%d')
            pbar.set_postfix_str(str_date)

            data_tuple = cb.calculate_ratio(current_date, data_consider)
            data_list.append(data_tuple)
            pbar.update(1)

    fh.save_tuple_to_excel(excel_name, data_list)


if __name__ == '__main__':
    main()
