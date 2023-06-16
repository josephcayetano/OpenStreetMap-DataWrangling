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
#import schema
import sqlite3

#connecting to the database. The name of the database file is "petersburg.db"
con = sqlite3.connect("petersburg.db") 

#acquring the cursor object using the variable "cur"                                
cur = con.cursor()


#creating the "nodes" table in "petersburg.db" and specifying its columns' names and datatypes
cur.execute("CREATE TABLE nodes (id INTEGER PRIMARY KEY NOT NULL,lat REAL,lon REAL,user TEXT,uid INTEGER,version INTEGER,changeset INTEGER,timestamp TEXT);")
con.commit()

#reading in the "nodes.csv" file and formatting the data as a list of tuples
with open('nodes.csv','rb') as j: 
    dire = csv.DictReader(j)
    to_db = [(i['id'].decode("utf-8"),i['lat'].decode("utf-8"),i['lon'].decode("utf-8"),i['user'].decode("utf-8"),i['uid'].decode("utf-8"),i['version'].decode("utf-8"),i['changeset'].decode("utf-8"),i['timestamp'].decode("utf-8")) for i in dire]
    
#inserting the formatted data from "nodes.csv" into the "nodes" table
cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?,?,?,?,?,?,?,?);", to_db)
con.commit()
j.close()


#creating the "nodes_tags" table in "petersburg.db" and specifying its columns' names and datatypes
cur.execute("CREATE TABLE nodes_tags (id INTEGER,key TEXT,value TEXT,type TEXT,FOREIGN KEY (id) REFERENCES nodes(id));")
con.commit()

#reading in the "nodes_tags.csv" file and formatting the data as a list of tuples
with open('nodes_tags.csv','rb') as j: 
    dire = csv.DictReader(j)
    to_db = [(i['id'].decode("utf-8"),i['key'].decode("utf-8"),i['value'].decode("utf-8"),i['type'].decode("utf-8")) for i in dire]

#inserting the formatted data from "nodes_tags.csv" into the "nodes_tags" table
cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?,?,?,?);", to_db)
con.commit()
j.close()


#creating the "ways" table in "petersburg.db" and specifying its columns' names and datatypes
cur.execute("CREATE TABLE ways(id INTEGER PRIMARY KEY NOT NULL,user TEXT,uid INTEGER,version TEXT,changeset INTEGER,timestamp TEXT);")
con.commit()

#reading in the "ways.csv" file and formatting the data as a list of tuples
with open('ways.csv','rb') as j: 
    dire = csv.DictReader(j)
    to_db = [(i['id'].decode("utf-8"),i['user'].decode("utf-8"),i['uid'].decode("utf-8"),i['version'].decode("utf-8"),i['changeset'].decode("utf-8"),i['timestamp'].decode("utf-8")) for i in dire]

#inserting the formatted data from "ways.csv" into the "ways" table 
cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?,?,?,?,?,?);", to_db)
con.commit()
j.close()


#creating the "ways_nodes" table in "petersburg.db" and specifying its columns' names and datatypes
cur.execute("CREATE TABLE ways_nodes (id INTEGER NOT NULL,node_id INTEGER NOT NULL,position INTEGER NOT NULL,FOREIGN KEY (id) REFERENCES ways(id),FOREIGN KEY (node_id) REFERENCES nodes(id));")
con.commit()

#reading in the "ways_nodes.csv" file and formatting the data as a list of tuples
with open('ways_nodes.csv','rb') as j: 
    dire = csv.DictReader(j)
    to_db = [(i['id'].decode("utf-8"),i['node_id'].decode("utf-8"),i['position'].decode("utf-8")) for i in dire]

    
#inserting the formatted data from "ways_nodes.csv" into the "ways_nodes" table     
cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?,?,?);", to_db)
con.commit()
j.close()


#creating the "ways_tags" table in "petersburg.db" and specifying its columns' names and datatypes
cur.execute("CREATE TABLE ways_tags (id INTEGER NOT NULL,key TEXT NOT NULL,value TEXT NOT NULL,type TEXT,FOREIGN KEY (id) REFERENCES ways(id));")
con.commit()


#reading in the "ways_tags.csv" file and formatting the data as a list of tuples
with open('ways_tags.csv','rb') as j: 
    dire = csv.DictReader(j)
    to_db = [(i['id'].decode("utf-8"),i['key'].decode("utf-8"),i['value'].decode("utf-8"),i['type'].decode("utf-8")) for i in dire]

#inserting the formatted data from "ways_tags.csv" into the "ways_tags" table     
cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?,?,?,?);", to_db)
con.commit()
j.close()


# In[ ]:




