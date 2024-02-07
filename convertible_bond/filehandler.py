import os
import time
import pandas as pd
import datetime
import json


def create_file(file_name="data"):
    """
    创建文件夹，用于存储数据

    :param file_name: 文件夹名
    :return:
    """
    directory_path = os.path.join(os.getcwd(), file_name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def save_to_excel(excel_name, data):
    """
    保存数据到Excel文件

    :param excel_name: Excel文件名
    :param data: 数据
    :return:
    """
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


def save_tuple_to_excel(excel_name, data):
    """
    将元组数据保存到Excel文件中。

    :param excel_name: Excel文件名
    :param data: 数据
    :return:
    """
    file_path = os.path.join(os.getcwd(), f'{excel_name}.xlsx')
    df = pd.DataFrame(data[1:], columns=data[0])
    max_attempts = 5
    attempt = 1

    while attempt <= max_attempts:
        try:
            # 检查文件是否存在
            if os.path.exists(file_path):
                existing_data = pd.read_excel(file_path)
                df = pd.concat([existing_data, df], ignore_index=True)

            # 将数据写入 Excel 文件
            with pd.ExcelWriter(file_path, mode='w', engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

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


def get_json_data(json_name, key, file_name="data"):
    """
    从JSON文件中获取数据

    :param json_name: json文件名
    :param key: 键名
    :param file_name: 文件夹名
    :return: key对应的值
    """
    create_file(file_name)
    directory_path = os.path.join(os.getcwd(), file_name)
    if isinstance(json_name, datetime.datetime):
        # 如果 json_name 是日期时间对象，则将其转换为字符串
        json_name = json_name.strftime("%Y%m%d")
    file_path = rf'{directory_path}\{json_name}.json'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            if key in data:
                return data[key]

    return None


def save_json_data(json_name, data, key, file_name="data"):
    """
    将数据保存到JSON文件中

    :param json_name: json文件名
    :param data: 要保存的数据
    :param key: 键名
    :param file_name: 文件夹名
    :return:
    """
    create_file(file_name)
    directory_path = os.path.join(os.getcwd(), file_name)
    if isinstance(json_name, datetime.datetime):
        # 如果 json_name 是日期时间对象，则将其转换为字符串
        json_name = json_name.strftime("%Y%m%d")
    file_path = rf'{directory_path}\{json_name}.json'

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
