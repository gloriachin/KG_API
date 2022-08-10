import sys
import json
import sqlite3
import pandas as pd
from os import stat_result
from pydantic import BaseModel
from neo4j import GraphDatabase
from typing import Optional, Dict, List, Any

# This file is from the BigGIM_fastapi GitHub repository 
# Accessible at: https://github.com/gloriachin/BigGIM_fastapi/blob/main/src/BigGIM.py
# Modified MySQL queries to be in the Cypher query language and the connection to our knowledge graph database. 

#sys.path.append('~/Documents/Softwares/SQLite/sqlite')

class apiP:
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
        assert self.__driver is not None, "The driver was not fully initialized"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("The Query did not complete:", e)
        finally: 
            if session is not None:
                session.close()
        return response

db = apiP("neo4j://34.171.95.111:7687","neo4j","GeneData") 

# db = sqlite3.connect("./KGs/BigGIM.db",check_same_thread=False)

#TRAPI standard: https://github.com/NCATSTranslator/ReasonerAPI

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
    #log_level: str
    #workflow: str

# class Names:
#     Names:str
# class MetaAttribute:
#     attribute_type_id: str
#     attribute_soure:str
#     original_attribute_names: list[Names]
#     constraint_use:bool
#     constraint_name: str
# class MetaEdge:
#     subject: str #BiolinkEntity
#     predicte: str # BiolinkPredicate
#     object: str #BiolinkEntity
#     attributes: MetaAttribute
# class MetaNode(BaseModel):
#     id_prefixes:str
#     attributes:list[MetaAttribute]
# class MetaKnowledgeGraph(BaseModel):
#     nodes:Dict[str, MetaNode]
#     edges: list[MetaEdge]

