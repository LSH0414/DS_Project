import requests
from bs4 import BeautifulSoup

import re


def get_proxy_list():
    url = 'http://spys.one/en/free-proxy-list/'
    data = {
        'xpp' : '1',
        'xf1' : '0',
        'xf2' : '0',
        'xf4' : '0',
        'xf5' : '2'
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    r = requests.post(url, data=data, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    result = []

    ports = {}
    script = soup.select_one('body > script')
    for row in script.text.split(';'):
        if '^' in row:
            line = row.split('=')
            ports[line[0]]  = line[1].split('^')[0]

    trs = soup.select('tr[onmouseover]')
    for tr in trs:

        is_http = tr.select_one('a')

        if is_http is not None:
            http = is_http.text
#             print(is_http.text)

        e_ip = tr.select_one('font.spy14')
#         print(e_ip)
        ip = ''

        e_port = tr.select_one('script')
        port = ''
        if e_port is not None:
            re_port = re.compile(r'\(([a-zA-Z0-9]+)\^[a-zA-Z0-9]+\)')
            match = re_port.findall(e_port.text)
            for item in match:
                port = port + ports[item]
        else:
            continue

        if e_ip is not None:
            for item in e_ip.findAll('script'):
                item.extract()
            ip = e_ip.text

        else:
            continue

        tds = tr.select("td")
        is_skip = False
        for td in tds:
            e_pct = td.select_one('font > acronym')
            if e_pct is not None:
                pct = re.sub('([0-9]+)%.*', r'\1', e_pct.text)
                if not pct.isdigit():
                    is_skip = True
            else:
                continue

        if not pct.isdigit():
            continue

        result.append((http,ip + ':' + port, pct))

    result.sort(key = lambda element  : int(element[2]), reverse=True)

    return result