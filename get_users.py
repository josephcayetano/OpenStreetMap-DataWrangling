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

#getting users and the number of users in the "petersburg.osm" file
def get_user(ele):
    return ele.get('user')


def process_users_map(filenm):
    users = set()
    for _, ele in ET.iterparse(filenm):
        if ele.get('user'):
            users.add(get_user(ele))
        ele.clear()    
    return users


with open(FILEOSM,'rb') as j:
    users = process_users_map(FILEOSM)

print len(users)
j.close()


# In[ ]:




