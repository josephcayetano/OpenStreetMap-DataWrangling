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

#finding out how many element tags are in the "petersburg.osm" file
def count_tags(filenm): #userdefined function
    tree = ET.iterparse(filenm)
    tags = {}
    for evt, ele in tree:
        if ele.tag not in tags.keys():
            tags[ele.tag] = 1
        else:
            tags[ele.tag] = tags[ele.tag] + 1
    return tags    
    
with open(FILEOSM,'rb') as j:
    tags = count_tags(FILEOSM)
    pprint.pprint(tags)
j.close()


# In[ ]:




