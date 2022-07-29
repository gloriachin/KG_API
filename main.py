from neo4j import GraphDatabase
from fastapi import FastAPI
class apiP:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
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
    

connection = apiP("neo4j+s://31d29394.databases.neo4j.io","neo4j","hn6p3tQaDFPWemO1JzDnGd0PrzXOWN62uv2hYKihP7g") 

app=FastAPI()

@app.get('/')
def root():
    return {'root': 'you are in the root of the api'}
@app.get('/GresDrug')
async def read_item(lim: int = 10, drug= str):
        qString= """
        match (d:Drug)-[rel:Predicate]->(g:Gene) 
        where rel.Predicate = 'biolink:associated with resistance to' and d.Object = '{drug}'
        return g limit {lim}
        """.format(lim=lim, drug=drug)
    
        result = connection.query(qString, db='neo4j')
        return {"Genes": result} ## this works fine 1
@app.get('/GsensitiveY')
async def count(drug: str, lim: int = 10):
        qString = """
        match (d:Drug)-[rel:Predicate]->(g:Gene) 
        where rel.Predicate = 'biolink:associated with sensitivity to' and d.Object = '{drug}'
        return g limit {lim}
        """.format(drug=drug, lim=lim)
        return {"Genes": connection.query(qString, db='neo4j')}
@app.get('/DrugTGene')
async def count(lim: int = 20, gene= str):
        qString = """
        match (d:Drug)-[rel:Targets]->(g:Gene) where g.Target = '{gene}' return d limit {lim} 
        """.format(lim=lim, gene= gene)
        return {"Drugs": connection.query(qString, db='neo4j')}
@app.get('/GTargetsForDrug')
async def count(lim: int = 10, drug= str):
        qString = """
        match (d:Drug)-[rel:Targets]->(g:Gene) where d.Drug = '{drug}' return g limit {lim} 
        """.format(lim=lim, drug = drug)
        return {"Genes": connection.query(qString, db='neo4j')} 
@app.get('/GwithSaR')
async def count(lim: int = 10, drug = str):
        qString = """
        match (d:Drug)-[rel:Targets]->(g:Gene) where d.Drug = '{drug}' 
        with d.Drug as drug, g.Target as gene  
        match (d:Drug)-[rel:Predicate]->(g:Gene) 
        where rel.Predicate = 'biolink:associated with sensitivity to' and d.Object = drug and g.Subject = gene  
        return g limit {lim}
        """.format(lim=lim, drug = drug)
        return {"Genes": connection.query(qString, db='neo4j')}
@app.get('/Genes')
async def genes(lim:int = 20):
    qString = "match (g:Gene) return g limit  {lim}".format(lim=lim)
    return {"Genes": connection.query(qString, db='neo4j')}
@app.get('/Drugs')
async def genes(lim:int = 20):
    qString = "match (d:Drug) return d limit  {lim}".format(lim=lim)
    return {"Drugs": connection.query(qString, db='neo4j')}
# match (d:Drug)-[rel:Targets]->(g:Gene) where d.Drug = 'Paclitaxel' with d.Drug as drug, g.Target as gene  match (d:Drug)-[rel:Predicate]->(g:Gene) where rel.Predicate = 'biolink:associated with sensitivity to' and d.Object = drug and g.Subject = gene  return g limit 10