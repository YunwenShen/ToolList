# -*-coding: utf-8 -*-
import os
import datetime
import paramiko

# 本地存放前端项目地址 - 用于存在更新代码
PROJECT_DIR = r"E:\ERP\vueProject"
# 本地存放前端dist包的目录
LOCAL_DIST_PATH = r"E:\ERP\vueProject\dist"
# 本地存放前端dist包的父目录
LOCAL_DIST_PARENT_PATH = "\\".join(LOCAL_DIST_PATH.split("\\")[0:-1])
# 本地存放前端dist包的相对路径
LOCAL_DIST_RELATIVE_PATH = "\\".join(LOCAL_DIST_PATH.split("\\")[0:-1]) + "\\"
# 远程服务器存放dist包的目录
REMOTE_DIST_PATH = '/home/nginx/nginx-setup/html/dist'
# 远程服务器存放dist包的父目录
REMOTE_DIST_PARENT_PATH = "/".join(REMOTE_DIST_PATH.split("/")[0:-1])

HOST_NAME = '192.168.1.225'
USER_NAME = 'root'
PASSWORD = 'dj123456'
PORT = 22


def update_code():
    """
    从svn上更新代码
    """
    print("[INFO]正在更新代码")
    cmd = "svn update " + PROJECT_DIR
    if os.system(cmd) != 0:
        raise RuntimeError("更新代码失败")
    print("[INFO]正在更新代码成功")


def build_project():
    """
    打包svn项目
    """
    print("[INFO]正在打包前端包")
    os.chdir("E:")
    os.chdir("E:/ERP/vueProject")
    build_cmd = "npm run build"
    if os.system(build_cmd) != 0:
        raise RuntimeError("打包失败")
    print("[INFO]正在打包前端包成功")


def login_sftp(hostname, username, password, port=22):
    """
    sftp登录
    :param hostname: 主机名
    :param username: 用户名
    :param password: 密码
    :param port: 端口
    :return: sftp
    """
    transport = paramiko.Transport(hostname, port)
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp


def login_ssh(hostname, username, password, port=22):
    """
    ssh登录
    :param hostname: 主机名
    :param username: 用户名
    :param password: 密码
    :param port: 端口
    :return:
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    return ssh


def upload(sftp, local_path):
    """
    上传dist包到服务器
    :param sftp: sftp句柄
    :param local_path: 本地dist包目录
    :return:
    """
    try:
        for root, dirs, files in os.walk(local_path):
            dist_root = REMOTE_DIST_PARENT_PATH + "/" + root.replace(LOCAL_DIST_RELATIVE_PATH, "")
            for file in files:
                local_path = os.path.join(root, file)
                remote_path = os.path.join(dist_root, file).replace('\\', '/')
                print("[INFO]原文件地址", local_path)
                print("[INFO]新文件地址", remote_path)
                print("---" * 20)
                sftp.put(local_path, remote_path)
    except Exception as e:
        print(e)


def reset_nginx(ssh):
    """
    重启nginx服务器
    :param ssh:
    :return:
    """
    cmd = "cd /home/nginx/nginx-setup/sbin;"
    ssh.exec_command(cmd)
    cmd = "./nginx -s stop"
    ssh.exec_command(cmd)
    cmd = "./nginx"
    ssh.exec_command(cmd)
    print("[INFO]正在重启nginx服务")


def run():
    """
    1、从svn上更新vue前端项目
    2、打包vue前端包
    3、上传到前端服务器
    4、重启nginx
    """
    update_code()
    build_project()
    sftp = login_sftp(HOST_NAME, USER_NAME, PASSWORD)
    upload(sftp, LOCAL_DIST_PATH)
    ssh = login_ssh(HOST_NAME, USER_NAME, PASSWORD)
    reset_nginx(ssh)


if __name__ == "__main__":
    print("start...", datetime.datetime.now())
    run()
    print("end....", datetime.datetime.now())
