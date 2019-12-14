
#!/usr/bin/python
# -*- coding=utf-8 -*-
# author : wklken@yeah.net
# date: 2012-05-25
# version: 0.1
 
from xml.etree.ElementTree import ElementTree,Element
import xml.etree.ElementTree as ET

def read_xml(in_path):
    ET.register_namespace('atom','http://www.w3.org/2005/Atom/')
    ET.register_namespace('content','http://purl.org/rss/1.0/modules/content/')
    ET.register_namespace('dc','http://purl.org/dc/elements/1.1/')
    ET.register_namespace('fireside','http://fireside.fm/modules/rss/fireside')   
    ET.register_namespace('googleplay','http://www.google.com/schemas/play-podcasts/1.0')     
    ET.register_namespace('itunes','http://www.itunes.com/dtds/podcast-1.0.dtd')
    ET.register_namespace('rdf','http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    ET.register_namespace('sy','ttp://purl.org/rss/1.0/modules/syndication/')
    tree = ET.parse(in_path)
    return tree
 
def write_xml(tree, out_path):
    tree.write(out_path, encoding="utf-8",xml_declaration=True)
 
def if_match(node, kv_map):
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True
 
#---------------search -----
 
def find_nodes(tree, path):
    return tree.findall(path)
 
 
def get_node_by_keyvalue(nodelist, kv_map):
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes
 
#---------------change -----
 
def change_node_properties(nodelist, kv_map, is_delete=False):
    for node in nodelist:
        for key in kv_map:
            if is_delete: 
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))
            
def change_node_text(nodelist, text, is_add=False, is_delete=False):
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text
            
def create_node(tag, property_map, content):
    element = Element(tag, property_map)
    element.text = content
    return element

def create_p_node(tag):
    element = Element(tag)
    return element

def create_c_node(tag, content):    
    element = Element(tag)
    element.text = content
    return element

def add_child_node(nodelist, element):
    for node in nodelist:
        node.append(element)
        
def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)
                        
 