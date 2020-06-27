import urllib.request
import json
import re
import time
import os

# GitHub Token
# Get Token https://github.com/settings/tokens
token = ''
debug_mode = False

if not os.path.exists(os.path.join('.','plugin')):
    os.mkdir(os.path.join('.','plugin'))
def down1(url) -> str:
    try:
        get = str(urllib.request.urlopen(url).read().decode())
        a = url.split('/')
        if len(a[len(a) - 1].split('?')) >= 2:
            name = a[len(a) - 1].split('?')[0]
        else:
            name = a[len(a) - 1]
        fo = open(os.path.join('.','plugin',name), 'w', encoding='utf-8')
        fo.write(get)
        fo.close()
        return get
    except Exception as error:
        print('get error: ',error)
        return down1(url)

def getmidstring(html, start_str, end) -> str:
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

def trim(s):
    if s[0] == " ":
        return trim(s[1:])
    elif s[-1] == " ":
        return trim(s[:-1])
    else:
        return s

def imurl(url):
    print('\nUrl: ',url,'\n')
    raw_url = ''
    while True:
        if raw_url != '':
            ok = input('\nurl: ' + raw_url + ' ok?[Y,N]\n')
            if ok in ['y','Y']:
                break
            elif ok in ['n','N']:
                raw_url = ''
            else:
                print('\nInput error\n')
        else:
            raw_url = input('\nInput Raw Url\n')
    return raw_url


def json_if(name):
    a = open(os.path.join('.','plugin','dy.json'))
    js = json.loads(a.read())
    a.close()
    return js.get(name,'')




pip = ['requests','Flask','requests','*','Enum','enum','deepcopy','flask','queueasQueue','Decimal','ROUND_HALF_UP','mcrcon','bypy','tool','Lock','constant','TitleAPI','daycount','ChatBridgeLibrary','Empty','Queue','Timer','timer','Thread','run','Popen','PIPE','RStyle','pathlib','RTextList','ruamel','RColor','RAction','RText','request','parse','__future__','rtext','config','plugins','utils','string', 're', 'difflib', 'textwrap', 'unicodedata', 'stringprep', 'readline', 'rlcompleter', 'struct', 'codecs', 'datetime', 'calendar', 'collections', 'collections.abc', 'heapq', 'bisect', 'array', 'weakref', 'types', 'copy', 'pprint', 'reprlib', 'numbers', 'math', 'cmath', 'decimal', 'fractions', 'random', 'itertools', 'functools', 'operator', 'os.path', 'fileinput', 'stat', 'filecmp', 'tempfile', 'glob', 'fnmatch', 'linecache', 'shutil', 'macpath', 'pickle', 'copyreg', 'shelve', 'marshal', 'dbm', 'sqlite3', 'zlib', 'gzip', 'bz2', 'lzma', 'zipfile', 'tarfile', 'csv', 'configparser', 'netrc', 'xdrlib', 'plistlib', 'hashlib', 'hmac', 'os', 'io', 'time', 'argparser', 'optparser', 'getopt', 'logging', 'logging.config', 'logging.handlers', 'getpass', 'curses', 'curses.textpad', 'curses.ascii', 'curses.panel', 'platform', 'errno', 'ctypes', 'threading', 'multiprocessing', 'concurrent', 'concurrent.futures', 'subprocess', 'sched', 'queue', 'select', 'dummy_threading', '_thread', '_dummy_thread', 'socket', 'ssl', 'asyncore', 'asynchat', 'signal', 'mmap', 'email', 'json', 'mailcap', 'mailbox', 'mimetypes', 'base64', 'binhex', 'binascii', 'quopri', 'uu', 'html', 'html.parser', 'html.entities', 'xml', 'xml.etree.ElementTree', 'xml.dom', 'xml.dom.minidom', 'xml.dom.pulldom', 'xml.sax', 'xml.sax.handler', 'xml.sax.saxutils', 'xml.sax.xmlreader', 'xml.parsers.expat', 'webbrowser', 'cgi', 'cgitb', 'wsgiref', 'urllib', 'urllib.request', 'urllib.response', 'urllib.parse', 'urllib.error', 'urllib.robotparser', 'http', 'http.client', 'ftplib', 'poplib', 'imaplib', 'nntplib', 'smtplib', 'smtpd', 'telnetlib', 'uuid', 'socketserver', 'http.server', 'http.cookies', 'http.cookiejar', 'xmlrpc', 'xmlrpc.client', 'xmlrpc.server', 'ipaddress', 'audioop', 'aifc', 'sunau', 'wave', 'chunk', 'colorsys', 'imghdr', 'sndhdr', 'ossaudiodev', 'gettext', 'locale', 'turtle', 'cmd', 'shlex', 'tkinter', 'tkinter.ttk', 'tkinter.tix', 'tkinter.scrolledtext', 'pydoc', 'doctest', 'unittest', 'unittest.mock', 'test', 'test.support', 'venv', 'bdb', 'faulthandler', 'pdb', 'timeit', 'trace', 'sys', 'sysconfig', 'builtins', 'main', 'warnings', 'contextlib', 'abc', 'atexit', 'traceback', 'future', 'gc', 'inspect', 'site', 'fpectl', 'distutils', 'code', 'codeop', 'imp', 'zipimport', 'pkgutil', 'modulefinder', 'runpy', 'importlib', 'parser', 'ast', 'symtable', 'symbol', 'token', 'keyword', 'tokenize', 'tabnany', 'pyclbr', 'py_compile', 'compileall', 'dis', 'pickletools', 'formatter', 'msilib', 'msvcrt', 'winreg', 'winsound', 'posix', 'pwd', 'spwd', 'grp', 'crypt', 'termios', 'tty', 'pty', 'fcntl', 'pipes', 'resource', 'nis', 'syslog']
nr = {'name':'','remarks_cn':'','remarks':'','raw_url_cn':'','raw_url':'','lib':[],'pip_lib':[],'file':'','author':'','url':'','class':'','subclass':'','class_cn':'','subclass_cn':''}
data = {'time':0,'list':[],'api_list':[]}


