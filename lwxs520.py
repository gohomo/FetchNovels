#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.lwxs520.com/books/{}/{}/'
INTRO_URL = 'http://www.lwxs520.com/book/{}/'
ENCODING = 'GB18030'


class Lwxs520Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend((
            re.compile(r'www\.lwxs520\.com 首发哦亲', re.I),
            re.compile(r'乐文小说网'),
            re.compile(r'乐文 小说'),
            re.compile(r'www\.lwxs520\.com'),
        ))


class Lwxs520(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         utils.base_to_url(INTRO_URL, tid), '.intro',
                         const.HEADERS, proxies, ENCODING,
                         tool=Lwxs520Tool,
                         chap_sel='.bookinfo_td td',
                         chap_type=serial.ChapterType.last)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'author'
        ).attr('content')
        return re.match(r'(.*)版权属于作者(.*)', st).groups()

    @property
    def chapter_list(self):
        clist = self.doc(self.chap_sel).filter(
            lambda i, e: Pq(e)('a').attr('href')
        ).map(
            lambda i, e: (i,
                          urljoin(self.url, Pq(e)('a').attr('href')),
                          self.simple_refine(Pq(e).text()))
        )
        return clist

    @staticmethod
    def simple_refine(text):
        text = re.sub(re.compile(r'www\.lwxs520\.com', re.I), '', text)
        text = re.sub(re.compile(r'乐文小说网'), '', text)
        return text


def main():
    utils.in_main(Lwxs520, const.GOAGENT)


if __name__ == '__main__':
    main()
