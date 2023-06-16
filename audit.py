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

#auditing street names
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Broadway", "Drive", "Court", "Place", "Square", "Lane", "Road", "Plaza",
            "Trail", "Parkway", "Commons", "Center", "Freeway", "Way", "Highway", "Terrace", "South", "East", "West", "North"]

#variable "mapping" contains the corrections
mapping = {
            " St ": " Street ",
            " St.": " Street ",
            " ST ": " Street ",
            " st ": " Street ",
            " Rd.": " Road ",
            " Rd ": " Road ",
            " Rd": " Road ",
            " Ave ": " Avenue ", 
            " Ave.": " Avenue ",
            " Av ": " Avenue ", 
            " Avene ": " Avenue ",
            " Dr ": " Drive ",
            " Dr.": " Drive",
            " Blv ": " Boulevard ",
            " Blvd ": " Boulevard ",
            " Blvd": " Boulevard",
            " Blvd.": " Boulevard",
            " Broadway.": "Broadway",
            " Ct ": " Center ",
            " Ctr": " Center",
            " Pl ": " Place ",
            " Plz ": " Plaza ",
            " Ln ": " Lane ",
            " Wy": " Way ",
            " S ": " South ",
            " E ": " East ",
            " W ": " West ",
            " N ": "North"
}

#function to use to see if the input string is not in the expected list. 
def audit_street_type(street_types, street_name): #case study function
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

#function to use to look at the k attribute only if it equals to "addr:street"
def is_street_name(ele): #case study function
    return (ele.attrib['k'] == "addr:street")

#function to use to look at all the street types, which helps us fill-up the "mapping" dictionary
def audit(osmfile): #case study function 
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events = ("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
            elem.clear()        
    osm_file.close()
    return street_types


#converting the old street name to a better street name
def update_name(nm, mapping): #userowned function
    for key, val in mapping.iteritems():
        if key in nm:
            return nm.replace(key,val)
    return nm        


#using the "petersburg_sample.osm" file to audit the street name
st_types = audit(FILEOSMSAMPLE)

for typest, ways in st_types.iteritems():
    for nm in ways:
        nm_better = update_name(nm, mapping)
        print nm, "=>", nm_better
        
#-------------------------------------------------------------------------------------------------------#

#auditing postal codes to check for inconsistent formats
zip_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

zip_types = defaultdict(set)

zip_expected = {}

#function to use to see if the input string is not in the expected list. 
def audit_zip_codes(zip_types, zip_nm, reg_exp, zip_expected):
    f = reg_exp.search(zip_nm)
    if f:
        zip_type = f.group()
        if zip_type not in zip_expected:
             zip_types[zip_type].add(zip_nm)

#function to use to look at the k attribute only if it equals to "addr:postcode"
def is_zip_name(ele):
    return (ele.attrib['k'] == "addr:postcode")

#function to use to look at all the postal codes, which helps us fill-up the "mapping" dictionary
def audit(filenm, reg_exp):
    for evt, ele in ET.iterparse(filenm, events = ("start",)):
        if ele.tag == "way" or ele.tag == "node":
            for tag in ele.iter("tag"):
                if is_zip_name(tag):
                    audit_zip_codes(zip_types, tag.attrib['v'], reg_exp, zip_expected)
    pprint.pprint(dict(zip_types))



#using the "petersburg_sample.osm" file to audit the postcodes  
audit(FILEOSMSAMPLE, zip_type_re)


for zip_type, ways in zip_types.iteritems(): 
        for nm in ways:
            if "-" in nm:
                nm = nm.split("-")[0].strip()
            if "FL " in nm:
                nm = nm.split("FL ")[1].strip('FL ')
            elif len(str(nm)) > 5:
                nm = nm[0:5]
            elif nm.isdigit() == False:
                print 'OK'
            print nm


# In[ ]:




