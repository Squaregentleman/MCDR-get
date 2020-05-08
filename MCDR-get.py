# -*- coding: utf-8 -*-

import platform
import os
import json
import urllib
import re
import time
import requests
import shutil
import yaml
from urllib.request import urlopen
from urllib.parse import unquote
from utils import constant


Prefix = '!!mget'
PluginName = 'MGet'
debug = False


sysb = platform.system()
if sysb != 'windows':
    ppath = os.path.join('plugins/')
    cconfig = os.path.join('plugins', 'config/')
    configpath = os.path.join('plugins', 'config', 'mget.json')
    listpath = os.path.join('plugins', 'mget', 'list.json')
    mconfig = os.path.join('plugins', 'mget/')
else:
    ppath = os.path.join('plugins\\')
    cconfig = os.path.join('plugins', 'config\\')
    configpath = os.path.join('plugins', 'config', 'mget.json')
    listpath = os.path.join('plugins', 'mget', 'list.json')
    mconfig = os.path.join('plugins', 'mget\\')

ver = constant.VERSION.split('-')[0]
ver = float('.'.join(ver.split('.')[0:2]))
chunk_size = 8

if ver >= 0.8:
    from utils.rtext import *
else:
    print('[' + PluginName + '] 不支持0.8.1以前的版本!')

config = None
lang = None


def get_text(text, mous='', cickrun='', color=RColor.white, run=True):
    if mous != '':
        if cickrun != '':
            if run:
                stxt = RText(text, color=color).set_hover_text(
                    mous).set_click_event(RAction.run_command, cickrun)
            else:
                stxt = RText(text, color=color).set_hover_text(
                    mous).set_click_event(RAction.suggest_command, cickrun)
        else:
            stxt = RText(text, color=color,
                         styles=RStyle.italic).set_hover_text(mous)
    else:
        if cickrun == '':
            stxt = RText(text, color=color)
        else:
            if run:
                stxt = RText(text, color=color).set_click_event(
                    RAction.run_command, cickrun)
            else:
                stxt = RText(text, color=color).set_click_event(
                    RAction.suggest_command, cickrun)
    return stxt


def get_open_url(text, mous, cickrun, color=RColor.white):
    return RText(text, color=color).set_hover_text(mous).set_click_event(RAction.open_url, cickrun)


def load_config():
    global config
    if debug:
        # print(configpath)
        # print(os.getcwd())
        # print(open_file(configpath))
        config = json.loads(open_file(configpath))
        return True
    else:
        try:
            config = json.loads(open_file(configpath))
            return True
        except:
            config = json.loads('{"language": "","source": 0,"boosbar": 0,"pip":""}')
            if not os.path.exists(mconfig):
                os.mkdir(mconfig)
            if not os.path.exists(cconfig):
                os.mkdir(cconfig)
            return False


def load_lang():
    global lang
    global config
    if debug:
        lang = yaml.load(open_file(mconfig + config['language'] + '.yml'), Loader=yaml.FullLoader)
        # print(lang)
        return lang
    else:
        try:
            lang = yaml.load(open_file(mconfig + config['language'] + '.yml'), Loader=yaml.FullLoader)
            # print(lang)
            return lang
        except:
            print('load lang no')
            return


def save_config():
    global config
    if debug:
        f = open(configpath, 'w')
        f.write(json.dumps(config))
        f.close()
        return True
    else:
        try:
            f = open(configpath, 'w')
            f.write(json.dumps(config))
            f.close()
            return True
        except:
            return False


def save_file(fill, msg):
    if debug:
        f = open(fill, 'w')
        f.write(msg)
        f.close()
        return True
    else:
        try:
            f = open(fill, 'w')
            f.write(msg)
            f.close()
            return True
        except:
            return False


def open_file(fill):
    with open(fill, 'r') as f:
        return f.read()


def on_load(server, old):
    global sysb
    global config
    sysb = platform.system()
    load_config()
    lang = load_lang()
    if lang:
        server.add_help_message(Prefix, lang['Plugin'])
    else:
        server.add_help_message(Prefix, '插件库 / Plugin Library')