def query_KG(query:Query):
    
    Edges_query: Dict[str, EdgeParams] = query.message.query_graph.edges
    Nodes_query: Dict[str, NodeParams] = query.message.query_graph.nodes
    #print(Nodes_query)
    n00_nodes: NodeParams = Nodes_query['n00']
    n01_nodes: NodeParams = Nodes_query['n01']
    e00_edges: EdgeParams = Edges_query['e00']
    #print(n00_nodes)
    n00_nodes.ids #Gene_list
    #print(n00_nodes.ids)
    n00_nodes.categories #
    n01_nodes.ids #Drug_list
    n01_nodes.categories
    e00_edges.predicates #Predicates_list
    #response_query={}

    if (n00_nodes.ids) is not None:
        gene_List_format = ["'"+ str(x).split(':')[1] + "'" for x in n00_nodes.ids]
    if (n01_nodes.ids) is not None:
        Drug_list_format = ["'"+ str(x) + "'" for x in n01_nodes.ids]
    if (e00_edges.predicates) is not None:
        Predicates_list_format  = ["'"+ str(x) + "'" for x in e00_edges.predicates]

    #print(gene_List_format)
    #print(Drug_list_format)
    #print(Predicates_list_format)
    if (n00_nodes.ids) is not None and (("biolink:associated_with_resistance_to" in e00_edges.predicates) or ('biolink:associated_with_sensitivity_to' in  e00_edges.predicates)):
        Gene_id_type = n00_nodes.ids[0].split(":")[0]
        if (n01_nodes.ids) is not None:
            if Gene_id_type.upper() == 'SYMBOL' : 
                Cypher = '''
                MATCH (g:Gene)-[rel]-(d:Drug)
                WHERE g.Symbol IN {__Gene_list__} AND d.Name IN {__Drug_list__} AND type(rel) IN {_Predicates_list_}
                RETURN g, d, rel
                '''.format(__Gene_list__=gene_List_format, __Drug_list__=Drug_list_format, _Predicates_list_=Predicates_list_format)
                # select * 
                # from Table_DrugResponse_KP
                # where (Subject_Approved_symbol IN (__Gene_list__) and Object IN (__Drug_list__)) and Predicate in (_Predicates_list_)

                # Cypher = Cypher.replace('_Predicates_list_' ,','.join(Predicates_list_format ))
                # Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))
                # Cypher = Cypher.replace('__Drug_list__' ,','.join(Drug_list_format))

            elif Gene_id_type.upper() == 'NCBI:GENEID':
                Cypher = '''
                MATCH (g:Gene)-[rel]-(d:Drug)
                WHERE g.NCBI_ID IN {__Gene_list__} AND d.Name IN {__Drug_list__} AND type(rel) IN {_Predicates_list_}
                RETURN g, d, rel
                '''.format(__Gene_list__=gene_List_format, __Drug_list__=Drug_list_format, _Predicates_list_=Predicates_list_format)
                # select * 
                # from Table_DrugResponse_KP 
                # where (Subject_NCBI_Gene_ID IN (__Gene_list__) and Object IN (__Drug_list__)) and Predicate in (_Predicates_list_)
                
                # Cypher = Cypher.replace('_Predicates_list_' ,','.join(Predicates_list_format))
                # Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))
                # Cypher = Cypher.replace('__Drug_list__' ,','.join(Drug_list_format))
        else:
            if Gene_id_type.upper() == 'SYMBOL' : 
                Cypher = '''
                MATCH (g:Gene)-[rel]-()
                WHERE g.Symbol IN {__Gene_list__} AND type(rel) IN {_Predicates_list_}
                RETURN g, rel
                '''.format(__Gene_list__=gene_List_format, _Predicates_list_=Predicates_list_format)
                # select * 
                # from Table_DrugResponse_KP 
                # where (Subject_Approved_symbol IN (__Gene_list__) and Predicate in (_Predicates_list_))
 
                # Cypher = Cypher.replace('_Predicates_list_' ,','.join(Predicates_list_format))
                # Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))

            elif Gene_id_type.upper() == 'NCBI:GENEID':
                Cypher = '''
                MATCH (g:Gene)-[rel]-(d:Drug)
                WHERE g.NCBI_ID IN {__Gene_list__} AND type(rel) IN {_Predicates_list_}
                RETURN g, rel
                '''.format(__Gene_list__=gene_List_format, _Predicates_list_=Predicates_list_format)
                # select * 
                # from Table_DrugResponse_KP 
                # where (Subject_NCBI_Gene_ID IN (__Gene_list__)  and Predicate in (_Predicates_list_)
                 
                # Cypher = Cypher.replace('_Predicates_list_' ,','.join(Predicates_list_format))
                # Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))

    elif n01_nodes.ids is not None and (("biolink:associated_with_resistance_to" in e00_edges.predicates) or ('biolink:associated_with_sensitivity_to' in  e00_edges.predicates)):    
        Cypher = '''
                MATCH (d:Drug)-[rel]-()
                WHERE d.Name IN {__Drug_list__} AND type(rel) IN {_Predicates_list_}
                RETURN d, rel
                '''.format(__Drug_list__=Drug_list_format, _Predicates_list_=Predicates_list_format)
        # select * 
        #         from Table_DrugResponse_KP 
        #         where Object IN (__Drug_list__) and Predicate in (_Predicates_list_)

        # Cypher = Cypher.replace('_Predicates_list_' ,','.join(Predicates_list_format))
        # Cypher = Cypher.replace('__Drug_list__' ,','.join(Drug_list_format))

    elif (n00_nodes.ids is not None ) and (n01_nodes.ids is not None): 
        print("Test2")
        Gene_id_type = n00_nodes.ids[0].split(":")[0]
        if Gene_id_type.upper() == 'SYMBOL' : 
            Cypher = '''
                MATCH (g:Gene)-[rel]->(d:Drug)
                WHERE g.Symbol IN {__Gene_list__} AND d.Name in {__Drug_list__}
                RETURN g, d
                '''.format(__Drug_list__=Drug_list_format, __Gene_list__=gene_List_format)
            # select * 
            # from Table_DrugResponse_KP 
            # where (Subject_Approved_symbol IN (__Gene_list__) and Object IN (__Drug_list__)) 
            
            # Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))
            # Cypher = Cypher.replace('__Drug_list__' ,','.join(Drug_list_format))
        
        elif Gene_id_type.upper() == 'NCBI:GENEID' : 
            Cypher = '''
                MATCH (g:Gene)-[]-(d:Drug)
                WHERE g.NCBI_ID IN {__Gene_list__} AND d.Name IN {__Drug_list__}
                RETURN g, d
                '''.format(__Drug_list__=Drug_list_format, __Gene_list__=gene_List_format)
            # select * 
            #     from Table_DrugResponse_KP 
            #     where (Subject_NCBI_Gene_ID IN (__Gene_list__) and Object IN (__Drug_list__)) 
             
            # Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))
            # Cypher = Cypher.replace('__Drug_list__' ,','.join(Drug_list_format))
    else:
        Cypher = ''''''
    
    print(Cypher)
    mysele = db.execute(Cypher)
    result = mysele.fetchall()
    #print(result)
    response_message = {}
    # "Subject":words[0],
    # "Subject_Ensembl_gene_ID": words[1],
    # "Subject_NCBI_Gene_ID":words[2],
    # "Subject_Approved_symbol":words[3],
    # "Subject_Category":words[4],
    # "Object":words[5],
    # "Object_name":words[6],
    # "Object_id":words[7],
    # "Object_Category":words[8],
    # "Predicate":words[9],
    # "Edge_attribute_Subject_Modifier":words[10],
    # "Edge_attribute_Object_Modifier":words[11],
    # "Edge_attribute_method":words[12],
    # "Edge_attribute_Pvalue":words[13],
    # "Edge_attribute_evidence_type":words[14],
    # "Edge_attribute_evidence_value":words[15],
    # "Edge_attribute_sample_size":words[16],
    # "Edge_attribute_sample_orign":words[17],
    # "Edge_attribute_MONDO_ID":words[18],
    # "Edge_attribute_DataResource":words[19],
    # "Edge_attribute_Publication":words[20],
    # "Edge_attribute_Provider":words[21]
    

    response_message['query_graph'] = query
    response_message['results'] = []
    knowledge_graph_nodes = {}
    knowledge_graph_edges = {}
    response_message['knowledge_graph'] = {}
    
    response_message['knowledge_graph']['edges'] = {}
    response_message['knowledge_graph']['nodes'] = {}

    for words in result:
        response_message['knowledge_graph']['nodes'][words[2]] =  {"name": words[0],"categories":words[4]},
        response_message['knowledge_graph']['nodes'][words[7]] =  {"name": words[6], "categories":words[8]}
        response_message['knowledge_graph']['edges'][words[2] + "-" +words[7]] = {"subject":words[2], 
                                                                                  "predicate":words[9], 
                                                                                  "object": words[7],
                                                                                  "edge_attributes": {"Edge_attribute_Subject_Modifier":words[10],
                                                                                                    "Edge_attribute_Object_Modifier":words[11],
                                                                                                    "Edge_attribute_method":words[12],
                                                                                                    "Edge_attribute_Pvalue":words[13],
                                                                                                    "Edge_attribute_evidence_type":words[14],
                                                                                                    "Edge_attribute_evidence_value":words[15],
                                                                                                    "Edge_attribute_sample_size":words[16],
                                                                                                    "Edge_attribute_sample_orign":words[17],
                                                                                                    "Edge_attribute_MONDO_ID":words[18],
                                                                                                    "Edge_attribute_DataResource":words[19],
                                                                                                    "Edge_attribute_Publication":words[20],
                                                                                                    "Edge_attribute_Provider":words[21]}
                                                                                    }

    response = {}
    #response["message"] = {}
    response["message"] = response_message
    return(response)

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

