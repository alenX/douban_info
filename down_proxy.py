# -*- coding: utf-8 -*-
import requests, datetime
from bs4 import BeautifulSoup

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': 'gzip',
}


def down_load_proxy():
    ll = []
    is_retry = True
    with open('proxy.txt', 'r') as pr:
        for i in pr:
            if i[:-1] == datetime.datetime.now().strftime('%x'):  # 每天只更新一次
                is_retry = False
                continue
            ll.append(i[:-1])
    pr.close()
    if not is_retry:
        return ll
    else:
        ll = []
    with open('proxy.txt', 'w') as of:
        of.write('%s\n' % (datetime.datetime.now().strftime('%x')))
        for page in range(2, 3):
            url = 'http://www.xicidaili.com/nn/%s' % page
            doc = requests.get(url, headers=headers, timeout=5).text
            soup = BeautifulSoup(doc, "html.parser")
            trs = soup.find('table', {"id": "ip_list"}).findAll('tr')
            # print(trs[1:][0].findAll('td')[5])
            # print(trs[1:][0].findAll('td')[1])
            # print(trs[1:][0].findAll('td')[2])
            for tr in trs[1:]:
                tds = tr.findAll('td')
                ip = tds[1].text.strip()
                port = tds[2].text.strip()
                protocol = tds[5].text.strip()
                if protocol == 'HTTP' and get_useful_ip(ip + ":" + port):  # or protocol == 'HTTPS'
                    of.write('%s=%s:%s\n' % (protocol, ip, port))
                    of.flush()
                    ll.append('%s=%s:%s' % (protocol, ip, port))
        of.close()
        return ll


def get_useful_ip(ip):
    try:
        c = requests.get('https://www.baidu.com/', headers=headers, proxies={'http': ip})
        if c.status_code != 200:
            return False
        else:
            return True
    except:
        return False