print('\nGet Readme!\n')


en = down1('https://raw.githubusercontent.com/MCDReforged-Plugins/PluginCatalogue/master/readme.md?access_token=' + token)
ch = down1('https://raw.githubusercontent.com/MCDReforged-Plugins/PluginCatalogue/master/readme_cn.md?access_token=' + token)


print('\nStart init Readme!\n')


# json_de = down1('https://raw.githubusercontent.com/Squaregentleman/MCDR-get/master/list.json')
# json_de = json.loads(json_de)
n = 0
clss = []
nrn = []
debug = []
for i in en.split('|'):
    if n == 1:
        if not i.replace(' ','') in ['Name','Maintainer','Function']:
            if i.find('##') >= 0:
                m = i.split('\n')
                for r in m:
                    if r != '':
                        if r[:3] == '###':
                            clss[1] = r.replace('#','').replace(' ','')
                        else:
                            clss[0] = r.replace('#','').replace(' ','')
                            clss[1] = ''
                if debug_mode:
                    print('\nclass: ',clss)
                debug.append(clss)
            else:
                if not i.replace(' ','').find('----------------------') >= 0:
                    if debug_mode:
                        print('\nprint: ',i)
                    debug.append(i)
                    if i != '\n':
                        if clss[0] == 'API':
                            ia = i.replace('\n','').replace('\r','').replace(' ','')
                            debug.append('ia : ' + ia)
                            if ia != '':
                                if not i.replace(' ','') in ['##','###']:
                                    nrn.append(i)
                                if len(nrn) == 3:
                                    nr['name'] = getmidstring(nrn[0].replace(' ',''),'[',']')
                                    nr['url'] = getmidstring(nrn[0].replace(' ',''),'(',')')
                                    if nrn[1].count('[') == 1:
                                        nr['author'] = getmidstring(nrn[1].replace(' ',''),'[',']')
                                    else:
                                        ins = 0
                                        cow = 0
                                        nr['author'] = getmidstring(nrn[1].replace(' ',''),'[',']')
                                        while ins >= nrn[1].count('[') - 1:
                                            ins += 1
                                            cow = nrn[1].find('[', cow + 1)
                                            nr['author'] += ',' + getmidstring(nrn[1].replace(' ','')[cow:],'[',']')
                                    nr['remarks'] = trim(nrn[2])
                                    if len(clss) == 2:
                                        nr['class'] = clss[0].replace('#','')
                                        nr['subclass'] = clss[1].replace('#','')
                                    else:
                                        nr['class'] = clss[0].replace('#','')
                                        nr['subclass'] = ''
                                    data['api_list'].append(nr)
                                    if debug_mode:
                                        print('\nprint nrn: ',nrn)
                                    debug.append(nrn)
                                    nr = {'name':'','remarks_cn':'','remarks':'','raw_url_cn':'','raw_url':'','lib':[],'pip_lib':[],'file':'','author':'','url':'','class':'','subclass':'','class_cn':'','subclass_cn':''}
                                    nrn = []
                        else:
                            ia = i.replace('\n','').replace('\r','').replace(' ','')
                            debug.append('ia : ' + ia)
                            if ia != '':
                                if not i.replace(' ','') in ['##','###']:
                                    nrn.append(i)
                                if len(nrn) == 3:
                                    nr['name'] = getmidstring(nrn[0].replace(' ',''),'[',']')
                                    nr['url'] = getmidstring(nrn[0].replace(' ',''),'(',')')
                                    if nrn[1].count('[') == 1:
                                        nr['author'] = getmidstring(nrn[1].replace(' ',''),'[',']')
                                    else:
                                        ins = 0
                                        cow = 0
                                        nr['author'] = getmidstring(nrn[1].replace(' ',''),'[',']')
                                        while ins >= nrn[1].count('[') - 1:
                                            ins += 1
                                            cow = nrn[1].find('[', cow + 1)
                                            nr['author'] += ',' + getmidstring(nrn[1].replace(' ','')[cow:],'[',']')
                                    nr['remarks'] = trim(nrn[2])
                                    if len(clss) == 2:
                                        nr['class'] = clss[0].replace('#','')
                                        nr['subclass'] = clss[1].replace('#','')
                                    else:
                                        nr['class'] = clss[0].replace('#','')
                                        nr['subclass'] = ''
                                    data['list'].append(nr)
                                    if debug_mode:
                                        print('\nprint nrn: ',nrn)
                                    debug.append(nrn)
                                    nr = {'name':'','remarks_cn':'','remarks':'','raw_url_cn':'','raw_url':'','lib':[],'pip_lib':[],'file':'','author':'','url':'','class':'','subclass':'','class_cn':'','subclass_cn':''}
                                    nrn = []
    else:
        if debug_mode:
            print('not print: ' + i)
        if n != 1:
            m = i.split('--------')[1].split('\n')
            for r in m:
                if r != '':
                    clss.append(r.replace('#','').replace(' ',''))
            if debug_mode:
                print('\nclass: ',clss)
            debug.append(clss)
        n = 1