def getsys():
    global sysb
    sysb = platform.system()
    return sysb

# HelpMessage {0} 点击查看插件列表 {1} 列出插件 {2} 点击输入 {3} 安装插件 {4} 点击更新插件列表 {5} 更新列表 {6} 更新插件 {7} 删除插件 {8} 插件配置
def printhelp(server, info):
    HelpMessage = RTextList(
        get_text('§7------------§bMCDR ' + PluginName + '§7------------\n      '),
        get_text(f'§7{Prefix} list', lang['cicklist'], f'{Prefix} list'),
        get_text(' §r' + lang['listp'] + '\n      '),
        get_text(f'§7{Prefix} find <Plugin>', lang['cickrun'], f'{Prefix} find ',run=False),
        get_text(' §r' + lang['findplugin'] + '\n      '),
        get_text(f'§7{Prefix} install ', lang['cickrun'], f'{Prefix} install ',run=False),
        get_text(' §r' + lang['instp'] + '\n      '),
        get_text(f'§7{Prefix} update', lang['cickupdate'], f'{Prefix} update'),
        get_text(' §r' + lang['uplist'] + '\n      '),
        get_text(f'§7{Prefix} updatelang', lang['cickrun'], f'{Prefix} updatelang',),
        get_text(' §r' + lang['updatelang'] + '\n      '),
        get_text(f'§7{Prefix} update <Plugin>', lang['cickrun'], f'{Prefix} update ',run=False),
        get_text(' §r' + lang['updateplugin'] + '\n      '),
        get_text(f'§7{Prefix} rm <Plugin>', lang['cickrun'], f'{Prefix} rm ',run=False),
        get_text(' §r' + lang['rmplugin'] + '\n      '),
        get_text(f'§7{Prefix} config', lang['cickconfighelp'], f'{Prefix} config',),
        get_text(' §r' + lang['pluginconfig'])
    )
    send_player(server, info, HelpMessage)

def get_list():
    global config
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    if config['source'] == 1:
        res = urllib.request.Request(url='https://raw.githubusercontent.com/Squaregentleman/MCDR-get/master/list.json', headers=headers)
        return str(urlopen(res).read(), 'utf-8')
    else:
        res = urllib.request.Request(
            url='https://gitee.com/fkj2005/MCDR-Get/raw/master/list.json', headers=headers)
        return str(urlopen(res).read(), 'utf-8')


def get_lang():
    global config
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    if config['source'] == 1:
        if config['language'] == 'zh-cn':
            res = urllib.request.Request(url='https://raw.githubusercontent.com/Squaregentleman/MCDR-get/master/zh-cn.yml', headers=headers)
        else:
            res = urllib.request.Request(url='https://raw.githubusercontent.com/Squaregentleman/MCDR-get/master/en-us.yml', headers=headers)
        return str(urlopen(res).read(), 'utf-8')
    else:
        if config['language'] == 'zh-cn':
            res = urllib.request.Request(url='https://gitee.com/fkj2005/MCDR-Get/raw/master/zh-cn.yml', headers=headers)
        else:
            res = urllib.request.Request(url='https://gitee.com/fkj2005/MCDR-Get/raw/master/en-us.yml', headers=headers)
        return str(urlopen(res).read(), 'utf-8')


