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

#db = db_connect("neo4j://34.171.95.111:7687","neo4j","GeneData")

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
    print("In parse_query")
    
    result = {}

    nodes = Dict[str, EdgeParams]
    edges = Dict[str, EdgeParams]

    nodes =  query.message.query_graph.nodes # { "n00": { "categories": [ "biolink:Gene", ], "ids": [ "NCBI:64102" ],},  "n01": { "categories": [ "biolink:Drug"]}}
    edges =  query.message.query_graph.edges # { "e00": { "object": "n01", "predicates": [ "biolink:targets" ], "subject": "n00"}}

    # Handle edges
    e00: EdgeParams = edges['e00']  # {"object": "n01", "predicates": [ "biolink:targets" ], "attributes":{"biolink:tumor_type":"GBM", "subject": "n00"}
    e00_predicates = []             # ["biolink:targets"]
    e00_predicate_type = ''         # "TARGETS"
    e00_property = []               # ["biolink:tumor_type":"GBM"]
    e00_property_type = ''          # "TUMOR_TYPE"
    e00_property_value = ''         # "GBM"
    subject_node = ''               # "n00"
    object_node = ''                # "n01"

    e00_predicates = e00.predicates 
    e00_predicate_type = e00_predicates[0].split(':')[1].upper()

    subject_node = e00.subject
    object_node = e00.object

    if e00.attributes is not None: # this probably isn't correct like might have error splitting list but check this later. 
        e00_property = e00.attributes 
        e00_property_type = e00_property.split(':')[0].split(':')[1].upper()
        e00_property_value = e00_property.split(':')[1] #.upper()?

    # Handle node n00
    subject: NodeParams = nodes[subject_node]  # {"categories": [ "biolink:Gene", ], "ids": [ "NCBI:64102" ]}
    subject_categories = []             # ["biolink:Gene"]
    subject_category_type = ''          # "Gene"
    subject_ids = []                    # ["NCBI:64102"]
    subject_property_type = ''          # "NCBI"
    subject_property_value = ''         # "64102"

    subject_categories = subject.categories 
    subject_category_type = subject_categories[0].split(':')[1] 

    if subject.ids is not None:
        subject_ids = subject.ids 

    for id in subject_ids:
        subject_property_type = id.split(':')[0] 
        subject_property_value = id.split(':')[1] 

    if (subject_property_type != 'Symbol') & (subject_property_type != 'Name'):
        subject_property_type = subject_property_type + "_ID"
        subject_property_value = int(subject_property_value)

    # Handle node n01
    object: NodeParams = nodes[object_node]  # {"categories": [ "biolink:Drug"]}
    object_categories = []             # ["biolink:Drug"]
    object_category_type = ''          # "Drug"
    object_ids = []                    # ["Name:Afatinib"]
    object_property_type = ''          # "Name"
    object_property_value = ''         # "AFATINIB"
    
    object_categories = object.categories 
    object_category_type = object_categories[0].split(':')[1] 

    if object.ids is not None:
        object_ids = object.ids 

    for id in object_ids:
        object_property_type = id.split(':')[0]
        object_property_value = id.split(':')[1]

    if (object_property_type != 'Symbol') & (object_property_type != 'Name'):
        object_property_type = object_property_type + "_ID"
        object_property_value = int(object_property_value)

    string1 = 'n00:' + subject_category_type
    string2 = 'e00:' + e00_predicate_type
    string3 = 'n01:' + object_category_type
    string4 = 'n00.' + subject_property_type + '=' + subject_property_value
    string5 = 'n01.' + object_property_type + '=' + object_property_value

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


def query_KG(query,db,string1,string2,string3,string4,string5):
    print("In query_KG")

    response_query={}

    if (string4 != 'n00.=') & (string5 != 'n01.='):
        query = '''
            MATCH ({string1})-[{string2}]-({string3})
            WHERE {string4} AND {string5}
            RETURN DISTINCT n00, e00, n01
            '''.format(string1=string1,string2=string2,string3=string3,string4=string4,string5=string5)
    elif (string4 == 'n00.='):
        query = '''
            MATCH ({string1})-[{string2}]-({string3})
            WHERE {string5}
            RETURN DISTINCT n00, e00, n01
            '''.format(string1=string1,string2=string2,string3=string3,string5=string5)
    elif (string5 == 'n01.='):
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
                                                                                    "Subject_Chembl_ID": Optional[words[0].Chembl_ID],
                                                                                    "Subject_NCBI_ID": Optional[words[0].NCBI_ID],
                                                                                    "Subject_Name": Optional[words[0].Name],
                                                                                    "Subject_Category": Optional[words[0].Category],
                                                                                    "Subject_Synonym": Optional[words[0].Synonym],
                                                                                    "Subject_Pubchem_ID": Optional[words[0].Pubchem_ID],
                                                                                    "Subject_MONDO_ID": Optional[words[0].MONDO_ID],
                                                                                    "Subject_Prefixes": Optional[words[0].Prefixes],
                                                                                    "Subject_Symbol": Optional[words[0].Symbol],

                                                                                    "Edge_attribute_knowledge_source": Optional[words[1].Knowledge_Source],
                                                                                    "Edge_attribute_publications": Optional[words[1].Publications],
                                                                                    "Edge_attribute_provided_by": Optional[words[1].Provided_By],
                                                                                    "Edge_attribute_FDA_approval_status": Optional[words[1].FDA_approval_status],
                                                                                    
                                                                                    "Object_Chembl_ID": Optional[words[2].Chembl_ID],
                                                                                    "Object_NCBI_ID": Optional[words[2].NCBI_ID],
                                                                                    "Object_Name": Optional[words[2].Name],
                                                                                    "Object_Category": Optional[words[2].Category],
                                                                                    "Object_Synonym": Optional[words[2].Synonym],
                                                                                    "Object_Pubchem_ID": Optional[words[2].Pubchem_ID],
                                                                                    "Object_MONDO_ID": Optional[words[2].MONDO_ID],
                                                                                    "Object_Prefixes": Optional[words[2].Prefixes],
                                                                                    "Object_Symbol": Optional[words[2].Symbol]
                                                                                    
                                                                                     }
    return(response_query)


def Query_KG_all(json_query,db):
    result = parse_query(json_query)
    df = query_KG(json_query, db, result['string1'], result['string2'], result['string3'],result['string4'], result['string5'])
    return(df)