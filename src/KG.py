import re
import sys
import json
import neo4j
import pandas as pd
from os import stat_result
from pydantic import BaseModel
from neo4j import GraphDatabase
from unicodedata import category
from typing import Optional, Dict, List, Any

# BaseModels are from BigGIM.py in the BigGIM_fastapi GitHub repository 
# Accessible at: https://github.com/gloriachin/BigGIM_fastapi/blob/main/src/BigGIM.py

class db_connect:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd), encrypted=False)
        except Exception as e:
            print("Failed to create the driver", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Failed to create the driver"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("The Query could not complete:", e)
        finally: 
            if session is not None:
                session.close()
        return response

db = db_connect("neo4j://34.171.95.111:7687","neo4j","GeneData")

class EdgeParams(BaseModel):
    subject: str
    object: str
    predicates: List[str]
    attributes: Optional[Dict[str, str]]

class NodeParams(BaseModel):
    categories: List[str]
    ids: Optional[List[str]]

class QueryGraph(BaseModel):
    edges: Dict[str, EdgeParams]
    nodes: Dict[str, NodeParams]

class QueryMessage(BaseModel):
    query_graph: QueryGraph

class KnowledgeGraph(BaseModel):
    nodes:Dict[str,NodeParams]
    edges:Dict[str,EdgeParams]
class NodeBinding(BaseModel):
    id: str

class SubAttribute(BaseModel):
   attribute_type_id: str
   original_attribute_name: str
   value: Any
   value_type_id: str
   attribute_source: str
   value_url: str
   description: str

class Attribute(BaseModel):
   attribute_type_id: str
   original_attribute_name: str
   value: Any
   value_type_id: str
   attribute_source: str
   value_url: str
   description: str
   attributes: List[SubAttribute]

class EdgeBinding(BaseModel):
    id: str
    attributes: List[Attribute]

class ResultMessage(BaseModel):
    node_bindings: Dict[str, List[NodeBinding]]
    edge_bindings: Dict[str, List[EdgeBinding]]
    score: float

class ResponseMessage(BaseModel):
    query_graph: QueryGraph
    knowledge_graph: KnowledgeGraph
    results: List[ResultMessage]

class Query(BaseModel):
    message: QueryMessage


def parse_query(query:Query):
    result = {}

    nodes = Dict[str, EdgeParams] = query.message.query_graph.nodes # { "n00": { "categories": [ "biolink:Gene", ], "ids": [ "NCBI:64102" ],},  "n01": { "categories": [ "biolink:Drug"]}}
    edges = Dict[str, EdgeParams] = query.message.query_graph.edges # { "e00": { "object": "n01", "predicates": [ "biolink:targets" ], "subject": "n00"}}

    # Handle edges
    e00: EdgeParams = edges['e00']  # {"object": "n01", "predicates": [ "biolink:targets" ], "attributes":{"biolink:tumor_type":"GBM", "subject": "n00"}
    e00_predicates = []             # ["biolink:targets"]
    e00_predicate_type = ''         # "TARGETS"
    e00_property = []               # ["biolink:tumor_type":"GBM"]
    e00_property_type = ''          # "TUMOR_TYPE"
    e00_property_value = ''         # "GBM"

    e00_predicates = e00.predicates 
    e00_predicate_type = e00_predicates.split(':')[1].upper()

    if e00.attributes is not None:
        e00_property = e00.attributes 
        e00_property_type = e00_property.split(':')[0].split(':')[1].upper()
        e00_property_value = e00_property.split(':')[1] #.upper()?

    # Handle node n00
    n00: NodeParams = nodes['n00']  # {"categories": [ "biolink:Gene", ], "ids": [ "NCBI:64102" ]}
    n00_categories = []             # ["biolink:Gene"]
    n00_category_type = ''          # "Gene"
    n00_ids = []                    # ["NCBI:64102"]
    n00_property_type = ''          # "NCBI"
    n00_property_value = ''         # "64102"

    n00_categories = n00.categories 
    n00_category_type = n00_categories.split(':')[1] 

    if n00.ids is not None:
        n00_ids = n00.ids 

    for id in n00_ids:
        n00_property_type = id.split(':')[0] 
        n00_property_value = id.split(':')[1] 

    if n00_property_type == 'Symbol' | n00_property_type == 'Name':
        n00_property_value = n00_property_value.upper()
    else:
        n00_property_type = n00_property_type + "_ID"
        n00_property_value = int(n00_property_value)


    # Handle node n01
    n01: NodeParams = nodes['n01']  # {"categories": [ "biolink:Drug"]}
    n01_categories = []             # ["biolink:Drug"]
    n01_category_type = ''          # "Drug"
    n01_ids = []                    # ["Name:Afatinib"]
    n01_property_type = ''          # "Name"
    n01_property_value = ''         # "AFATINIB"
    
    n01_categories = n01.categories 
    n01_category_type = n01_categories.split(':')[1] 

    if n01.ids is not None:
        n01_ids = n01.ids 

    for id in n01_ids:
        n01_property_type = id.split(':')[0]
        n01_property_value = id.split(':')[1]

    if n01_property_type == 'Symbol' | n01_property_type == 'Name':
        n01_property_value = n01_property_value.upper()
    else:
        n01_property_type = n01_property_type + "_ID"
        n01_property_value = int(n01_property_value)

    string1 = 'n00:' + n00_category_type
    string2 = 'e00:' + e00_predicate_type
    string3 = 'n01:' + n01_category_type
    string4 = 'n00.' + n00_property_type + "=" + n00_property_value
    string5 = 'n01.' + n01_property_type + "=" + n01_property_value

    # MATCH ({string1})-[{string2}]-({string3})
    # WHERE {string4} AND {string5}
    # RETURN DISTINCT n00, e00, n01

    # MATCH (n00:n00_category_type)-[e00:e00_predicate_type]-(n01:n01_category_type)
    # WHERE n00.n00_property_type=n00_property_value AND n01.n01_property_type=n01_property_value
    # RETURN DISTINCT n00, e00, n01

    # MATCH (n00:Gene)-[e00:TARGETS]-(n01:Drug)
    # WHERE n00.NCBI_ID=64102 AND n01.Name="AFATINIB"
    # RETURN DISTINCT n00, e00, n01

    result= {"string1": string1, "string2": string2, "string3": string3, "string4": string4,"string5": string5}
    return(result)


def query_KG(query,string1,string2,string3,string4,string5):
    response_query={}

    if string4 != 'n00.=' & string5 != 'n01.=':
        query = '''
            MATCH ({string1})-[{string2}]-({string3})
            WHERE {string4} AND {string5}
            RETURN DISTINCT n00, e00, n01
            '''.format(string1=string1,string2=string2,string3=string3,string4=string4,string5=string5)
    elif string4 == 'n00.=':
        query = '''
            MATCH ({string1})-[{string2}]-({string3})
            WHERE {string5}
            RETURN DISTINCT n00, e00, n01
            '''.format(string1=string1,string2=string2,string3=string3,string5=string5)
    elif string5 == 'n01.=':
        query = '''
            MATCH ({string1})-[{string2}]-({string3})
            WHERE {string4}
            RETURN DISTINCT n00, e00, n01
            '''.format(string1=string1,string2=string2,string3=string3,string4=string4)
    else:
        query = ''''''

    print(query)
    result = db.query(query, db='neo4j')
    
    response_query["message"] = {"query_graph":query.message.query_graph,

                                "knowledge_graph":{"edges":{},
                                                    "nodes":{}}, 
                                "results":{}}

    for words in result:
        response_query['message']['knowledge_graph']['edges'][words[0].Name + "-"+words[1].type ] = {
                                                                                    "Pubchem_ID": words[0].Pubchem_ID
                                                                                    #keep doing that for the rest of the stuff for drug and relationship
                                                                                     }
    return(response_query)


def Query_KG_all(json_query):
    result = parse_query(json_query)
    df = query_KG(json_query, result['string1'], result['string2'], result['string3'],result['string4'], result['string5'])
    return(df)