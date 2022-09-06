from ctypes import sizeof
import re
import sys
import json
import neo4j
from os import stat_result
from pydantic import BaseModel
from neo4j import GraphDatabase
from unicodedata import category
from typing import Optional, Dict, List, Any

# KG_types.py
# This file returns to the user a message telling them:
# 1. The relationship types in the graph database, 
# 2. The node types in the graph database,
# 3. The relationship properties that they are allowed to search with
#    in the relationship 'attribute' dictionary of their JSON query, and
# 4. The node properties that they are allowed to search with 
#    in the node 'id' list of their JSON query
# Author: Katie Christensen
# August 2022

def get_KG_types(db):
    relationship_query = ''
    relationship_types = {}
    relationship_types_result = ''
    relationship_properties = ''
    rel_list = []

    node_query = ''
    node_types = {}
    node_types_results = ''
    node_properties = ''
    node_list = []

    # Handle relationships
    relationship_query = ''' MATCH ()-[rel]-() RETURN DISTINCT TYPE(rel)'''
    relationship_types = db.query(relationship_query, db='neo4j')

    for i, word in enumerate(relationship_types):
        rel_list.insert(len(rel_list)-1, dict(relationship_types[i]).get("TYPE(rel)"))

    relationship_types_result = "Relationship types currently in the database: " + str(rel_list) + ". "
    relationship_properties = "Relationship attributes allowed in the user-input JSON query: ['Provided_By', 'Knowledge_Source', 'Publications', 'FDA_approval_status']. "

    # Handle nodes
    node_query = ''' MATCH (node) RETURN DISTINCT node.Category'''
    node_types = db.query(node_query, db='neo4j')

    for i, word in enumerate(node_types):
        node_list.insert(len(node_list)-1, node_types[i].get('node.Category'))

    node_types_results = "Node types currently in the database: " + str(node_list) + ". "
    node_properties = "Node id's allowed in the user-input JSON query: ['Name', 'Symbol', 'MONDO', 'NCBI', 'Pubchem', 'Chembl']. "

    # Handle result
    result = relationship_types_result + relationship_properties + node_types_results + node_properties
    return(result)
