import os

from convertible_bond_script.bondday import BondDay
from fileoperator import FileOperator


def main():
    menu = """
        0. 退出
        1. 上传数据库
        2. 更新数据库
        """
    while True:
        print(menu)
        option = int(input('请输入选择：'))
        if option == 1:
            FileOperator.upload('convertible_bond.db')
            input('上传完成，请按任意键继续...')
        elif option == 2:
            BondDay.db_init()
            input('更新完成，请按任意键继续...')
        elif option == 0:
            break

        # 清空面板
        os.system('cls')


if __name__ == '__main__':
    main()