for i in ch.split('|'):
    if n == 1:
        if not i.replace(' ','') in ['名称','维护者','功能']:
            if i.find('##') >= 0:
                m = i.split('\n')
                for r in m:
                    if r != '':
                        if r[:3] == '###':
                            clss[1] = r.replace('#','').replace(' ','')
                        else:
                            clss[0] = r.replace('#','').replace(' ','')
                            clss[1] = ''
                if debug_mode:
                    print('\nclass: ',clss)
                debug.append(clss)
            else:
                if not i.replace(' ','').find('----------------------') >= 0:
                    if debug_mode:
                        print('\nprint: ',i)
                    debug.append(i)
                    if i != '\n':
                        if clss[0] == 'API':
                            ia = i.replace('\n','').replace('\r','').replace(' ','')
                            debug.append('ia : ' + ia)
                            if ia != '':
                                if not i.replace(' ','') in ['##','###']:
                                    nrn.append(i)
                                if len(nrn) == 3:
                                    for line in data['api_list']:
                                        if line['name'] == getmidstring(nrn[0].replace(' ',''),'[',']'):
                                            line['remarks_cn'] = trim(nrn[2])
                                            if len(clss) == 2:
                                                line['class_cn'] = clss[0].replace('#','')
                                                line['subclass_cn'] = clss[1].replace('#','')
                                            else:
                                                line['class_cn'] = clss[0].replace('#','')
                                                line['subclass_cn'] = ''
                                            if debug_mode:
                                                print('\nprint nrn: ',nrn)
                                            debug.append(nrn)
                                            nrn = []
                                            break
                        else:
                            ia = i.replace('\n','').replace('\r','').replace(' ','')
                            debug.append('ia : ' + ia)
                            if ia != '':
                                if not i.replace(' ','') in ['##','###']:
                                    nrn.append(i)
                                if len(nrn) == 3:
                                    for line in data['list']:
                                        if line['name'] == getmidstring(nrn[0].replace(' ',''),'[',']'):
                                            line['remarks_cn'] = trim(nrn[2])
                                            if len(clss) == 2:
                                                line['class_cn'] = clss[0].replace('#','')
                                                line['subclass_cn'] = clss[1].replace('#','')
                                            else:
                                                line['class_cn'] = clss[0].replace('#','')
                                                line['subclass_cn'] = ''
                                            if debug_mode:
                                                print('\nprint nrn: ',nrn)
                                            debug.append(nrn)
                                            nrn = []
                                            break
    else:
        if debug_mode:
            print('not print: ' + i)
        if n != 1:
            m = i.split('--------')[1].split('\n')
            for r in m:
                if r != '':
                    clss.append(r.replace('#','').replace(' ',''))
            if debug_mode:
                print('\nclass: ',clss)
            debug.append(clss)
        n = 1


