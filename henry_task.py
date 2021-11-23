#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from bs4 import NavigableString
import urlparse
from henry_inser_item import *

import requests
import json
from xml.etree.ElementTree import ElementTree, Element
from xml_praser import *
import re
from datetime import datetime

home_index = ["5", "84", "102"]
# home_index = ["84"]

page_link = 'https://www.mihk.tv/channel/index.php?route=mihk/archive&program_id=205'

limit_id = get_cid()

page_response = requests.get(page_link, timeout=60)
html = page_response.content
html2 = html.decode("utf8", "ignore").encode("utf", "ignore")
# print html2
page_content = BeautifulSoup(html2, "html.parser", from_encoding='utf-8')
module_array = page_content.find_all('div', attrs={
    'style': 'marign:0px; line-height:50px; font-size:16px;border-bottom:1px dotted #999999;  border-left:1px solid #00F; padding:0px;'})

h = ''
e = ''
list = []
limit_id = get_cid()

for ii, module in enumerate(module_array):
    div_list = module.contents
    index = 0
    data = {}
    title = ''

    for idx, div in enumerate(div_list):
        if isinstance(div, NavigableString):
            continue

        if index == 0:
            title = div.contents[0]
            data[0] = title
        if index == 2:
            href = div.contents[0].attrs["href"]
            parsed = urlparse.urlparse(href)
            topic_id = urlparse.parse_qs(parsed.query)['topic_id'][0]
            if limit_id < int(topic_id):
                if 'Part 1' in data[0]:
                    data[1] = topic_id
                    new_url = page_link + '&type=audio&topic_id=' + topic_id
                    print new_url
                    page_response2 = requests.get(new_url, timeout=60)
                    h2 = page_response2.content
                    h22 = h2.decode("utf8", "ignore").encode("utf", "ignore")
                    page_content2 = BeautifulSoup(h22, "html.parser", from_encoding='utf-8')
                    download_div = page_content2.find_all("a", href=lambda href: href and "mp3" in href)
                    print download_div
                    download_url = download_div[0]['href']
                    date = re.sub("[^0-9]", "", re.sub(r'^.+/([^/]+)$', r'\1', download_url).split('.mp3')[0])
                    data[2] = date
                    data[3] = download_url
                else:
                    pre_url = list[-1][3]
                    pre_eps = re.sub(r'^.+/([^/]+)$', r'\1', pre_url).split('.mp3')[0]
                    if 'a' in pre_eps:
                        new_download_link = pre_url.replace(pre_eps,pre_eps.replace('a', 'b'))
                    else:
                        new_download_link = pre_url.replace(pre_eps,pre_eps.replace('b', 'c'))
                    data[1] = str(int(list[-1][1])+1)

                    date = re.sub("[^0-9]", "", re.sub(r'^.+/([^/]+)$', r'\1', new_download_link).split('.mp3')[0])
                    data[2] = date
                    data[3] = new_download_link
        index += 1
    list.append(data)

for item in list[::-1]:
    if len(item) == 1:
        continue
    print item
    url = item[3].replace("&amp;e", "&e")
    date = datetime.strptime(item[2], '%Y%m%d').strftime('%Y-%m-%d')

    write2xml(title_str=item[0], link_str=page_link, guid_str=item[1], pubDate_str=date, author_str="henry",
              download_link=url)

replace_str()