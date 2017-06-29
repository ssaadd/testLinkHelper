# -*- coding:utf-8 -*-
#
# Copyright 2017 , donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#

import configparser
import os.path


def join_url(base, url):
    if base.endswith('/'):
        base = base[:-1]
    return '/'.join((base, url))


def read_config_file(file_name):
    '''
    读取配置文件信息
    参数:
        file_name: 配置文件路径
        配置文件内容格式：
            [sectionA]
                server_url = http://192.168.1.200:8700/testlink
                devkey = 20f9b350323cc147deceb53fd73b83ee
                proxy = xxx
                login_name = root
            [sectionB]
                ......
    返回值：
        读取成功，返回ConfigParser对象，格式为：
         config={
                'sectionA': {'host': '192.168.1.1', 'port': '80', 'user': 'admin'},
                'sectionb': {'server': 'xxx.xxx.xxx', 'test': 'test'}, }
        失败抛出异常
    '''
    config = configparser.ConfigParser()
    if os.path.exists(file_name):
        config.read(file_name)
    else:
        raise FileNotFoundError
    return config


def write_config_file(file_name, para_dict):
    '''
    将配置信息写入配置文件.
    参数:
        file_name: 配置文件路径
        para_dict: 配置参数字典，其格式必须如下格式
            para_dict={
                'server': {'host': '192.168.1.1', 'port': '80', 'user': 'admin'},
                'local': {'server': 'xxx.xxx.xxx', 'test': 'test'}, }
    返回值：
        成功返回True，失败抛出异常
    '''
    config = configparser.ConfigParser()
    if os.path.exists(file_name):
        config.read(file_name)
    else:
        for section in para_dict:
            config.add_section(section)

    for section in para_dict:
        for option in para_dict[section]:
            config.set(section, option, para_dict[section][option])
    with open(file_name, 'w') as f:
        config.write(f)
    return True


if __name__ == '__main__':
    try:
        read_config_file('filename.ini')
    except Exception as err:
        print("Capture error: %s" % str(err))
