#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import json
from xml.etree.ElementTree import ElementTree,Element
from xml_praser import *
import re
from inser_item import *

home_index = ["sitdowncomedy"]
# home_index = ["84"]

page_link = 'http://www.passiontimes.hk'

def get_detail(urls,prog):
    for url in urls:
        channel_link = url
        channel_response = requests.get(channel_link, timeout=60)
        channel_html = channel_response.content.decode("utf8", "ignore").encode("utf", "ignore")
        channel_content = BeautifulSoup(channel_html, "html.parser", from_encoding='utf-8')

        title = channel_content.find('meta',attrs={'property': 'og:title'})['content']
        infos = channel_content.find('h4',attrs={'class': 'byline'})
        author =  infos.find('span',attrs={'class':'host'}).a.string
        date =  infos.find('time',attrs={'class':'published'})['datetime']
        print str(title.encode('utf-8'))+str(author.encode('utf-8'))+str(date.encode('utf-8'))
       
        if u'黃洋達' not in author:
            print str(title.encode('utf-8'))+str(url)+' not 黃洋達 pass'
            continue

        #downlaod link
        scripts = channel_content.find_all("script")
        for script in scripts:
            content =  script.string
            if content is None:
                continue
            if '.mp3' not in content:
                continue
            lines =  content.split(';')
            index = 0
            for line in lines:
                if '.mp3' not in line:
                    continue
                download_link =re.findall(r'"(.*?)(?<!\\)"', line)[0]
                index +=1
                title_str = title+'-'+str(index)
                # guid = prog+","+url.split('/')[-1]+","+index
                guid = '{},{},{}'.format(prog,url.split('/')[-1],index)
                write2xml(title_str=title_str,link_str=url,guid_str=guid,pubDate_str=date,author_str=author,download_link=download_link)    
                print download_link



limit_id =get_cid()
print limit_id
# for index in home_index:
for index in home_index:
    limit = limit_id[index]
    print 'limit:',limit
    home_link = page_link+"/prog/{}/".format(index)
    
    print home_link
    page_response = requests.get(home_link, timeout=60)
    html = page_response.content
    html2 = html.decode("utf8", "ignore").encode("utf", "ignore")
    page_content = BeautifulSoup(html2, "html.parser", from_encoding='utf-8')
    module_array = page_content.find_all('li', attrs={'class': 'progEp-module'})
    urls = []
    for module in module_array:
        title = module.find("h4")
        if title is not None:
            url_index= title.a.get("href")
            last_index = url_index.split('/')[-1]
            # print 'current id:',last_index
            if int(last_index)>int(limit):
                urls.append(page_link+url_index)
    # print urls
    if len(urls) >0:    
        get_detail(urls=urls,prog=index)
    else:
        print 'not update'









