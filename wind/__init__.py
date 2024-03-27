from WindPy import w


def login():
    """
    登录Wind

    :return:
    """
    if not w.isconnected():
        data_wind = w.start()
        if data_wind.ErrorCode != 0:
            print("连接到Wind失败，请检查网络")
