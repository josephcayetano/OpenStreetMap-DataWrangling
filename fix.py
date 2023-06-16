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

#getting the elements that have tags of nodes and way
def get_element(FILEOSM, tags=('node', 'way', 'relation')): #case study function
    context = iter(ET.iterparse(FILEOSM, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

#if street name has a string that is contained in the mapping variable, then the change will be made
#to format the street name, functions update_street_name and audit_street_name_tag will be used in the shape_element function
def update_street_name(nm, mapping):
    for key, val in mapping.iteritems():
        if key in nm:
            return nm.replace(key, val)
    return nm       

def audit_street_name_tag(ele): 
    strtname = ele.get('v')
    f = street_type_re.search(strtname)
    if f:
        strtname_better = update_street_name(strtname,mapping)
        return strtname_better
    return strtname


#making all postal codes a 5 digit number. This will fix any postal code that have more than 5 digits and begins with 
#a state abbreviation like "FL" for Florida. 
#to format the postal codes, functions update_postcode and audit_postcode_tag will be used in the shape_element function
def update_postcode(nm): 
    if "-" in nm:
        nm = nm.split("-")[0].strip()
    elif "FL" in nm:
        nm = nm.split("FL ")[1].strip('FL ')
    elif len(str(nm)) > 5:
        nm = nm[0:5]
    elif nm.isdigit() == False:
         nm = 00000
    return nm

def audit_postcode_tag(ele, reg_exp=re.compile(r'\b\S+\.?$', re.IGNORECASE)):
    postal_cd = ele.get('v')
    f = reg_exp.search(postal_cd)
    if f:
        postal_cd_better = update_postcode(postal_cd)
        return postal_cd_better
    return postal_cd


schema = {
    'node': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'lat': {'required': True, 'type': 'float', 'coerce': float},
            'lon': {'required': True, 'type': 'float', 'coerce': float},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'node_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    },
    'way': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'way_nodes': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'node_id': {'required': True, 'type': 'integer', 'coerce': int},
                'position': {'required': True, 'type': 'integer', 'coerce': int}
            }
        }
    },
    'way_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    }
}

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWCOLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


#cleaning and shaping node or way XML element to Python dictionary
def shape_element(ele, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS, #userowned
                  problem_chars=PROBCHARS, default_tag_type='regular'):
    
    
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []
             
    if ele.tag == 'node':
        for fld in node_attr_fields:
            node_attribs[fld] = ele.get(fld)
                 
        if ele.find('tag') is None:
            pass
           
        elif ele.find('tag') is not None:
            tag_atb = {}
            node_tag_fld = NODE_TAGS_FIELDS
            for z in ele.iter('tag'):
                if PROBCHARS.search(z.attrib['k']):
                    pass
                elif LOWCOLON.search(z.attrib['k']):
                    tag_atb[node_tag_fld[0]] = ele.get('id')
                    tag_atb[node_tag_fld[1]] = z.get('k')[(z.get('k').find(':') + 1):]
                    if z.attrib['k'] == "addr:street":
                        tag_atb[node_tag_fld[2]] = audit_street_name_tag(z)
                    elif z.attrib['k'] == "addr:postcode":
                        tag_atb[node_tag_fld[2]] = audit_postcode_tag(z)       
                    else:
                        tag_atb[node_tag_fld[2]] = z.get('v')
                    tag_atb[node_tag_fld[3]] = z.get('k').split(':')[0]
                    tags.append(tag_atb.copy())
                
                else:
                    tag_atb[node_tag_fld[0]] = ele.get('id')
                    tag_atb[node_tag_fld[1]] = z.get('k')
                    if z.attrib['k'] == "addr:street":
                        tag_atb[node_tag_fld[2]] = audit_street_name_tag(z)
                    elif z.attrib['k'] == "addr:postcode":
                        tag_atb[node_tag_fld[2]] = audit_postcode_tag(z)    
                    else:    
                        tag_atb[node_tag_fld[2]] = z.get('v')
                    tag_atb[node_tag_fld[3]] = default_tag_type
                    tags.append(tag_atb.copy())
        
                
    elif ele.tag == 'way':
        for fld in way_attr_fields:
            way_attribs[fld] = ele.get(fld)
    
        way_node_atb = {}
        way_node_fld = WAY_NODES_FIELDS
        for node in ele.findall('nd'):
            way_node_atb[way_node_fld[0]] = ele.get('id')
            way_node_atb[way_node_fld[1]] = node.get('ref')
            way_node_atb[way_node_fld[2]] = ele.findall('nd').index(node)
            way_nodes.append(way_node_atb.copy())
        
        if ele.find('tag') is None:
            pass
           
        elif ele.find('tag') is not None:
            way_tag_atb = {}
            way_tag_fld = WAY_TAGS_FIELDS
            for z in ele.iter('tag'):
                if PROBCHARS.search(z.attrib['k']):
                    pass
                elif LOWCOLON.search(z.attrib['k']):
                    way_tag_atb[way_tag_fld[0]] = ele.get('id')
                    way_tag_atb[way_tag_fld[1]] = z.get('k')[(z.get('k').find(':') + 1):]
                    if z.attrib['k'] == "addr:street":
                        way_tag_atb[way_tag_fld[2]] = audit_street_name_tag(z)
                    elif z.attrib['k'] == "addr:postcode":
                        way_tag_atb[way_tag_fld[2]] = audit_postcode_tag(z)    
                    else:
                        way_tag_atb[way_tag_fld[2]] = z.get('v')
                    way_tag_atb[way_tag_fld[3]] = z.get('k').split(':')[0]
                    tags.append(way_tag_atb.copy())
                    
                else:
                    way_tag_atb[way_tag_fld[0]] = ele.get('id')
                    way_tag_atb[way_tag_fld[1]] = z.get('k')
                    if z.attrib['k'] == "addr:street":
                        way_tag_atb[way_tag_fld[2]] = audit_street_name_tag(z) 
                    elif z.attrib['k'] == "addr:postcode":
                        way_tag_atb[way_tag_fld[2]] = audit_postcode_tag(z)    
                    else:   
                        way_tag_atb[way_tag_fld[2]] = z.get('v')
                    way_tag_atb[way_tag_fld[3]] = default_tag_type
                    tags.append(way_tag_atb.copy())
    
    if ele.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif ele.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

#raising validation error if element does not match schema
def validate_element(element, validator, schema=SCHEMA): #case study function
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))
        
#extending csv.DictWriter to handle Unicode input
class UnicodeDictWriter(csv.DictWriter, object): #case study function

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            
#iteratively process each XML element and write to csv(s)
def process_map(file_in, validate): #case study function

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

process_map(FILEOSM, validate=True)


# In[ ]:




