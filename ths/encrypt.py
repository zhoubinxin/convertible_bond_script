import hashlib
import json

import requests


class ThsEncrypt(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_cookie(self):
        username = self.encode(self.username)
        password = self.encode(self.hex_md5(self.password))

        url = "http://ft.10jqka.com.cn/thsft/jgbservice"

        params = {
            "reqtype": "verify",
            "account": username,
            "passwd": password,
            "qsid": "800",
            "securities": "同花顺iFinD",
            "jgbversion": "1.10.12.405",
            "Encrypt": "1"
        }

        response = requests.get(url, params=params)

        set_cookie = response.headers['Set-Cookie'].replace(" ", '')

        cookie_list = set_cookie.split(';')
        cookies = {}
        for cookie in cookie_list:
            key_value_pairs = cookie.split(',')
            for pair in key_value_pairs:
                key_value = pair.split('=')
                cookies[key_value[0]] = key_value[1]

        return cookies

    def encode(self, b):
        data = {
            "key": b
        }

        # 设置请求头
        headers = {
            "Content-Type": "application/json"
        }

        # 发送 POST 请求
        response = requests.post("https://neoapi.bxin.top/ths", data=json.dumps(data), headers=headers)
        return response.text

    def hex_md5(self, c):
        # 创建MD5哈希对象
        md5_hasher = hashlib.md5()
        # 将输入字符串编码为UTF-8并更新MD5哈希对象
        md5_hasher.update(c.encode('utf-8'))
        # 返回MD5加密结果的十六进制表示
        return md5_hasher.hexdigest()


def main():
    ths = ThsEncrypt('', '')
    ths.get_cookie()


if __name__ == '__main__':
    main()
