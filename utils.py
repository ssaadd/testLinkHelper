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
    read config from file_name, if success, return a instance of ConfigParser
    parameter:
        file_name: the path of the config file
    '''
    config = configparser.ConfigParser()
    if os.path.exists(file_name):
        config.read(file_name)
    else:
        raise FileNotFoundError
    return config


def write_config_file(file_name, para_dict):
    '''
    write user config into the config file.
    parameter:
        file_name: the path of the config file
        para_dict: contents of the config, it must be a dict like this:
            para_dict={
                'server': {'host': '192.168.1.1', 'port': '80', 'user': 'admin'},
                'local': {'server': 'xxx.xxx.xxx', 'test': 'test'}, }
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


if __name__ == '__main__':
    try:
        read_config_file('filename.ini')
    except Exception as err:
        print("Capture error: %s" % str(err))
