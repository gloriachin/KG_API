#!/usr/bin/env python3 

from neo4j import GraphDatabase

class ConnectGraphDatabase:
    def __init__(self, uri, user, password):
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=True, trust='TRUST_ALL_CERTIFICATES')
        except Exception as e:
            print("Could not create the driver", e)
        
    def close(self):
        if self.driver is not None:
            self.driver.close()
        
    def query(self, query, db=None):
        assert self.driver is not None, "The driver was not fully initialized"
        session = None
        response = None
        try: 
            session = self.driver.session(database=db) if db is not None else self.driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("The query did not complete:", e)
        finally: 
            if session is not None:
                session.close()
        return response

def main():
    uri = "bolt://34.133.105.26:7687"  #external IP
    #uri = 'bolt://10.128.0.8:7687'    #internal IP
    user = "neo4j"
    password = 'GeneData'

    connection = ConnectGraphDatabase(uri, user, password)

    constraint_query= 'CREATE CONSTRAINT FOR (g:Gene) REQUIRE g.Symbol IS UNIQUE;'

    db_query= 'USING PERIODIC COMMIT \
        LOAD CSV WITH HEADERS \
        FROM \'http://localhost:11001/project-0a7bc7c9-e50c-47f3-aefe-52d0ae166a1e/edges_test.csv\' AS row \
        MERGE (subject:Gene {Symbol: row.subject_symbol}) \
        SET subject.ID = row.subject_id, \
            subject.Prefixes = row.subject_id_prefixes, \
            subject.Category = row.subject_category \
        MERGE (object:Gene {Symbol: row.object_symbol}) \
        SET object.ID = row.object_id, \
            object.Prefixes = row.object_id_prefixes, \
            object.Category = row.object_category \
        CREATE (subject)-[p:ASSOCIATION]->(object) \
        SET p.Name = row.predicate, \
            p.Publications = row.ASSOCIATION_Publications \
        ;'
    
    connection.query(constraint_query, db='neo4j')
    connection.query(db_query, db='neo4j')

if __name__ == "__main__":
    main()