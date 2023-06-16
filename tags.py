#!/usr/bin/env python
# coding: utf-8

# In[2]:


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

#checking the K atrribute format
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(ele, keys): #userdefined function
    if ele.tag == "tag":
        if lower.search(ele.attrib['k']):
            keys['lower'] += 1
        elif lower_colon.search(ele.attrib['k']):
            keys['lower_colon'] += 1
        elif problemchars.search(ele.attrib['k']):
            keys['problemchars'] = keys['problemchars'] + 1
        else:    
            keys['other'] += 1  
    return keys


def process_keys_map(filenm): #case study function
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filenm):
        keys = key_type(element, keys)

    return keys

with open(FILEOSM,'rb') as j:
    keys = process_keys_map(FILEOSM)
    pprint.pprint(keys)
j.close()


# In[ ]:




