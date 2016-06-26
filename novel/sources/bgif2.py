#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from .. import serial, utils

BASE_URL = 'http://2bgif.com/chapters/{}'


class Bgif2(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         None, '#description',
                         chap_sel='tbody td',
                         chap_type=serial.ChapterType.path,
                         tid=tid)

    def get_title_and_author(self):
        st = self.doc('title').text()
        pat = re.compile(r'(\w+)\s+-\s+(\w+)\s+', re.U)
        return re.match(pat, st).groups()