print('\nGet Url!\n')


for line in data['list']:
    url = line['url'].split('/')
    if len(url) > 6:
        print('get:', line['url'])
        js_en = down1('https://api.github.com/repos/' + url[3] + '/' + url[4] + '/contents?access_token=' + token + '&ref=' + url[6])
        js = json.loads(js_en)
        for lin in js:
            if lin['name'][:-3].lower() == line['name'].lower():
                line['raw_url_cn'] = lin['download_url']
                line['raw_url'] = lin['download_url']
                line['file'] = lin['name']
                time.sleep(1)
                break
    else:
        print('get:', line['url'])
        js_en = down1('https://api.github.com/repos/' + url[3] + '/' + url[4] + '/contents?access_token=' + token)
        js = json.loads(js_en)
        for lin in js:
            if lin['name'][:-3].lower() == line['name'].lower():
                line['raw_url_cn'] = lin['download_url']
                line['raw_url'] = lin['download_url']
                line['file'] = lin['name']
                time.sleep(1)
                break

for line in data['api_list']:
    url = line['url'].split('/')
    if len(url) > 6:
        print('get:', line['url'])
        js_en = down1('https://api.github.com/repos/' + url[3] + '/' + url[4] + '/contents?access_token=' + token + '&ref=' + url[6])
        js = json.loads(js_en)
        for lin in js:
            if lin['name'][:-3].lower() == line['name'].lower():
                line['raw_url_cn'] = lin['download_url']
                line['raw_url'] = lin['download_url']
                line['file'] = lin['name']
                time.sleep(1)
                break
    else:
        print('get:', line['url'])
        js_en = down1('https://api.github.com/repos/' + url[3] + '/' + url[4] + '/contents?access_token=' + token)
        js = json.loads(js_en)
        for lin in js:
            if lin['name'][:-3].lower() == line['name'].lower():
                line['raw_url_cn'] = lin['download_url']
                line['raw_url'] = lin['download_url']
                line['file'] = lin['name']
                time.sleep(1)
                break


print('\nGet Lib List!\n')


