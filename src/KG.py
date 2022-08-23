import re
import sys
import json
import neo4j
from os import stat_result
from pydantic import BaseModel
from neo4j import GraphDatabase
from unicodedata import category
from typing import Optional, Dict, List, Any

# KG.py
# This file parses the json formatted user-input, and places its components into a Cypher query. 
# It then connects to and queries the neo4j graph database with this Cypher query. 
# Finally, it parses the results and makes a json formatted response, and returns this.
# Authors: Katie Christensen and Omar Aziz
# June - August 2022

# BaseModels are from the BigGIM_fastapi GitHub repository 
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
            print("The query could not complete:", e)
        finally: 
            if session is not None:
                session.close()
        return response

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

class Query(BaseModel):
    message: QueryMessage

def parse_query(query:Query):
    result = {}

    nodes = Dict[str, EdgeParams]
    edges = Dict[str, EdgeParams]
                                               # EXAMPLE USER INPUT JSON - to visually show what each variable is holding.
    nodes =  query.message.query_graph.nodes   # { "n00": { "categories": [ "biolink:Gene", ], "ids": [ "NCBI:64102" ],},  "n01": { "categories": [ "biolink:Drug"]}}
    edges =  query.message.query_graph.edges   # { "e00": { "object": "n01", "predicates": [ "biolink:targets" ], "subject": "n00"}}

    # Handle edges
    e00: EdgeParams = edges['e00']             # {"object": "n01", "predicates": [ "biolink:targets" ], "attributes":{"biolink:tumor_type":"GBM", "subject": "n00"}
    e00_predicates = []                        # ["biolink:targets"]
    e00_predicate_type = ''                    # "TARGETS"
    e00_property = []                          # ["biolink:tumor_type":"GBM"]
    e00_property_type = ''                     # "TUMOR_TYPE"
    e00_property_value = ''                    # "GBM"
    subject_node = ''                          # "n00"
    object_node = ''                           # "n01"

    e00_predicates = e00.predicates 
    e00_predicate_type = e00_predicates[0].split(':')[1].upper()

    subject_node = e00.subject
    object_node = e00.object

    if e00.attributes is not None: #might get an error about splitting a list but lets check that later
        e00_property = e00.attributes 
        e00_property_type = e00_property.split(':')[0].split(':')[1].upper()
        e00_property_value = e00_property.split(':')[1] #.upper()?

    # Handle node n00
    subject: NodeParams = nodes[subject_node]  # {"categories": [ "biolink:Gene", ], "ids": [ "NCBI:64102" ]}
    subject_categories = []                    # ["biolink:Gene"]
    subject_category_type = ''                 # "Gene"
    subject_ids = []                           # ["NCBI:64102"]
    subject_property_type = ''                 # "NCBI"
    subject_property_value = ''                # "64102"

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
        else:
            subject_property_value = subject_property_value.upper()

    # Handle node n01
    object: NodeParams = nodes[object_node]    # {"categories": [ "biolink:Drug"]}
    object_categories = []                     # ["biolink:Drug"]
    object_category_type = ''                  # "Drug"
    object_ids = []                            # ["Name:Afatinib"]
    object_property_type = ''                  # "Name"
    object_property_value = ''                 # "AFATINIB"
    
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
        else:
            object_property_value = object_property_value.upper()

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

    # MATCH (n00:Drug)-[e00:TARGETS]-(n01:Gene)
    # WHERE n00.Name="PACLITAXEL" AND n01.Symbol="BCL2"
    # RETURN DISTINCT n00, e00, n01

    result= {"string1": string1, "string2": string2, "string3": string3, "string4": string4,"string5": string5}
    return(result)


def query_KG(json_query,db,string1,string2,string3,string4,string5):
    if (string4 != 'n00.=') & (string5 != 'n01.='):
        query = ''' MATCH ({string1})-[{string2}]-({string3}) WHERE {string4} AND {string5} RETURN DISTINCT n00, e00, n01, type(e00)'''.format(string1=string1,string2=string2,string3=string3,string4=string4,string5=string5)
    
    elif (string4 == 'n00.='):
        query = '''MATCH ({string1})-[{string2}]-({string3}) WHERE {string5} RETURN DISTINCT n00, e00, n01, type(e00)'''.format(string1=string1,string2=string2,string3=string3,string5=string5)
    
    elif (string5 == 'n01.='):
        query = '''MATCH ({string1})-[{string2}]-({string3}) WHERE {string4} RETURN DISTINCT n00, e00, n01, type(e00)'''.format(string1=string1,string2=string2,string3=string3,string4=string4)
    
    else:
        query = ''''''

    result = db.query(query, db='neo4j')
    
    response_list = []

    for word in result:
        response_message={}

        response_message["query_graph"] = json_query
        response_message["results"] = {}
        response_message["knowledge_graph"] =  {}
        response_message["knowledge_graph"]["edges"] =  {}
        response_message["knowledge_graph"]["nodes"] =  {}

        w = dict(word)
        n0 = dict(w.get("n00"))
        e0 = dict(w.get("e00"))
        n1 = dict(w.get("n01"))
        predicate = w.get("type(e00)")

        response_message['knowledge_graph']['nodes']["n00"] = {
                                                            "Subject_Name": n0.get("Name"),
                                                            "Subject_Symbol": n0.get("Symbol"),
                                                            "Subject_Category": n0.get("Category"),
                                                            "Subject_attributes": 
                                                                {
                                                                "Subject_NCBI_ID": n0.get("NCBI_ID"),
                                                                "Subject_MONDO_ID": n0.get("MONDO_ID"),
                                                                "Subject_Chembl_ID": n0.get("Chembl_ID"),
                                                                "Subject_Pubchem_ID": n0.get("Pubchem_ID"),
                                                                "Subject_Synonym": n0.get("Synonym"),
                                                                "Subject_Prefixes": n0.get("Prefixes")
                                                                }
                                                            }

        response_message['knowledge_graph']['edges']["e00"] = {
                                                            "Predicate": predicate,
                                                            "Edge_attributes": 
                                                                {
                                                                "Edge_attribute_publications": e0.get("Publications"),
                                                                "Edge_attribute_knowledge_source": e0.get("Knowledge_Source"),
                                                                "Edge_attribute_provided_by": e0.get("Provided_by"),
                                                                "Edge_attribute_FDA_approval_status": e0.get("FDA_approval_status")
                                                                }
                                                            }

        response_message['knowledge_graph']['nodes']["n01"] = {
                                                            "Object_Name": n1.get("Name"),
                                                            "Object_Symbol": n1.get("Symbol"),
                                                            "Object_Category": n1.get("Category"),
                                                            "Object_attributes": 
                                                                {
                                                                "Object_NCBI_ID": n1.get("NCBI_ID"),
                                                                "Object_MONDO_ID": n1.get("MONDO_ID"),
                                                                "Object_Chembl_ID": n1.get("Chembl_ID"),
                                                                "Object_Pubchem_ID": n1.get("Pubchem_ID"),
                                                                "Object_Synonym": n1.get("Synonym"),
                                                                "Object_Prefixes": n1.get("Prefixes")
                                                                }
                                                            }

        response_list.insert(len(response_list)-1, response_message)

    response = {}
    response["message"] = response_list
    return(response)

def Query_KG_all(json_query,db):
    result = parse_query(json_query)
    df = query_KG(json_query, db, result['string1'], result['string2'], result['string3'],result['string4'], result['string5'])
    return(df)