def query_bigGIM(query,gene_List,Gene_id_type, Drug_list,Predicates_list,Attribute_list):
    response_query={}
    gene_List_format = ["'"+ str(x) + "'" for x in gene_List]
    print(gene_List_format)
    Drug_list_format = ["'"+ str(x) + "'" for x in Drug_list]
    Predicates_list_format  = ["'"+ str(x) + "'" for x in Predicates_list]
    Cypher = ''''''

    if len(gene_List) > 0 and (("biolink:associated_with_resistance_to" in Predicates_list) or ('biolink:associated_with_sensitivity_to' in  Predicates_list)):
        if len(Drug_list) > 0:
            if Gene_id_type.upper() == 'SYMBOL' : 
                Cypher = '''
                MATCH (g:Gene)-[rel]-(d:Drug)
                WHERE g.Symbol IN {__Gene_list__} AND d.Name IN {__Drug_list__} AND type(rel) IN {_Predicates_list_}
                RETURN g, d, rel
                '''.format(__Gene_list__=gene_List_format, __Drug_list__=Drug_list_format, _Predicates_list_=Predicates_list_format)
                # select * 
                # from Table_DrugResponse_KP 
                # where (Subject_Approved_symbol IN (__Gene_list__) and Object IN (__Drug_list__)) and Predicate in (_Predicates_list_)

                # Cypher = Cypher.replace('_Predicates_list_' ,','.join(Predicates_list_format ))
                # Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))
                # Cypher = Cypher.replace('__Drug_list__' ,','.join(Drug_list_format))

            elif Gene_id_type.upper() == 'NCBI:GENEID':
                Cypher = '''
                MATCH (g:Gene)-[rel]-(d:Drug)
                WHERE g.NCBI_ID IN {__Gene_list__} AND d.Name IN {__Drug_list__} AND type(rel) IN {_Predicates_list_}
                RETURN g, d, rel
                '''.format(__Gene_list__=gene_List_format, __Drug_list__=Drug_list_format, _Predicates_list_=Predicates_list_format)
                # select * 
                # from Table_DrugResponse_KP 
                # where (Subject_NCBI_Gene_ID IN (__Gene_list__) and Object IN (__Drug_list__)) and Predicate in (_Predicates_list_)
                
                # Cypher = Cypher.replace('_Predicates_list_' ,','.join(Predicates_list_format))
                # Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))
                # Cypher = Cypher.replace('__Drug_list__' ,','.join(Drug_list_format))

        else:
            if Gene_id_type.upper() == 'SYMBOL' : 
                Cypher = '''
                MATCH (g:Gene)-[rel]-()
                WHERE g.Symbol IN {__Gene_list__} AND type(rel) IN {_Predicates_list_}
                RETURN g, rel
                '''.format(__Gene_list__=gene_List_format, _Predicates_list_=Predicates_list_format)
                # select * 
                # from Table_DrugResponse_KP 
                # where (Subject_Approved_symbol IN (__Gene_list__) and Predicate in (_Predicates_list_))

                # Cypher = Cypher.replace('_Predicates_list_' ,','.join(Predicates_list_format))
                # Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))

            elif Gene_id_type.upper() == 'NCBI:GENEID':
                Cypher = '''
                select * 
                from Table_DrugResponse_KP 
                where (Subject_NCBI_Gene_ID IN (__Gene_list__)  and Predicate in (_Predicates_list_)
                '''

                Cypher = Cypher.replace('_Predicates_list_' ,','.join(Predicates_list_format))
                Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))

    elif len(Drug_list) > 0 and (("biolink:associated_with_resistance_to" in Predicates_list) or ('biolink:associated_with_sensitivity_to' in  Predicates_list)):    
        Cypher = '''
                MATCH (d:Drug)-[rel]-()
                WHERE d.Name IN {__Drug_list__} AND type(rel) IN {_Predicates_list_}
                RETURN d, rel
                '''.format(__Drug_list__=Drug_list_format, _Predicates_list_=Predicates_list_format)
        # select * 
        # from Table_DrugResponse_KP 
        # where Object IN (__Drug_list__) and Predicate in (_Predicates_list_)

        # Cypher = Cypher.replace('_Predicates_list_' ,','.join(Predicates_list_format))
        # Cypher = Cypher.replace('__Drug_list__' ,','.join(Drug_list_format))

    elif len(Drug_list) > 0 and len(gene_List) > 0:
        print("Test2")
        if Gene_id_type.upper() == 'SYMBOL' : 
            Cypher = '''
                MATCH (g:Gene)-[rel]->(d:Drug)
                WHERE g.Symbol IN {__Gene_list__} AND d.Name in {__Drug_list__}
                RETURN g, d
                '''.format(__Drug_list__=Drug_list_format, __Gene_list__=gene_List_format)
            # select * 
            # from Table_DrugResponse_KP 
            # where (Subject_Approved_symbol IN (__Gene_list__) and Object IN (__Drug_list__)) 
            
            # Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))
            # Cypher = Cypher.replace('__Drug_list__' ,','.join(Drug_list_format))
        
        elif Gene_id_type.upper() == 'NCBI:GENEID' : 
            Cypher = '''
                MATCH (g:Gene)-[]-(d:Drug)
                WHERE g.NCBI_ID IN {__Gene_list__} AND d.Name IN {__Drug_list__}
                RETURN g, d
                '''.format(__Drug_list__=Drug_list_format, __Gene_list__=gene_List_format)
            # select * 
            # from Table_DrugResponse_KP 
            # where (Subject_NCBI_Gene_ID IN (__Gene_list__) and Object IN (__Drug_list__)) 
            
            # Cypher = Cypher.replace('__Gene_list__' ,','.join(gene_List_format))
            # Cypher = Cypher.replace('__Drug_list__' ,','.join(Drug_list_format))

        
    else:
        Cypher = ''''''
    
    print(Cypher)
    mysele = db.execute(Cypher)
    result = mysele.fetchall()
    
    response_query["message"] = {"query_graph":query.message.query_graph,

                                "knowledge_graph":{"edges":{},
                                                    "nodes":{}}, 
                                "results":{}}

    for words in result:
        response_query['message']['knowledge_graph']['edges'][words[0] + "-"+words[9] + "-" + words[5]] = {
                                                                                    "Subject":words[0],
                                                                                    "Subject_Ensembl_gene_ID": words[1],
                                                                                    "Subject_NCBI_Gene_ID":words[2],
                                                                                    "Subject_Approved_symbol":words[3],
                                                                                    "Subject_Category":words[4],
                                                                                    "Object":words[5],
                                                                                    "Object_name":words[6],
                                                                                    "Object_id":words[7],
                                                                                    "Object_Category":words[8],
                                                                                    "Predicate":words[9],
                                                                                    "Edge_attribute_Subject_Modifier":words[10],
                                                                                    "Edge_attribute_Object_Modifier":words[11],
                                                                                    "Edge_attribute_method":words[12],
                                                                                    "Edge_attribute_Pvalue":words[13],
                                                                                    "Edge_attribute_evidence_type":words[14],
                                                                                    "Edge_attribute_evidence_value":words[15],
                                                                                    "Edge_attribute_sample_size":words[16],
                                                                                    "Edge_attribute_sample_orign":words[17],
                                                                                    "Edge_attribute_MONDO_ID":words[18],
                                                                                    "Edge_attribute_DataResource":words[19],
                                                                                    "Edge_attribute_Publication":words[20],
                                                                                    "Edge_attribute_Provider":words[21],
                                                                                     }
    return(response_query)


def Query_bigGIM_all(json_query):
    result = parse_Query(json_query)
    df = query_bigGIM(json_query, result['gene_List'], result['Gene_id_type'], result['Drug_list'],result['Predicates_list'], result['Attribute_list'])
    return(df)