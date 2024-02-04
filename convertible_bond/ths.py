import requests
import json
from dotenv import load_dotenv
import os


def get_access_token():
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