for line in data['list']:
    if line['raw_url'] != '':
        print('get:', line['raw_url'])
        py = down1(line['raw_url'] + '?access_token=' + token)
        fom = re.findall('from.*import.*',py)
        if len(fom) >= 1:
            for lin in fom:
                for li in data['api_list']:
                        if py.find(li['file'][:-3]) >= 0:
                            if not li['name'] in line['lib']:
                                line['lib'].append(li['name'])
                            break
                        for sr in re.findall('^from (?:(?:[^\s]*\.)*)?([^\s.]+) import .*$',lin):
                            if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                                py = py.replace(lin,'')
                                if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in line['pip_lib']:
                                    line['pip_lib'].append(sr.replace('\r','').replace('\n','').replace('import ','').replace(' ',''))
                                break
                        
        fom = re.findall('import .*,.*',py)
        if len(fom) >= 1:
            for lin in fom:
                for li in data['api_list']:
                    l = lin.split(',')
                    for a in l:
                        if not py.find(li['file'][:-3]) >= 0:
                            if not a.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                                sr = a.replace('\r','').replace('\n','').replace('import ','').replace(' ','')
                                if not sr in line['pip_lib']:
                                    line['pip_lib'].append(sr)
                        else:
                            if not li['name'] in line['lib']:
                                line['lib'].append(li['name'])
                    py = py.replace(lin,'')
        im = re.findall('import.*',py)
        for lin in im:
            for li in data['api_list']:
                if py.find(li['file'][:-3]) >= 0:
                    if not li['name'] in line['lib']:
                        line['lib'].append(li['name'])
                    break
                for sr in re.findall('^from (?:(?:[^\s]*\.)*)?([^\s.]+) import .*$',lin):
                    if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                        py = py.replace(lin,'')
                        if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in line['pip_lib']:
                            line['pip_lib'].append(sr.replace('\r','').replace('\n','').replace('import ','').replace(' ',''))
                        break
        for li in data['api_list']:
            if py.find(li['file'][:-3]) >= 0:
                if not li['name'] in line['lib']:
                    line['lib'].append(li['name'])
        time.sleep(1)
    else:
        urlr = json_if(line['name'])
        if urlr == '':
            line['raw_url'] = imurl(line['url'])
        else:
            line['raw_url'] = urlr
        print('get:', line['raw_url'])
        py = down1(line['raw_url'] + '?access_token=' + token)
        fom = re.findall('from.*import.*',py)
        if len(fom) >= 1:
            for lin in fom:
                for li in data['api_list']:
                        if py.find(li['file'][:-3]) >= 0:
                            if not li['name'] in line['lib']:
                                line['lib'].append(li['name'])
                            break
                        for sr in re.findall('^from (?:(?:[^\s]*\.)*)?([^\s.]+) import .*$',lin):
                            if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                                py = py.replace(lin,'')
                                if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in line['pip_lib']:
                                    line['pip_lib'].append(sr.replace('\r','').replace('\n','').replace('import ','').replace(' ',''))
                                break
                        
        fom = re.findall('import .*,.*',py)
        if len(fom) >= 1:
            for lin in fom:
                for li in data['api_list']:
                    l = lin.split(',')
                    for a in l:
                        if not py.find(li['file'][:-3]) >= 0:
                            if not a.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                                sr = a.replace('\r','').replace('\n','').replace('import ','').replace(' ','')
                                if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in line['pip_lib']:
                                    line['pip_lib'].append(sr.replace('\r','').replace('\n','').replace('import ','').replace(' ',''))
                        else:
                            if not li['name'] in line['lib']:
                                line['lib'].append(li['name'])
                    py = py.replace(lin,'')
        im = re.findall('import.*',py)
        for lin in im:
            for li in data['api_list']:
                if py.find(li['file'][:-3]) >= 0:
                    if not li['name'] in line['lib']:
                        line['lib'].append(li['name'])
                    break
                for sr in re.findall('^from (?:(?:[^\s]*\.)*)?([^\s.]+) import .*$',lin):
                    if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                        py = py.replace(lin,'')
                        if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in line['pip_lib']:
                            line['pip_lib'].append(sr.replace('\r','').replace('\n','').replace('import ','').replace(' ',''))
                        break
                # elif not lin.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                #     sr = lin
                #     py = py.replace(lin,'')
                #     sr = re.findall('^from (?:(?:[^\s]*\.)*)?([^\s.]+) import .*$',lin)
                #     line['pip_lib'].append(sr)
                #     break
        for li in data['api_list']:
            if py.find(li['file'][:-3]) >= 0:
                if not li['name'] in line['lib']:
                    line['lib'].append(li['name'])
        time.sleep(1)


