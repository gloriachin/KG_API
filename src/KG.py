import sys
import json
import pandas as pd
from os import stat_result
from pydantic import BaseModel
from neo4j import GraphDatabase
from typing import Optional, Dict, List, Any

# This file is inspired by BigGIM.py in the BigGIM_fastapi GitHub repository 
# Accessible at: https://github.com/gloriachin/BigGIM_fastapi/blob/main/src/BigGIM.py

class api_connect:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd), encrypted=False)
        except Exception as e:
            print("Could not create the driver", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Could'nt make the driver"
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

db = api_connect("neo4j://34.171.95.111:7687","neo4j","GeneData")

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

def parse_Query(query:Query):
    result = {}
    Drug_list = []
    gene_list = []
    Predicates_list = []
    Attribute_list = []
    Gene_id_type = ''

    Edges_query: Dict[str, EdgeParams] = query.message.query_graph.edges
    Nodes_query: Dict[str, NodeParams] = query.message.query_graph.nodes

    n00_nodes: NodeParams = Nodes_query['n00']
    n01_nodes: NodeParams = Nodes_query['n01']

    Query_Nodes0_Set = [] #Genes
    Query_Nodes1_Set = [] #Drugs
    if n00_nodes.ids is not None:
        Query_Nodes0_Set = Query_Nodes0_Set + n00_nodes.ids

    if n01_nodes.ids is not None:
        Query_Nodes1_Set  = Query_Nodes1_Set + n01_nodes.ids
 
    Query_Nodes_Set_id_transformed = set() #Genes

    for i in Query_Nodes0_Set:
        if 'SYMBOL' in i:
            Gene_id_type = 'SYMBOL'
            Query_Nodes_Set_id_transformed.add(i.split(':')[1])
        else:
            Query_Nodes_Set_id_transformed.add(i) ## Need conversation NCBIGENE

    gene_list = list(Query_Nodes_Set_id_transformed)
    print(gene_list)

    #if len(Query_Nodes1_Set) > 0:
    Drug_list = list(Query_Nodes1_Set)
    #print(gene_list)

    e00_edges: EdgeParams = Edges_query['e00']
    Query_Edge_Set = []
    Query_Edge_Set = Query_Edge_Set + e00_edges.predicates
    Query_Edge_Set = set(Query_Edge_Set)
    Predicates_list = list(Query_Edge_Set)
    print(Predicates_list)
    print(Drug_list)
    if e00_edges.attributes is not None:
        Query_Attribute_Set = e00_edges.attributes
    else:
        Query_Attribute_Set = set() 
    Attribute_list = list(Query_Attribute_Set)
    result= {"gene_List": gene_list, "Gene_id_type":Gene_id_type, "Drug_list":Drug_list, "Predicates_list":Predicates_list, "Attribute_list":Attribute_list}
    return(result)

def query_KG(query,gene_List,Gene_id_type, Drug_list,Predicates_list,Attribute_list):
    response_query={}
    gene_List_format = ["'"+ str(x) + "'" for x in gene_List]
    print(gene_List_format)
    Drug_list_format = ["'"+ str(x) + "'" for x in Drug_list]
    Predicates_list_format  = ["'"+ str(x) + "'" for x in Predicates_list]
    Cypher = ''''''

    if len(gene_List) > 0 and len(Drug_list) == 0 and len(Predicates_list) == 0:
        if Gene_id_type.upper() == 'SYMBOL' : 
                Cypher = '''
                MATCH (d:Drug)-[drugToGene]->(g:Gene)
                WHERE g.Symbol = {__Gene_list__}
                RETURN DISTINCT d, drugToGene;
                '''.format(__Gene_list__=gene_List_format)
              
        elif Gene_id_type.upper() == 'NCBI:GENEID':
                Cypher = '''
                MATCH (d:Drug)-[drugToGene]->(g:Gene)
                WHERE g.NCBI_ID = {__Gene_list__}
                RETURN DISTINCT d, drugToGene;
                '''.format(__Gene_list__=gene_List_format)
    else:
        Cypher = ''''''
    
    print(Cypher)
    result = db.query(Cypher, db='neo4j')
    
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
    result = parse_Query(json_query)
    df = query_KG(json_query, result['gene_List'], result['Gene_id_type'], result['Drug_list'],result['Predicates_list'], result['Attribute_list'])
    return(df)