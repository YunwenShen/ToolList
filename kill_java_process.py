# -*- coding: utf-8 -*-

import os
import re


def show_all_process():
    """
    展示所有运行的进程
    :return:
    """
    task_list = os.popen("tasklist")
    return task_list.readlines()


def find_java_process(task):
    """
    寻找java进程的pid
    :param task:
    :return:
    """
    pattern = re.compile("java\.exe.*?(\d+)")
    result_list = re.findall(pattern, task)
    return result_list[0]


def kill_java_process(pid):
    """
    杀死进程
    :param pid:
    :return:
    """
    command = "tskill " + pid
    os.popen(command)


def run():
    task_list = show_all_process()
    for task in task_list:
        if "java.exe" in task:
            pid = find_java_process(task)
            kill_java_process(pid)


if __name__ == "__main__":
    run()