print('\nGet Api Lib List!\n')


for line in data['api_list']:
    if line['raw_url'] != '':
        print('get:', line['raw_url'])
        py = down1(line['raw_url'] + '?access_token=' + token)
        fom = re.findall('from.*import.*',py)
        if len(fom) >= 1:
            for lin in fom:
                for li in data['api_list']:
                    for sr in re.findall('^from (?:(?:[^\s]*\.)*)?([^\s.]+) import .*$',lin):
                        if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                            py = py.replace(lin,'')
                            if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in line['pip_lib']:
                                line['pip_lib'].append(sr.replace('\r','').replace('\n','').replace('import ','').replace(' ',''))
                            break
        fom = re.findall('import .*,.*',py)
        if len(fom) >= 1:
            for lin in fom:
                for li in data['api_list']:
                    l = lin.split(',')
                    for a in l:
                        if not a.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                            sr = a.replace('\r','').replace('\n','').replace('import ','').replace(' ','')
                            if not sr in line['pip_lib']:
                                line['pip_lib'].append(sr)
                    py = py.replace(lin,'')
        im = re.findall('import.*',py)
        for lin in im:
            if not lin.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in line['pip_lib']:
                    line['pip_lib'].append(lin.replace('\r','').replace('\n','').replace('import ','').replace(' ',''))
        time.sleep(1)
    else:
        urlr = json_if(line['name'])
        if urlr == '':
            line['raw_url'] = imurl(line['url'])
        else:
            line['raw_url'] = urlr
        print('get:', line['raw_url'])
        py = down1(line['raw_url'] + '?access_token=' + token)
        fom = re.findall('from.*import.*',py)
        if len(fom) >= 1:
            for lin in fom:
                for li in data['api_list']:
                    for sr in re.findall('^from (?:(?:[^\s]*\.)*)?([^\s.]+) import .*$',lin):
                        if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                            py = py.replace(lin,'')
                            if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in line['pip_lib']:
                                line['pip_lib'].append(sr.replace('\r','').replace('\n','').replace('import ','').replace(' ',''))
                            break
        fom = re.findall('import .*,.*',py)
        if len(fom) >= 1:
            for lin in fom:
                for li in data['api_list']:
                    l = lin.split(',')
                    for a in l:
                        if not a.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                            sr = a.replace('\r','').replace('\n','').replace('import ','').replace(' ','')
                            if not sr in line['pip_lib']:
                                line['pip_lib'].append(sr)
                    py = py.replace(lin,'')
        im = re.findall('import.*',py)
        for lin in im:
            if not lin.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in pip:
                if not sr.replace('\r','').replace('\n','').replace('import ','').replace(' ','') in line['pip_lib']:
                    line['pip_lib'].append(lin.replace('\r','').replace('\n','').replace('import ','').replace(' ',''))
        time.sleep(1)


print('\nInput list air raw\n')


for line in data['list']:
    if line['raw_url'] == '':
        print('\nurl: ',line['url'],'\n')
        raw_url = ''
        while raw_url != '':
            if raw_url != '':
                ok = input('url: ' + raw_url + ' ok?[Y,N]')
                if ok in ['y','Y']:
                    line['raw_url'] = raw_url
                    break
                elif ok in ['n','N']:
                    raw_url = ''
                else:
                    print('Input error')
            else:
                raw_url = input('Input Raw Url')


print('\nInput api_list air raw\n')


for line in data['api_list']:
    if line['raw_url'] == '':
        print('\nurl: ',line['url'],'\n')
        raw_url = ''
        while raw_url != '':
            if raw_url != '':
                ok = input('url: ' + raw_url + ' ok?[Y,N]')
                if ok in ['y','Y']:
                    line['raw_url'] = raw_url
                    break
                elif ok in ['n','N']:
                    raw_url = ''
                else:
                    print('input error')
            else:
                raw_url = input('Input Raw Url')

data['time'] = int(time.time())

fo = open("list.json", "w")
fo.write(str(json.dumps(data)))
fo.close()
if debug_mode:
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n',debug)
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n',json.dumps(data),'\n\nsave list.json!')
