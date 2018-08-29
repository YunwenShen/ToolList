# -*- coding: utf-8 -*-

import os
import re


def find_form_file(file_dir):
    """
    寻找到form文件
    :return:
    """
    file_path_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if match_form_file(file):
                file_path_list.append(os.path.join(root, file))
    return file_path_list


def match_form_file(file_name):
    """
    匹配文件名是否符合form要求
    :param file_name: 文件名
    :return: true
    """
    pattern = re.compile("[fF]orm\.java")
    result = re.findall(pattern, file_name)
    return True if len(result) > 0 else False


def open_form_file(file_path):
    """
    将javaForm格式转换成dict格式
    :return:
    """
    with open(file_path, encoding="utf-8") as file:
        return file.read()


def replace_static_field(string):
    """
    去除静态域
    :param string: 字符串
    :return: 
    """
    pattern = re.compile(r'private static final .*')
    return re.sub(pattern, "", string)


def replace_annotation(string):
    """
    替换注解@
    :param string: 文件内容
    :return: 去除@注解的文本
    """
    pattern = re.compile(r'@.+\n')
    return re.sub(pattern, "", string)


def find_field_comments(string):
    """
    获得form的数据域以及注释(单行注释以及3行注释)
    :param string: 文件内容(必须先进行去除注解)
    :return:  文件内容
    """
    # TODO 可以添加更多规则的正则
    array_list = []
    pattern = re.compile("\/(.*\n.*\n.*)\/\n.*?(private .*)|\/(.*?)\/\n.*?(private .*)")
    result = re.findall(pattern, string)
    for t in result:
        map = dict()
        for item in t:
            # 注释
            if "*" in item:
                comment = replace_invalid_letter(item)
                comment = split_space(comment)
                map["comment"] = comment
            if "private" in item:
                field = find_field(item)
                map["field"] = split_space(field)
        array_list.append(map)
    return array_list


def replace_invalid_letter(string):
    """
    过滤非法字符（\n\t*）
    :param string 字符串
    :return:
    """
    string = string.replace("\n", "")
    string = string.replace("\t", "")
    string = string.replace("*", "")
    return string


def find_field(string):
    """
    过滤出数据域
    :param string: 字符串
    :return:
    """
    pattern = re.compile("private .* (.*);")
    return re.findall(pattern, string)[0]


def split_space(string):
    """
    去除空字符串
    :param string 字符串
    :return:
    """
    return "".join(string.split())


def write_to_field(path, map_list):
    """
    将表单写入文件中
    :param path: 写入文件的路径
    :param map_list: 字典列表
    :return: 
    """
    start = "var form={\n"
    end = "\n}"
    form = ""
    for map in map_list:
        # form += "\t // " + map["comment"] + '\n'
        form += '\t"' + map["field"] + '":"",\n'
    content = start + form + end
    with open(path, "w+", encoding="utf-8") as file:
        file.write(content)


def find_file_name(relative_path):
    """
    在绝对路径中找到文件名
    :param relative_path: 绝对路径
    :return: 文件名
    """
    file_name = relative_path.split("\\")[-1]
    return file_name


def run(file_dir, new_file_dir):
    """
    生成表单
    :param file_dir: 存放原来表单的路径
    :param new_file_dir: 存放新表单的路径
    :return: 
    """
    file_path_list = find_form_file(file_dir)
    for filePath in file_path_list:
        file_name = find_file_name(filePath)
        print(file_name)
        path = os.path.join(new_file_dir, str(file_name) + ".json")
        file_content = open_form_file(filePath)
        file_content = replace_static_field(file_content)
        file_content = replace_annotation(file_content)
        map_list = find_field_comments(file_content)
        write_to_field(path, map_list)


if __name__ == "__main__":
    directory = r"E:\ERP\dy-parent-develop-es\dy-flat-api"
    new_directory = r'E:\test'
    run(directory, new_directory)
