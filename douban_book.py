# -*- coding: utf-8 -*-
import requests, re
import pymysql.cursors
import pymongo
from urllib import parse
from bs4 import BeautifulSoup
from utils import reg_tag, user_agents, headers, get_sql_info
from down_proxy import down_load_proxy
from threading import Thread

url = 'https://book.douban.com/tag/'
auth_reg = '^\([\u4E00-\u9FFF]+\)|\[[\u4E00-\u9FFF]+\]'
infos = get_sql_info()


def get_douban_book_tag():
    tags = []
    book_soup = BeautifulSoup(requests.get(url=url, headers=headers).text, "html.parser")
    for t in book_soup.find_all('a'):
        href = t.get('href')
        if href is not None and reg_tag(href):
            tags.append(href.split('/tag/')[1])
    connection = pymysql.connect(host=infos['host'],
                                 user=infos['user'],
                                 password=infos['password'],
                                 db=infos['database'],
                                 charset=infos['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            for i in tags:
                sql = "INSERT INTO `douban_book_tag` (`tag_name`) VALUES (%s)"
                cursor.execute(sql, (i))
        connection.commit()
    finally:
        connection.close()


def get_douban_book_list(tag_url):  # 解析单页
    tag_list = BeautifulSoup(requests.get(url=tag_url, headers=headers).text, "html.parser")
    books = tag_list.find_all('li', class_="subject-item")
    connection = pymysql.connect(host=infos['host'],
                                 user=infos['user'],
                                 password=infos['password'],
                                 db=infos['database'],
                                 charset=infos['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            reg_price = '元'
            for book in books:
                image = BeautifulSoup(str(book), "html.parser").img.get('src')
                name = BeautifulSoup(str(book), "html.parser").find_all('a')[1].get('title')
                detail = str(BeautifulSoup(str(book), "html.parser").find_all(attrs={"class": "pub"})[0].string).strip()
                author_old = detail.split('/')[0]
                county = ''
                if len(re.compile(auth_reg).findall(author_old)) > 0:
                    county = re.compile(auth_reg).findall(author_old)[0][1:-1]
                author = re.sub(auth_reg, '', author_old).strip()
                i = 1
                translator = ''
                if detail.count('/') != 4 and detail.count('/') != 3:
                    print(detail)
                    break
                if detail.count('/') > 3:  # 说明是外文书籍，有翻译人员
                    i += 1
                    translator = detail.split('/')[1]
                press = detail.split('/')[i]
                data_str = detail.split('/')[i + 1]
                price = re.compile('\d+(.\d+)?').search(re.sub(reg_price, '', detail.split('/')[i + 2])).group(0)
                print('aaaaa' + detail)
                score = 0
                if len(BeautifulSoup(str(book), "html.parser").find_all(attrs={"class": "rating_nums"})) > 0:
                    score = BeautifulSoup(str(book), "html.parser").find_all(attrs={"class": "rating_nums"})[0].string
                description = ''
                if BeautifulSoup(str(book), "html.parser").p is not None:
                    description = BeautifulSoup(str(book), "html.parser").p.string
                sql = 'INSERT INTO `douban_book` (`name`,`author`,`county`,`translator`,`press`,`data_str`,`price`,`score`,`description`,`image`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql,
                               (name, author, county, translator, press, data_str, price, score, description, image))
        connection.commit()
    finally:
        connection.close()


def get_all_book_tags():
    all_tags = []  # 数据库读取所有的标签
    connection = pymysql.connect(host=infos['host'],
                                 user=infos['user'],
                                 password=infos['password'],
                                 db=infos['database'],
                                 charset=infos['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `tag_name` FROM `douban_book_tag` "
            cursor.execute(sql)
            result = cursor.fetchall()
            for r in result:
                all_tags.append(r['tag_name'])
    finally:
        connection.close()
        return all_tags


# proxy = down_load_proxy()


def recycle_get_books():
    threads = []
    all_books = get_all_book_tags()
    for book_tag in all_books:
        t = Douban_Book_Thread(book_tag)
        threads.append(t)
        t.start()
    for th in threads:
        th.join()


class Douban_Book_Thread(Thread):
    def __init__(self, book_tag):
        self.book_tag = book_tag
        super(Douban_Book_Thread, self).__init__()

    def run(self):
        tag_url = url + parse.quote(self.book_tag)
        get_douban_book_list(tag_url)
        start_num = 20
        while True:
            web_url = tag_url + "?start=" + str(start_num) + "&type=T"
            if str(BeautifulSoup(requests.get(web_url).text, "html.parser")).count('没有找到符合条件的图书') > 0:
                break
            get_douban_book_list(web_url)
            start_num += 20


if __name__ == '__main__':
    recycle_get_books()