def on_info(server, info):
    global config
    global lang
    if info.content.startswith(Prefix):
        if server.get_permission_level(info) >= 3:
            args = info.content.split(' ')
            if os.path.exists(configpath) == False:
                if len(args) >= 2:
                    init(server, info)
                else:
                    say(server, '[§b' + PluginName + '§r] §6检测到首次启动 请输入 {0} init 初始化 / First boot detected please enter {0} init initialization'.format(
                        Prefix))
                    return
            elif len(args) == 1:
                printhelp(server, info)
            elif len(args) == 2:
                if args[1] == 'list':
                    if os.path.exists(listpath):
                        if open_file(listpath) != '':
                            list_print(server, info)
                        else:
                            if debug:
                                save_file(listpath, get_list())
                                list_print(server, info)
                            else:
                                try:
                                    save_file(listpath, get_list())
                                    list_print(server, info)
                                except:
                                    say(server, '[§b' + PluginName + '§r] §6' + lang['updatelist_off'])
                                    return
                    else:
                        if debug:
                            save_file(listpath, get_list())
                            list_print(server, info)
                        else:
                            try:
                                save_file(listpath, get_list())
                                list_print(server, info)
                            except:
                                say(server, '[§b' + PluginName + '§r] §6' + lang['updatelist_off'])
                                return
                elif args[1] == 'update':
                    if debug:
                        save_file(listpath, get_list())
                        say(server, '[§b' + PluginName + '§r] §6' + lang['updatelist'])
                    else:
                        try:
                            save_file(listpath, get_list())
                            say(server, '[§b' + PluginName + '§r] §6!' + lang['updatelist'])
                        except:
                            say(server, '[§b' + PluginName + '§r] §6' + lang['updatelist_off'])
                            return
                elif args[1] == 'updatelang':
                    say(server, '[§b' + PluginName + '§r] §4' + lang['updateload'].format('§6' + config['language'] + '.yml'), info, True)
                    if save_file(mconfig + config['language'] + '.yml', get_lang()):
                        say(server, '[§b' + PluginName + '§r] §6' + lang['saveyes'], info, True)
                    else:
                        say(server, '[§b' + PluginName + '§r] §6' + lang['saveno'], info, True)
                if args[1] == 'config':
                    # {0} 语言 {1} 下载源 {2} 进度条 {3} pip命令
                    send_config(server,info)
            elif len(args) == 3:
                if args[1] == 'install':
                    plugin_info = get_plugin_info(args[2])
                    if plugin_info['lib']:
                        # lib = ','.join(plugin_info['lib'])
                        lib = None
                        for line in plugin_info['lib']:
                            if lib:
                                lib = RTextList(
                                    get_text('§b,'),
                                    get_text('§b' + line,lang['cickinfo'],'!!' + PluginName + ' getlib ' + line),
                                    lib
                                    )
                            else:
                                lib = RTextList(
                                    get_text('§b' + line,lang['cickinfo'],'!!' + PluginName + ' getlib ' + line)
                                )
                    else:
                        lib = '§b' + lang['libno']
                    if plugin_info['pip_lib']:
                        pylib = ','.join(plugin_info['pip_lib'])
                    else:
                        pylib = '§b' + lang['libno']
                    url = get_open_url('§r[§b' + lang['cickopen'] + '§r]', plugin_info['raw_url'] if config['language'] == 'zh-cn' else plugin_info['raw_url_cn'], plugin_info['raw_url'] if config['language'] == 'zh-cn' else plugin_info['raw_url_cn'])
                    send_player(server, info, RTextList(
                        get_text('§7------------§bMCDR ' + PluginName + '§7------------'),
                        get_text('\n      §6' + lang['installp'] + ': §b' + args[2]),
                        get_text('\n      §6' + lang['author'] + ': §b' + plugin_info['author']),
                        get_text('\n      §6' + lang['downloadurl'] + '(Github): ') if config['language'] == 'zh-cn' else get_text('\n      §6' + lang['downloadurl'] + '(Gitee): '),
                        url,
                        get_text('\n      §6' + lang['downloadlib'] + ': §b'),
                        lib,
                        get_text('\n      §6' + lang['pylib'] + ': §b' + pylib),
                        get_text('\n      ['),
                        get_text('√',lang['install'],Prefix + ' yinstall ' + args[2],color=RColor.green),
                        get_text(']')
                    ))
                elif args[1] == 'find':
                    findlist_print(server, info, args[2])
                elif args[1] == 'yinstall':
                    if not install(server, info):
                        server.tell(info.player, '[§b' + PluginName + '§r] §4' + lang['notplugin'])
                        return
                    send_player(server, info, get_text('[§b' + PluginName + '§r] §6' + lang['autoload']))
                    server.refresh_changed_plugins()
                elif args[1] == 'getlib':
                    plugin_info = get_plugin_lib_info(args[2])
                    print(plugin_info)
                    if config['language'] != 'zh-cn':
                        url = plugin_info['raw_url_cn']
                    else:
                        url = plugin_info['raw_url']
                    send_player(server, info, RTextList(
                        get_text('§7------------§bMCDR ' + PluginName + '§7------------'),
                        get_text('\n      §6' + lang['apiname'] + ': §b' + args[2]),
                        get_text('\n      §6' + lang['apiauthor'] + ': §b' + plugin_info['author']),
                        get_text('\n      §6' + lang['downloadurl'] + '(Github): ') if config['language'] != 'zh-cn' else get_text('\n      §6下载地址(Gitee): '),
                        get_open_url('§r[§b' + lang['cickopen'] + '§r]', url, url)
                    ))
                elif args[1] == 'update':
                    if not install(server, info):
                        server.tell(info.player, '[§b' + PluginName + '§r] §4' + lang['notplugin'])
                        return
                    send_player(server, info, get_text('[§b' + PluginName + '§r] §6' + lang['autoload']))
                    server.refresh_changed_plugins()
                elif args[1] == 'rm':
                    send_player(server, info, RTextList(
                        get_text('[§b' + PluginName + '§r] '), 
                        get_text(lang['remove'] + ' ', '', '', RColor.red), 
                        get_text('['),
                        get_text('√', lang['install'], Prefix + ' yrm ' + args[2], RColor.aqua),
                        get_text(']')
                    ))
                elif args[1] == 'yrm':
                    js = open_file(listpath)
                    js_jx = json.loads(js)
                    if debug:
                        for line in js_jx['list']:
                            if line['name'] == args[2]:
                                os.remove(ppath + line['file'])
                        send_player(server, info, RTextList(
                            get_text('[§b' + PluginName + '§r] '), 
                            get_text(lang['removeyes'], color=RColor.red)
                        ))
                        server.refresh_changed_plugins()
                        send_player(server, info, get_text('[§b' + PluginName + '§r] §6' + lang['autoload']))
                    else:
                        try:
                            for line in js_jx['list']:
                                if line['name'] == args[2]:
                                    os.remove(ppath + line['file'])
                            send_player(server, info, RTextList(
                                get_text('[§b' + PluginName + '§r] '), 
                                get_text(lang['removeyes'], color=RColor.red)
                            ))
                            server.refresh_changed_plugins()
                            send_player(server, info, get_text('[§b' + PluginName + '§r] §6' + lang['autoload']))
                        except:
                            send_player(server, info, RTextList(
                                get_text('[§b' + PluginName + '§r] '), 
                                get_text(lang['removeno'], color=RColor.red)
                            ))
                elif args[1] == 'getinfo':
                    plugin_info = get_plugin_info(args[2])
                    if plugin_info['lib']:
                        # lib = ','.join(plugin_info['lib'])
                        lib = None
                        for line in plugin_info['lib']:
                            if lib:
                                lib = RTextList(
                                    get_text('§b,'),
                                    get_text('§b' + line,lang['cickinfo'],'!!' + PluginName + ' getlib ' + line),
                                    lib
                                    )
                            else:
                                lib = RTextList(
                                    get_text('§b' + line,lang['cickinfo'],'!!' + PluginName + ' getlib ' + line)
                                )
                    else:
                        lib = '§b' + lang['libno']
                    if plugin_info['pip_lib']:
                        pylib = ','.join(plugin_info['pip_lib'])
                    else:
                        pylib = '§b' + lang['libno']
                    if config['language'] != 'zh-cn':
                        bz = '§b' + plugin_info['remarks']
                    else:
                        bz = '§b' + plugin_info['remarks_cn']
                    url = get_open_url('§r[§b' + lang['cickopen'] + '§r]', plugin_info['raw_url'] if config['language'] != 'zh-cn' else plugin_info['raw_url_cn'], plugin_info['raw_url'] if config['language'] != 'zh-cn' else plugin_info['raw_url_cn'])
                    send_player(server, info, RTextList(
                        get_text('§7------------§bMCDR ' + PluginName + '§7------------'),
                        get_text('\n      §6' + lang['installp'] + ': §b' + args[2]),
                        get_text('\n      §6' + lang['author'] + ': §b' + plugin_info['author']),
                        get_text('\n      §6' + lang['remarks'] + ': '),
                        bz,
                        get_text('\n      §6' + lang['downloadurl'] + '(Github): ') if config['language'] != 'zh-cn' else get_text('\n      §6下载地址(Gitee): '),
                        url,
                        get_text('\n      §6' + lang['downloadlib'] + ': §b'),
                        lib,
                        get_text('\n      §6' + lang['pylib'] + ': §b' + pylib)
                    ))
            if len(args) == 4:
                if args[1] == 'config':
                    if args[2] == 'source':
                        if args[3] in ['1', '2']:
                            if debug:
                                config['source'] = int(args[3])
                                save_config()
                                send_player(server, info, get_text(
                                    '[§b' + PluginName + '§r] §6' + lang['saveyes']))
                            else:
                                try:
                                    config['source'] = int(args[3])
                                    save_config()
                                    send_player(server, info, get_text(
                                        '[§b' + PluginName + '§r] §6' + lang['saveyes']))
                                except:
                                    send_player(server, info, get_text(
                                        '[§b' + PluginName + '§r] §6' + lang['saveno']))
                        else:
                            send_player(server, info, get_text(
                                '[§b' + PluginName + '§r] §6' + lang['argserror']))
                    elif args[2] == 'language':
                        if args[3] in ['zh-cn', 'en-us']:
                            if debug:
                                config['language'] = args[3]
                                save_config()
                                load_config()
                                load_lang()
                                send_player(server, info, get_text(
                                    '[§b' + PluginName + '§r] §6' + lang['saveyes']))
                            else:
                                try:
                                    config['language'] = args[3]
                                    save_config()
                                    send_player(server, info, get_text(
                                        '[§b' + PluginName + '§r] §6' + lang['saveyes']))
                                except:
                                    send_player(server, info, get_text(
                                        '[§b' + PluginName + '§r] §6' + lang['saveno']))
                        else:
                            send_player(server, info, get_text(
                                '[§b' + PluginName + '§r] §6' + lang['argserror']))
                    elif args[2] == 'boosbar':
                        if args[3] in ['true', 'false']:
                            if debug:
                                if args[3] == 'true':
                                    config['boosbar'] = 1
                                else:
                                    config['boosbar'] = 2
                                save_config()
                                send_player(server, info, get_text(
                                    '[§b' + PluginName + '§r] §6' + lang['saveyes']))
                            else:
                                try:
                                    if args[3] == 'true':
                                        config['boosbar'] = 1
                                    else:
                                        config['boosbar'] = 2
                                    save_config()
                                    send_player(server, info, get_text(
                                        '[§b' + PluginName + '§r] §6' + lang['saveyes']))
                                except:
                                    send_player(server, info, get_text(
                                        '[§b' + PluginName + '§r] §6' + lang['saveno']))
                        else:
                            send_player(server, info, get_text(
                                '[§b' + PluginName + '§r] §6' + lang['argserror']))

        else:
            server.tell(info.player, '[§b' + PluginName + '§r] §4' + lang['preno'])


