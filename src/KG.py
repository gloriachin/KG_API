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
    e00: EdgeParams = edges['e00']             # {"object": "n01", "predicates": [ "biolink:targets" ], "attributes":{'biolink:provided_by': 'Multiomics-BigGIM'}, "subject": "n00"}
    e00_predicates = []                        # ["biolink:targets"]
    e00_predicate_type = ''                    # "TARGETS"
    e00_property = {}                          # {'biolink:provided_by': 'Multiomics-BigGIM'}
    e00_property_type = ''                     # "Provided_By"
    e00_property_value = ''                    # "MULTIOMICS-BIGGIM"
    subject_node = ''                          # "n00"
    object_node = ''                           # "n01"

    e00_predicates = e00.predicates 
    e00_predicate_type = e00_predicates[0].split(':')[1].upper()

    subject_node = e00.subject
    object_node = e00.object
    
    if e00.attributes is not None:
        e00_property = e00.attributes
        e00_property_type = list(e00_property)[0].split(':')[1]
        e00_property_value = "\"" + e00_property.get(list(e00_property)[0]).upper() + "\""

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
            subject_property_value = "\"" + subject_property_value.upper() + "\""

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
        else:
            object_property_value = "\"" + object_property_value.upper() + "\""

    match_subject = 'n00:' + subject_category_type
    match_edge = 'e00:' + e00_predicate_type
    match_object = 'n01:' + object_category_type
    where_subject = 'n00.' + subject_property_type + '=' + subject_property_value
    where_edge = 'e00.' + e00_property_type + '=' + e00_property_value
    where_object = 'n01.' + object_property_type + '=' + object_property_value

    # MATCH ({match_subject})-[{match_edge}]-({match_object})
    # WHERE {where_subject} AND {where_edge} AND {where_object}
    # RETURN DISTINCT n00, e00, n01, type(e00)

    # MATCH (n00:n00_category_type)-[e00:e00_predicate_type]-(n01:n01_category_type)
    # WHERE n00.n00_property_type=n00_property_value AND e00.e00_property_type=e00_property_value AND n01.n01_property_type=n01_property_value
    # RETURN DISTINCT n00, e00, n01, type(e00)

    # MATCH (n00:Drug)-[e00:TARGETS]-(n01:Gene)
    # WHERE n00.Name="PACLITAXEL" AND e00.Provided_By="MULTIOMICS-BIGGIM" AND n01.Symbol="BCL2"
    # RETURN DISTINCT n00, e00, n01, type(e00)

    result= {"match_subject": match_subject, "match_edge": match_edge, "match_object": match_object, "where_subject": where_subject, "where_edge": where_edge, "where_object": where_object}
    return(result)


def query_KG(json_query,db,match_subject,match_edge,match_object,where_subject,where_edge,where_object):
    if (where_edge != 'e00.='):
        if (where_subject != 'n00.=') & (where_object != 'n01.='):
            query = ''' MATCH ({match_subject})-[{match_edge}]-({match_object}) WHERE {where_subject} AND {where_edge} AND {where_object} RETURN DISTINCT n00, e00, n01, type(e00)'''.format(match_subject=match_subject, match_edge=match_edge, match_object=match_object, where_subject=where_subject, where_edge=where_edge, where_object=where_object)
        elif (where_subject == 'n00.=') & (where_object != 'n01.='):
            query = ''' MATCH ({match_subject})-[{match_edge}]-({match_object}) WHERE {where_edge} AND {where_object} RETURN DISTINCT n00, e00, n01, type(e00)'''.format(match_subject=match_subject, match_edge=match_edge, match_object=match_object, where_edge=where_edge, where_object=where_object)
        elif (where_subject != 'n00.=') & (where_object == 'n01.='):
            query = ''' MATCH ({match_subject})-[{match_edge}]-({match_object}) WHERE {where_subject} AND {where_edge} RETURN DISTINCT n00, e00, n01, type(e00)'''.format(match_subject=match_subject, match_edge=match_edge, match_object=match_object, where_subject=where_subject, where_edge=where_edge)
        else:
            query = ''' MATCH ({match_subject})-[{match_edge}]-({match_object}) WHERE {where_edge} RETURN DISTINCT n00, e00, n01, type(e00)'''.format(match_subject=match_subject, match_edge=match_edge, match_object=match_object, where_edge=where_edge)

    elif (where_edge == 'e00.='):
        if (where_subject != 'n00.=') & (where_object != 'n01.='):
            query = ''' MATCH ({match_subject})-[{match_edge}]-({match_object}) WHERE {where_subject} AND {where_object} RETURN DISTINCT n00, e00, n01, type(e00)'''.format(match_subject=match_subject, match_edge=match_edge, match_object=match_object, where_subject=where_subject, where_object=where_object)
        elif (where_subject == 'n00.=') & (where_object != 'n01.='):
            query = ''' MATCH ({match_subject})-[{match_edge}]-({match_object}) WHERE {where_object} RETURN DISTINCT n00, e00, n01, type(e00)'''.format(match_subject=match_subject, match_edge=match_edge, match_object=match_object, where_object=where_object)
        elif (where_subject != 'n00.=') & (where_object == 'n01.='):
            query = ''' MATCH ({match_subject})-[{match_edge}]-({match_object}) WHERE {where_subject} RETURN DISTINCT n00, e00, n01, type(e00)'''.format(match_subject=match_subject, match_edge=match_edge, match_object=match_object, where_subject=where_subject)
        else:
            query = ''' MATCH ({match_subject})-[{match_edge}]-({match_object}) RETURN DISTINCT n00, e00, n01, type(e00)'''.format(match_subject=match_subject, match_edge=match_edge, match_object=match_object)
    
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
    df = query_KG(json_query, db, result['match_subject'], result['match_edge'], result['match_object'],result['where_subject'], result['where_edge'], result['where_object'])
    return(df)