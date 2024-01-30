import os
import time
import pandas as pd
import datetime
import json


def create_file(file_name):
    """


    :param file_name:
    :return:
    """
    directory_path = os.path.join(os.getcwd(), file_name)
    # 创建data目录，用于存储数据
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    return True


def save_to_excel(excel_name, data):
    """

    :param excel_name:
    :param data:
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


def get_json_data(file_name, json_name, key):
    """

    :param file_name:
    :param json_name:
    :param key:
    :return:
    """
    create_file(file_name)
    directory_path = os.path.join(os.getcwd(), file_name)
    json_name = json_name.strftime("%Y%m%d")
    file_path = rf'{directory_path}\{json_name}.json'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            if key in data:
                return data[key]

    return None


def save_json_data(file_name, json_name, data, key):
    """

    :param file_name:
    :param json_name:
    :param data:
    :param key:
    :return:
    """
    create_file(file_name)
    directory_path = os.path.join(os.getcwd(), file_name)
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
