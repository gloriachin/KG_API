# api.py
# This file connects to our Google Cloud server, and allows us to query the graphs in the instance.
# Run on the command line with: python3 -m uvicorn api:app --reload
# New queries / endpoints can be made simply by writing new functions towards the end of this file. 
# Authors: Omar Aziz, Katie Christensen

from neo4j import GraphDatabase
from fastapi import FastAPI

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
            print("The query did not complete:", e)
        finally:
            if session is not None:
                session.close()
        return response

connection = apiP("neo4j://34.171.95.111:7687","neo4j", "GeneData")
app=FastAPI()

@app.get('/')
def root():
    return {'root': 'you are in the root of the api'}

@app.get('/Genes')
async def genes(lim:int = 20):
    qString = "MATCH (g:Gene) RETURN g LIMIT  {lim}".format(lim=lim)
    return connection.query(qString, db='neo4j')

@app.get('/Drugs')
async def genes(lim:int = 20):
    qString = "MATCH (d:Drug) RETURN d LIMIT  {lim}".format(lim=lim)
    return connection.query(qString, db='neo4j')

@app.get('/GresDrug')
async def read_item(lim: int = 10, drug= str):
        qString= """
        MATCH (d:Drug)-[rel:ASSOCIATED_WITH]->(g:Gene) 
        WHERE rel.Predicate = 'biolink:associated with resistance to' AND d.Object = '{drug}'
        RETURN g limit {lim}
        """.format(lim=lim, drug=drug)
        return connection.query(qString, db='neo4j')

@app.get('/GsensitiveY')
async def count(drug: str, lim: int = 10):
        qString = """
        MATCH (d:Drug)-[rel:ASSOCIATED_WITH]->(g:Gene) 
        WHERE rel.Predicate = 'biolink:associated with sensitivity to' AND d.Object = '{drug}'
        RETURN g limit {lim}
        """.format(drug=drug, lim=lim)
        return connection.query(qString, db='neo4j')

@app.get('/DrugTGene')
async def count(lim: int = 20, gene= str):
        #qString = """
        #MATCH (d:Drug)-[rel:TARGETS]->(g:Gene) WHERE g.Target = '{gene}' RETURN d limit {lim} 
        #""".format(lim=lim, gene= gene)
        #return connection.query(qString, db='neo4j')

        qString = '''
                MATCH (d:Drug)-[drugToGene]->(g:Gene)
                WHERE g.Symbol = "TP53"
                RETURN DISTINCT d, drugToGene;
                '''.format(lim=lim)
        return connection.query(qString, db='neo4j')

@app.get('/GTargetsForDrug')
async def count(lim: int = 10, drug= str):
        qString = """
        MATCH (d:Drug)-[rel:TARGETS]->(g:Gene) WHERE d.Drug = '{drug}' RETURN g limit {lim} 
        """.format(lim=lim, drug = drug)
        return connection.query(qString, db='neo4j')

@app.get('/GwithSaR')
async def count(lim: int = 10, drug = str):
        qString = """
        MATCH (d:Drug)-[rel:TARGETS]->(g:Gene) WHERE d.Drug = '{drug}' 
        WITH d.Drug as drug, g.Target AS gene  
        MATCH (d)-[rel:ASSOCIATED_WITH]->(g) 
        WHERE rel.Predicate = 'biolink:associated with sensitivity to' AND d.Object = drug AND g.Subject = gene  
        RETURN g limit {lim}
        """.format(lim=lim, drug = drug)
        return connection.query(qString, db='neo4j')
