# -*- coding: utf-8 -*-
# MCDR-Get 插件安装
# 请根据提示修改

def info() -> tuple:
    name = '' # 插件名字
    pip_lib = '' # pip支持库 多个请用 ',' 分割（自带的无需填写）
    lib = '' # mcdr仓库api 多个请用 ',' 分割
    auther = '' # 作者
    api = False # 是否为Api
    remarks_cn = '' # 介绍 中文
    remarks = '' # 介绍 英文
    raw = '' # 下载地址
    raw_cn = '' # 国内下载地址
    return name, pip_lib, lib, auther, api, remarks ,remarks_cn, raw, raw_cn

def install(server):
    # server.download(link, filename, file_path) 下载文件 默认插件文件夹
    # server.say(text) 往服务器发送信息
    # server.reload(plugin) 重载插件 如非必要请勿执行
    pass