def send_config(server, info):
    # {0} 语言 {1} 下载源 {2} 进度条 {3} pip命令
    ConfigMessage = RTextList(
        get_text('§7------------§bMCDR ' + PluginName + '§7------------'),
        get_text('\n      §6' + lang['language'] + ' '),
        get_text('§r[§b中文§r]', '中文', Prefix + ' config language zh-cn'),
        get_text(' '),
        get_text('§r[§bEnglish§r]', 'English', Prefix + ' config language en-us'),
        get_text('\n      §6' + lang['downsource'] + ' '),
        get_text('§r[§bGitHub§r]', '国外源', Prefix + ' config source 1'),
        get_text(' '),
        get_text('§r[§bGitee§r]', '国内源', Prefix + ' config source 0'),
        get_text('\n      §6' + lang['jindutiao'] + ' '),
        get_text('§r[§bTrue§r]', '开启', Prefix + ' config boosbar true'),
        get_text(' '),
        get_text('§r[§bFalse§r]', '关闭', Prefix + ' config boosbar false'),
        get_text('\n      §6' + lang['pipcommand'] + ' '),
        get_text('§r[§bpip§r]', 'pip', Prefix + ' config pip pip'),
        get_text(' '),
        get_text('§r[§bpip3§r]', 'pip3', Prefix + ' config pip pip3'),
        get_text(' '),
        get_text('§r[§bcustom§r]', '自定', Prefix + ' config pip ',run=False)
    )
    send_player(server, info, ConfigMessage)


