# -*- coding: utf-8 -*-
import requests,re
import pymysql.cursors
from bs4 import BeautifulSoup
from utils import reg_tag, user_agents, headers


url = 'https://book.douban.com/tag/'
auth_reg = '^\([\u4E00-\u9FFF]+\)|\[[\u4E00-\u9FFF]+\]'


def get_douban_book_tag():
    tags = []
    book_soup = BeautifulSoup(requests.get(url=url, headers=headers).text, "html.parser")
    for t in book_soup.find_all('a'):
        href = t.get('href')
        if href is not None and reg_tag(href):
            tags.append(href.split('/tag/')[1])
    connection = pymysql.connect(host='localhost',
                                 user='douban',
                                 password='douban',
                                 db='douban',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            for i in tags:
                sql = 'INSERT INTO `douban_book_tag` (`tag_name`) VALUES (%s)'
                cursor.execute(sql, (i))
        connection.commit()
        # with connection.cursor() as cursor:
        #     # Read a single record
        #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        #     cursor.execute(sql, ('webmaster@python.org',))
        #     result = cursor.fetchone()
        #     print(result)
    finally:
        connection.close()


def get_douban_book_list(tag='小说'):
    tag_url = url+tag
    tag_list = BeautifulSoup(requests.get(url=tag_url, headers=headers).text, "html.parser")
    books = tag_list.find_all(attrs={"class": "subject-item"})
    connection = pymysql.connect(host='localhost',
                                 user='douban',
                                 password='douban',
                                 db='douban',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            for book in books:
                image = BeautifulSoup(str(book), "html.parser").img.get('src')
                name = BeautifulSoup(str(book), "html.parser").find_all('a')[1].get('title')
                detail = str(BeautifulSoup(str(book), "html.parser").find_all(attrs={"class": "pub"})[0].string).strip()
                author_old = detail.split('/')[0]
                county=re.compile(auth_reg).findall(author_old)[0][1:-1]
                i = 0
                translator=''
                if detail.count('/') > 3:  # 说明是外文书籍，有翻译人员
                    i += 1
                    translator = detail.split('/')[1]
                press = detail.split('/')[i]
                data_str = detail.split('/')[i + 1]
                price = detail.split('/')[i + 2]
                score = BeautifulSoup(str(book), "html.parser").find_all(attrs={"class": "rating_nums"})[0].string
                description = BeautifulSoup(str(book), "html.parser").p.string
                sql = 'INSERT INTO `douban_book` (`name`,`author`,`county`,`translator`,`press`,`data_str`,`price`,`socre`,`description`,`image`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql, (name,author,name,translator,press,data_str,price,score,description,image))
        connection.commit()
        # with connection.cursor() as cursor:
        #     # Read a single record
        #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        #     cursor.execute(sql, ('webmaster@python.org',))
        #     result = cursor.fetchone()
        #     print(result)
    finally:
        connection.close()





get_douban_book_list()