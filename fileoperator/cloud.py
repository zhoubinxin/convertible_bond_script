import json

from webdav3.client import Client


class CloudClient(object):
    @classmethod
    def upload(cls, local_file):
        with open('webdav.json') as f:
            config = json.load(f)
        # WebDAV服务器的地址、用户名和密码
        webdav_url = config['webdav_url']
        webdav_username = config['webdav_username']
        webdav_password = config['webdav_password']

        # 初始化WebDAV客户端
        client = Client({
            'webdav_hostname': webdav_url,
            'webdav_login': webdav_username,
            'webdav_password': webdav_password
        })

        remote_file = '/convertible_bond.db'

        try:
            client.upload(remote_file, local_file)
            return True
        except Exception as e:
            print(e)
            return False
