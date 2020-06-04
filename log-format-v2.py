import re
import datetime
import os

par = '''(?P<ip>[\d\.]{7,})\s-\s-\s\[(?P<datetime>[^\[\]]+)\]\s"(?P<method>[\w]+)\s(?P<url>[\S]+)\s(?P<protocol>[\S]+)"\s(?P<status>[\d]{3})\s(?P<size>[\d]+)\s"(?P<referer>[\S]+)"\s"(?P<useragent>.*)"'''
# url = '''37.9.113.21 - - [02/May/2017:10:21:25 +0800] "GET /job/index.php?c=search&provinceid=28 HTTP/1.1" 200 239 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"'''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(BASE_DIR, 'acc')
options = {'datetime': lambda dater: datetime.datetime.strptime(dater, '%d/%b/%Y:%H:%M:%S %z'),
           'status':int,
           'size': int}
# d={}
def extract(url):
    com = re.compile(par)
    dats = re.match(com, url)
    if dats:
        # for name, data in dats.groupdict().items():
        #     d[name] = options.get(name, lambda x: x)(data)
        d = {name:options.get(name, lambda x: x)(data) for name, data in dats.groupdict().items()}
        return d
def load(file):
    with open(file, 'r') as f:
        for url in f:
            extract(url)