def say(server, msg, info=None, tell=False):
    if tell or info != None:
        server.tell(info.player, msg)
    else:
        server.say(msg)


def get_plugin_info(name):
    js = open_file(listpath)
    js_jx = json.loads(js)
    for line in js_jx['list']:
        if name.lower() == line['name'].lower():
            return line


def get_plugin_lib_info(name):
    js = open_file(listpath)
    js_jx = json.loads(js)
    for line in js_jx['api_list']:
        if name.lower() == line['name'].lower():
            return line


def install(server, info):
    global config
    global lang
    args = info.content.split(' ')
    js = open_file(listpath)
    js_jx = json.loads(js)
    for line in js_jx['list']:
        if args[2] == line['name']:
            if config['language'] != 'zh-cn':
                download(line['raw_url_cn'], server, info)
            else:
                download(line['raw_url'], server, info)
            if line['lib']:
                for line2 in js_jx['api_list']:
                    if line2['name'] in line['lib']:
                        server.tell(info.player, '§6' + lang['installlib'] + ': ' + line2['name'])
                        download(line2['raw_url'], server, info)
                        if line2['name'] == 'MinecraftItemAPI.json':
                            shutil.copyfile(
                                ppath + 'MinecraftItemAPI.json', 
                                cconfig + 'MinecraftItemAPI.json'
                                )
            if line['pip_lib']:
                for line3 in line['pip_lib']:
                    server.tell(info.player, '§6' + lang['installpylib'] + ': ' + line3)
                    os.system(config['pip'] + ' install ' + line3)
            return True
    return False


