from neo4j import GraphDatabase

class ConnectGraphDatabase:
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

def main():
    uri = "bolt://34.133.105.26:7687"
    user = "neo4j"
    password = 'your password here'

    connection = ConnectGraphDatabase(uri, user, password)

    qString= """
        MATCH (g:Gene) RETURN g
        """.format(gene=gene)
    
    connection.query(qString, db='neo4j')

if __name__ == "__main__":
    main()