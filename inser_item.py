#!/usr/bin/python
# -*- coding=utf-8 -*-
import xml.etree.ElementTree as ET

debug = True
from pathlib import Path

xml_path = str(Path.cwd()) + '/ptime.xml'


def indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def read_xml(in_path):
    """读取并解析xml文件
       in_path: xml路径
       return: ElementTree"""
    ET.register_namespace('atom', 'http://www.w3.org/2005/Atom/')
    ET.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')
    ET.register_namespace('dc', 'http://purl.org/dc/elements/1.1/')
    ET.register_namespace('fireside', 'http://fireside.fm/modules/rss/fireside')
    ET.register_namespace('googleplay', 'http://www.google.com/schemas/play-podcasts/1.0')
    ET.register_namespace('itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
    ET.register_namespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    ET.register_namespace('sy', 'ttp://purl.org/rss/1.0/modules/syndication/')
    tree = ET.parse(in_path)
    return tree


def create_node(tag, property_map, content):
    """新造一个节点
       tag:节点标签
       property_map:属性及属性值map
       content: 节点闭合标签里的文本内容
       return 新节点"""
    element = ET.Element(tag, property_map)
    element.text = content
    return element


def create_p_node(tag):
    """新造一个节点
       tag:节点标签
       property_map:属性及属性值map
       content: 节点闭合标签里的文本内容
       return 新节点"""
    element = ET.Element(tag)
    return element


def create_c_node(tag, content):
    """新造一个节点
       tag:节点标签
       property_map:属性及属性值map
       content: 节点闭合标签里的文本内容
       return 新节点"""
    element = ET.Element(tag)
    element.text = content
    return element


#   <item>
#      <title>笑死朕 第422集 - 熱血東遊記1</title>
#      <link>http://www.passiontimes.hk/prog/5/422</link>
#      <guid isPermaLink="false">0e6b7a581b8ef11a66e9ae02824c52e3</guid>
#      <pubDate>Fri, 18 Jan 2019 22:00:00 -0600</pubDate>
#      <author>黃洋達、陳秀慧</author>
#      <enclosure url="http://ptmirror.passiontimes.hk/cache/05/422/king20190215a.mp3" length="31279627" type="audio/mpeg" />
#      <itunes:episodeType>full</itunes:episodeType>
#      <itunes:author>IPN</itunes:author>
#      <itunes:subtitle>黃洋達、陳秀慧-嘉賓：阿薯、謎之音</itunes:subtitle>
#      <itunes:duration>30:00</itunes:duration>
#      <itunes:explicit>no</itunes:explicit>
#      <itunes:image href="http://www.passiontimes.hk/4.0/favicons/android-chrome-192x192.png" />
#      <description>熱血東遊記1-黃洋達、陳秀慧-嘉賓：阿薯、謎之音</description>
#      <content:encoded></content:encoded>
#      <itunes:summary></itunes:summary>
#   </item>
def write2xml(title_str, link_str, guid_str, pubDate_str, author_str, download_link):
    # 1. 读取xml文件
    tree = read_xml(xml_path)
    nodes = tree.getroot().find("channel")
    item = create_p_node("item")

    title = create_c_node("title", title_str)
    link = create_c_node("link", link_str)
    # guid = create_c_node("guid",guid_str)
    guid = ET.Element("guid")
    guid.attrib = {"isPermaLink": "false"}
    guid.text = guid_str
    pubDate = create_c_node("pubDate", pubDate_str)
    author = create_c_node("author", author_str)
    enclosure = ET.Element("enclosure")
    enclosure.attrib = {"url": download_link, "length": "31279627", "type": "audio/mpeg"}
    itunes_episodeType = create_c_node("itunes:episodeType", "full")
    itunes_author = create_c_node("itunes:author", "PT")
    itunes_subtitle = create_c_node("itunes:subtitle", author_str)
    itunes_duration = create_c_node("itunes:duration", "30:00")
    itunes_explicit = create_c_node("itunes:explicit", "no")
    itunes_image = ET.Element("itunes:image")
    itunes_image.attrib = {"href": "http://www.passiontimes.hk/4.0/favicons/android-chrome-192x192.png"}
    description = create_c_node("description", author_str)
    content_encoded = ET.Element("content:encoded")
    itunes_summary = ET.Element("itunes:summary")

    item.append(title)
    item.append(link)
    item.append(guid)
    item.append(pubDate)
    item.append(author)
    item.append(enclosure)
    item.append(itunes_episodeType)
    item.append(itunes_author)
    item.append(itunes_subtitle)
    item.append(itunes_duration)
    item.append(itunes_explicit)
    item.append(itunes_image)
    item.append(description)
    item.append(content_encoded)
    item.append(itunes_summary)

    nodes.insert(18, item)
    indent(nodes)
    # ET.dump(nodes)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    print('Insert,Download Link:', download_link, end='\n')


# channel_map = {"5":"405","85":"731"}
def get_cid():
    channel_map = {}
    tree = read_xml(xml_path)
    nodes = tree.getroot().find("channel")
    items = nodes.findall('item')
    for child in items:
        cid = child.find("guid").text.split(",")
        if cid[0] not in channel_map:
            channel_map[cid[0]] = cid[1]
        else:
            if channel_map[cid[0]] < cid[1]:
                channel_map[cid[0]] = cid[1]
    return channel_map