def list_print(server, info):
    global lang
    js = open_file(listpath)
    js_jx = json.loads(js)
    server.tell(info.player, '§7------------§bMCDR ' + PluginName + '§7------------')
    for line in js_jx['list']:
        if config['language'] == 'zh-cn':
            h1 = get_text(line['name'], line['remarks_cn'], f'{Prefix} getinfo ' + line['name'], RColor.green)
        else:
            h1 = get_text(line['name'], line['remarks'], f'{Prefix} getinfo ' + line['name'], RColor.green)
        h2 = get_text('   ')
        if os.path.exists(ppath + line['file']):
            h3 = get_text('[uninstall]', '卸载', Prefix +
                          ' rm ' + line['name'], RColor.red)
            h4 = get_text(' ')
            h5 = get_text('[update]', '更新', Prefix +
                          ' update ' + line['name'], RColor.red)
            h6 = RTextList(h3, h4, h5)
        else:
            h6 = get_text('[install]', '安装', Prefix +
                          ' install ' + line['name'], RColor.green)
        send_player(server, info, RTextList(h1, h2, h6))
    send_player(server, info, RTextList(
        get_text(lang['listupdatetime'] + ': ', color=RColor.gold), 
        get_text(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(js_jx['time'])), color=RColor.green)
        ))


