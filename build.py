# -*-coding: utf-8 -*-
"""
1、从svn上更新vue前端项目
2、打包vue前端包
3、上传到前端服务器
4、重启nginx
"""
import os
import datetime
import paramiko

# 本地存放前端项目地址 - 用于存在更新代码
PROJECT_DIR = r"E:\ERP\vueProject"
# 本地存放前端dist包的目录
LOCAL_DIST_PATH = r"E:\ERP\vueProject\dist"
# 远程服务器存放dist包的目录
REMOTE_DIST_PATH = '/home/nginx/nginx-setup/html/dist'

HOST_NAME = '192.168.1.225'
USER_NAME = 'root'
PASSWORD = 'dj123456'
PORT = 22


class UploadFile:
    def __init__(self, hostname, username, password, localPath, remotePath, port=22):
        print("正在与服务器连接")
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.localPath = localPath
        self.localParentPath = "\\".join(localPath.split('\\')[0:-1])
        self.remotePath = remotePath
        self.remoteParentPath = "/".join(remotePath.split('/')[0:-1])
        # sftp
        self.transport = paramiko.Transport(self.hostname, self.port)
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        # ssh
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(self.hostname, self.port, username, password)

    def upload(self):
        try:
            for root, dirs, files in os.walk(self.localPath):
                newRoot = self.remoteParentPath + "/" + root.replace("E:\\ERP\\vueProject\\", "")
                for file in files:
                    localPath = os.path.join(root, file)
                    remotePath = os.path.join(newRoot, file).replace('\\', '/')
                    print("[INFO]原文件地址", localPath)
                    print("[INFO]新文件地址", remotePath)
                    print("---" * 20)

                    self.sftp.put(localPath, remotePath)
        except Exception as e:
            print(e)

    def reset_nginx(self):
        cmd = "cd /home/nginx/nginx-setup/sbin;"
        self.ssh_client.exec_command(cmd)
        cmd = "./nginx -s stop"
        self.ssh_client.exec_command(cmd)
        cmd = "./nginx"
        self.ssh_client.exec_command(cmd)
        print("[INFO]正在重启nginx服务")


def update_code():
    """
    从svn上更新代码
    """
    print("[INFO]正在更新代码")
    cmd = "svn update " + PROJECT_DIR
    p1 = os.system(cmd)
    raise_error(p1, "更新代码错误")
    print("[INFO]正在更新代码成功")


def build_project():
    """
    打包svn项目
    """
    print("[INFO]正在打包前端包")
    os.chdir("E:")
    os.chdir("E:/ERP/vueProject")
    build_cmd = "npm run build"
    p3 = os.system(build_cmd)
    raise_error(p3, "打包失败")
    print("[INFO]正在打包前端包成功")


def upload_to_server():
    """
    上传到前端服务器重启服务
    """
    uploadFile = UploadFile(HOST_NAME, USER_NAME, PASSWORD, LOCAL_DIST_PATH, REMOTE_DIST_PATH)
    uploadFile.upload()
    uploadFile.reset_nginx()


def raise_error(code, reason):
    """
    抛出异常
    :param code: 运行结果
    :param reason: 抛出原因
    """
    if code != 0:
        raise RuntimeError(reason)


def main():
    update_code()
    build_project()
    upload_to_server()


if __name__ == "__main__":
    print("start...", datetime.datetime.now())
    main()
    print("end....", datetime.datetime.now())
