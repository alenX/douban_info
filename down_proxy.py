# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': 'gzip',
    }


def down_load_proxy():
    ll = []
    with open('proxy.txt', 'w') as of:
        for page in range(1, 2):
            url = 'http://www.xicidaili.com/nn/%s' % page
            doc = requests.get(url, headers=headers).text
            soup = BeautifulSoup(doc,"html.parser")
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
                    ll.append(ip + ":" + port)
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