def findlist_print(server, info, plugin):
    global lang
    js = open_file(listpath)
    js_jx = json.loads(js)
    server.tell(info.player, '§7------------§bMCDR ' + PluginName + '§7------------')
    now = 0
    for line in js_jx['list']:
        if line['name'].lower().find(plugin.lower()) > -1:
            noww = str_replace(line['name'],plugin)
            if noww == []:
                pass
            else:
                name = line['name'].replace(line['name'][noww[0]:noww[1]], '§4' + line['name'][noww[0]:noww[1]] + '§a')
                if config['language'] == 'zh-cn':
                    h1 = get_text(name, line['remarks_cn'], f'{Prefix} getinfo ' + line['name'], RColor.green)
                else:
                    h1 = get_text(name, line['remarks'], f'{Prefix} getinfo ' + line['name'], RColor.green)
                h2 = get_text('   ')
                if os.path.exists(ppath + line['file']):
                    h3 = get_text('[uninstall]', '卸载', Prefix +
                                ' rm ' + line['name'], RColor.red)
                    h4 = get_text(' ')
                    h5 = get_text('[update]', '更新', Prefix +
                                ' update ' + line['name'], RColor.red)
                    h6 = RTextList(h3, h4, h5)
                else:
                    h6 = get_text('[install]', '安装', Prefix +
                                ' install ' + line['name'], RColor.green)
                send_player(server, info, RTextList(h1, h2, h6))
                now += 1
    send_player(server, info, get_text('§6' + lang['findnow'].format('§4' + str(now) + '§6')))


def str_replace(text, re_text):
    now = text.lower().find(re_text.lower())
    lend = turn(len(text))
    if now > -1:
        turn_now = 0
        while text[now:turn_now].lower() != re_text.lower():
            if turn_now < lend:
                return []
            turn_now -= 1
        return [now,turn_now]


def turn(a):
    a = ~a + 1
    return a    


def send_player(server, info, m1):
    server.reply(info, m1)


def init(server, info):
    args = info.content.split(' ')
    global config
    if args[1] == 'init' and len(args) == 2:
        say(server, '[§b' + PluginName + '§r] §6设置语言 / Set language', info, True)
        m1 = get_text('[中文]', '中文', Prefix +
                      ' init language zh-cn', RColor.aqua)
        m2 = RText(' ', color=RColor.white)
        m3 = get_text('[English]', 'English', Prefix +
                      ' init language en-us', RColor.aqua)
        m4 = RTextList(m1, m2, m3)
        send_player(server, info, m4)
    elif args[1] == 'init' and len(args) == 4:
        if args[2] == 'language':
            if args[3] in ['zh-cn', 'en-us']:
                config['language'] = args[3]
                say(server, '[§b' + PluginName + '§r] §6选择下载源 / Select download source', info, True)
                m1 = get_text('[GitHub]', '国外源 / Github source', Prefix +
                              ' init source 1', RColor.aqua)
                m2 = RText(' ', color=RColor.white)
                m3 = get_text('[Gitee]', '国外源 / Gitee source', Prefix +
                              ' init source 2', RColor.aqua)
                m4 = RTextList(m1, m2, m3)
                send_player(server, info, m4)
        elif args[2] == 'source':
            if args[3] in ['1', '2']:
                config['source'] = int(args[3])
                say(server, '[§b' + PluginName + '§r] §6PIP命令 / PIP command', info, True)
                send_player(server, info, 
                RTextList(
                    get_text('[pip]', 'pip', Prefix + ' init pip pip', RColor.aqua),
                    RText(' ', color=RColor.white),
                    get_text('[pip3]', 'pip3', Prefix + ' init pip pip3', RColor.aqua),
                    RText(' ', color=RColor.white),
                    get_text('[custom]', '自定 / custom', Prefix + ' init pip ', RColor.aqua, False)
                ))
        elif args[2] == 'pip':
            config['pip'] = args[3]
            say(server, '[§b' + PluginName + '§r] §6是否启用进度条 / Enable progress bar or not', info, True)
            m1 = get_text('[True]', '开启 / On', Prefix + ' init boosbar 1', RColor.aqua)
            m2 = RText(' ', color=RColor.white)
            m3 = get_text('[False]', '关闭 / Off', Prefix + ' init boosbar 2', RColor.aqua)
            m4 = RTextList(m1, m2, m3)
            send_player(server, info, m4)
        elif args[2] == 'boosbar':
            if args[3] in ['1', '2']:
                config['boosbar'] = int(args[3])
                say(server, '[§b' + PluginName + '§r] §6设置语言 / Set language : ' + config['language'], info, True)
                say(server, '[§b' + PluginName + '§r] §6PIP命令 / PIP command : ' + config['pip'], info, True)
                if config['source'] != 1:
                    say(server, '[§b' + PluginName + '§r] §6下载源 / download source : 国内源', info, True)
                else:
                    say(server, '[§b' + PluginName + '§r] §6下载源 / download source : 国外源', info, True)
                if config['boosbar'] == 1:
                    say(server, '[§b' + PluginName + '§r] §6是否启用进度条 / Enable progress bar or not : True(鸽了', info, True)
                else:
                    say(server, '[§b' + PluginName + '§r] §6是否启用进度条 / Enable progress bar or not : False(鸽了', info, True)
                say(server, '[§b' + PluginName + '§r] §6正在下载语言文件 / Downloading language file', info, True)
                if save_file(mconfig + config['language'] + '.yml', get_lang()):
                    say(server, '[§b' + PluginName + '§r] §6保存成功 / Save failed', info, True)
                else:
                    say(server, '[§b' + PluginName + '§r] §6保存失败 / Save failed', info, True)
                    return
                say(server, '[§b' + PluginName + '§r] §6正在保存配置文件 / Saving profile', info, True)
                if save_config():
                    say(server, '[§b' + PluginName + '§r] §6保存成功 / Saved successfully', info, True)
                else:
                    say(server, '[§b' + PluginName + '§r] §6保存失败 / Save failed', info, True)
                    return


