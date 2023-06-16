#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict
import re
import csv
import codecs
import cerberus
import sqlite3


FILEOSM = "petersburg.osm"
FILEOSMSAMPLE = "petersburg_sample.osm"
k = 40

#getting the elements that have tags of nodes and way
def get_element(FILEOSM, tags=('node', 'way', 'relation')): #case study function
    context = iter(ET.iterparse(FILEOSM, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

#getting sample from "petersburg.osm"
with open(FILEOSMSAMPLE, 'wb') as output: #case study function
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(FILEOSM)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')
    
#finding unique K attributes and the total number
def unique_keys(filenm):
    dstnct_keys = []
    cnt = 1

    EL = get_element(filenm, tags=('node', 'way', 'relation'))
    for ele in EL:
        if ele.tag == 'node' or ele.tag == 'way':
            for tag in ele.iter('tag'):
                if tag.attrib['k'] not in dstnct_keys:
                    dstnct_keys.append(tag.attrib['k'])
                    cnt += 1
    dstnct_keys.sort()
    print "Total number of unique keys (tag attrib['k'])is {}".format(cnt)
    
    pprint.pprint(dstnct_keys)
    
#finding the unique k attribute values
def values_for_unique_keys(filenm):        
        key = 'addr:street'
        vals = []
        EL = get_element(filenm, tags=('node', 'way', 'relation'))
        for ele in EL:
            for tag in ele.iter('tag'):
                if tag.attrib['k'] == key:
                    vals.append(tag.attrib['v'])
            ele.clear()
        print key
        pprint.pprint(vals)

    
#using "petersburg_sample.osm" to audit the key 'addr:street'                 
unique_keys(FILEOSMSAMPLE)

#using "petersburg_sample.osm" to audit the key 'addr:street'  
values_for_unique_keys(FILEOSMSAMPLE)


# In[ ]:




