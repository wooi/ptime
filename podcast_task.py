#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

import requests
from bs4 import BeautifulSoup

from inser_item import *

home_index = ["5", "87", "sitdowncomedy"]

page_link = 'http://www.passiontimes.hk'


def get_detail(url_address, prog):
    for url in url_address:
        channel_response = requests.get(url, timeout=60)
        channel_html = channel_response.content.decode("utf8", "ignore").encode("utf", "ignore")
        channel_content = BeautifulSoup(channel_html, "html.parser", from_encoding='utf-8')

        detail_title = channel_content.find('meta', attrs={'property': 'og:title'})['content']
        detail_info = channel_content.find('h4', attrs={'class': 'byline'})
        author = detail_info.find('span', attrs={'class': 'host'}).a.string
        date = detail_info.find('time', attrs={'class': 'published'})['datetime']
        print(str(detail_title) + str(author) + str(date), end='\n')

        if u'黃洋達' not in author:
            print('PASS, The author does not include 黃洋達 ', end='\n')
            continue

        # download link
        scripts = channel_content.find_all("script")
        for script in scripts:
            content = script.string
            if content is None:
                continue
            if '.mp3' not in content:
                continue
            lines = content.split(';')
            s_index = 0
            for line in lines:
                if '.mp3' not in line:
                    continue
                download_link = re.findall(r'"(.*?)(?<!\\)"', line)[0]
                s_index += 1
                title_str = detail_title + '-' + str(s_index)
                guid = '{},{},{}'.format(prog, url.split('/')[-1], s_index)
                write2xml(title_str=title_str, link_str=url, guid_str=guid, pubDate_str=date, author_str=author,
                          download_link=download_link)


latest_episode = get_cid()
limit_keys = latest_episode.keys()
for channel_id in home_index:
    latest_index = latest_episode[channel_id]
    print('===================Channel========================')
    print('channelId:', channel_id, ' Latest:', latest_index, end='\n')
    channel_link = page_link + "/prog/{}/".format(channel_id)

    print(channel_link, end='\n')
    page_response = requests.get(channel_link, timeout=60)
    html = page_response.content
    html2 = html.decode("utf8", "ignore").encode("utf", "ignore")
    page_content = BeautifulSoup(html2, "html.parser", from_encoding='utf-8')
    module_array = page_content.find_all('li', attrs={'class': 'progEp-module'})
    urls = []
    for module in module_array:
        title = module.find("h4")
        if title is not None:
            url_index = title.a.get("href")
            last_index = url_index.split('/')[-1]
            if int(last_index) > int(latest_index):
                urls.append(page_link + url_index)
    if len(urls) > 0:
        get_detail(url_address=urls, prog=channel_id)
    else:
        print('Not update', end='\n')
    print('===================End========================\n')

