import json
import os

import requests
from dotenv import load_dotenv


def get_access_token():
    """
    获取 access_token

    :return: access_token
    """
    # 加载 .env 文件中的环境变量
    load_dotenv()

    refresh_token = os.getenv('REFRESHTOKEN')
    print(refresh_token)
    url = 'https://ft.10jqka.com.cn/api/v1/get_access_token'
    header = {"ContentType": "application/json", "refresh_token": refresh_token}
    response = requests.post(url=url, headers=header)

    print(response)
    access_token = json.loads(response.content)['data']['access_token']

    return access_token


def get_data(request_url, form_data):
    """
    获取数据

    :param request_url: 请求地址
    :param form_data: 请求参数
    :return:
    """
    #  获取 access_token
    access_token = get_access_token()

    requestHeaders = {"Content-Type": "application/json", "access_token": access_token}

    # 发送POST请求
    response = requests.post(request_url, headers=requestHeaders, data=json.dumps(form_data))

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 JSON 响应
        data = response.json()
        # 保存json数据
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return data
    else:
        # 打印错误信息
        print("请求出错: {}".format(response.status_code))
