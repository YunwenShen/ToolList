# -*- coding: utf-8 -*-
import requests

# 请求头
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 "
                  "Safari/537.36 "
}
# 登录url
LOGIN_URL = "http://gqt1.cloud/auth/login"
# 流量续命地址
FREE_FLOW_URL = "http://gqt1.cloud/user/checkin"
# session
SESSION = requests.session()


def login(username, password):
    """
    登录网站
    :param username: 用户名
    :param password: 密码
    :return:
    """
    data = {
        "email": username,
        "passwd": password,
        "code": ""
    }
    res = SESSION.post(LOGIN_URL, data, headers=HEADERS)
    print(res.json())


def get_free_flow():
    """
    获取免费流量
    :return:
    """
    res = SESSION.post(FREE_FLOW_URL)
    print(res.json())


def run(username, password):
    """
    程序入口
    :param username: 用户名
    :param password: 密码
    :return:
    """
    login(username, password)
    get_free_flow()


if __name__ == "__main__":
    run("shenyunwen520@qq.com", "123456syw")