def download(link, server, info, filename=None):
    server.reply(info, '[§b' + PluginName + '§r] 正在尝试连接')
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        file = requests.get(link, stream=True, timeout=(10, 27), headers=headers)
        try:
            length = round(int(file.headers['Content-Length']) / 1024, 2)
        except:
            length = '∞'
        if not filename:
            if 'Content-Disposition' in file.headers:
                filename = re.findall(
                    r'filename=(.+)', file.headers['Content-Disposition'])
                if filename:
                    filename = unquote(filename[0])
                    if filename.startswith(' '):
                        filename = filename[1:]
                else:
                    filename = os.path.basename(link)
            else:
                filename = os.path.basename(link)
        file_path = os.path.join('plugins', filename)
        server.reply(info, f'[§b' + PluginName + '§r] 正在下载 §b{filename} §6({length}KB)')
        start_time = int(time.time())
        down_size = 0
        with open(f'{file_path}.tmp', 'wb') as fp:
            for chunk in file.iter_content(chunk_size=chunk_size):
                now_time = int(time.time())
                fp.write(chunk)
                down_size += len(chunk)
                u_time = now_time - start_time
                # 若下载时间过长，间隔5秒报告一次
                if u_time >= 5:
                    server.say(
                        f'[§b' + PluginName + '§r Downloading §b{filename} §6{round(down_size / 1024, 2)}KB ({round(down_size / 1024 / u_time, 2)}KB/s)]')
                    start_time = int(time.time())
                    down_size = 0
    except requests.exceptions.ConnectTimeout:
        server.reply(info, '[§b' + PluginName + '§r] §c错误：连接超时')
        return False
    except requests.exceptions.ConnectionError:
        server.reply(info, '[§b' + PluginName + '§r] §c错误：连接失败')
        return False

    if os.path.isfile(file_path):
        server.reply(info, '[§b' + PluginName + '§r] §c警告：发现旧文件已存在，将会被覆盖')
        os.remove(file_path)
    os.rename(f'{file_path}.tmp', file_path)
    server.reply(info, f'[§b' + PluginName + '§r] §b{filename} 下载完成')
    if getsys() != 'windows':
        os.system('chmod +x ' + ppath + filename)
    return True
