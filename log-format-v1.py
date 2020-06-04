import datetime

line = '''37.9.113.21 - - [02/May/2017:10:21:25 +0800] "GET /robots.txt HTTP/1.1" 200 239 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"'''

CHAR = " \t"
def mok(key:str):
    start = 0
    skip = False
    for i, c in enumerate(key):
        if not skip and c in '"[':
            start = i+1
            skip = True
        elif skip and c in '"]':
            skip = False
            yield key[start:i]
            start  = i+1
            continue
        if skip:
            continue
        if c in CHAR:
            # 当start和i都指向一个空格或tab时，跳过
            if start == i:
                start = i+1
                continue
            yield key[start:i]
            start = i+1
    else:
        if start < len(key):
            yield line[start:]

# ['37.9.113.21', '-', '-', '02/May/2017:10:21:25 +0800', 'GET /robots.txt HTTP/1.1', '200', '239', '-', 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)']
# print(list(mok(line)))

# 时间转换
# dates = datetime.datetime.strptime(list(mok(line))[3], '%d/%b/%Y:%H:%M:%S %z')

names = ['remote', '-', '-', 'datetime', 'protocol', 'status', 'size', '-', 'useragent']
ops = (None, None, None,
       lambda datestr: datetime.datetime.strptime(datestr, '%d/%b/%Y:%H:%M:%S %z'),
       lambda x: dict(zip(('method', 'url', 'protocol'), x.split())), # 将'GET /robots.txt HTTP/1.1'拆分
       int, int, None, None)

def extract():
    datas = {name:data if op is None else op(data) for name,op,data in zip(names, ops, mok(line))}
    return datas


