#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.ttshuba.com/shu/%s/%s/'
INTRO_URL = 'http://www.ttshuba.com/info-%s.html'
ENCODING = 'GB18030'


class Ttshuba(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '.intro', '.zhangjieTXT',
                         const.HEADERS, proxies, ENCODING,
                         chap_sel='dd',
                         chap_type=serial.ChapterType.last)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords').attr('content')
        return re.match(r'(.*)最新章节,(.*?),.*', st).groups()


def main():
    serial.in_main(Ttshuba, const.GOAGENT)


if __name__ == '__main__':
    main()
