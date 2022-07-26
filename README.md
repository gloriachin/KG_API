# KG_API README

## Graph Database Development
Convert your CSV file into a graph database using Neo4j.

### Downloads

1. Download [Neo4j Desktop](https://neo4j.com/download/)

### Install Packages

1. No packages are needed to be installed.

#### Getting Started

1. Open Neo4j Desktop and login or create an account with either a username/password, or with an email address.
2. When you first open Neo4j Desktop, there will be an intro project with a movie database already started. You can only have one DBMS running at a time, so first thing is to click 'Stop' to end this session. After it stops, there should be a message on the top saying 'No active DBMS'.
3. Create a new project in the left-hand sidebar by clicking 'New'. This makes a new project named 'Project'. 
4. On the right-hand side of the name 'Project', there is an 'Edit' button, click this to rename your project to something more specific. Click the check mark to save the new name.
5. In your new Project, you can create as many DBMSs as you want. Go to the 'Add' button on the right-hand side of the project, and choose 'Local DBMS'. 
6. Here, you can rename your DBMS and give it a password (can be different from your Neo4j Desktop password). Then choose 'Create'.
7. Hover over your newly created DBMS and click 'Start'. It will take a moment to start, but soon you'll see a green 'Active' label.
8. Now that your DBMS is created and activated, you can access your DBMS locally from any of Neo4j's other tools, such as Bloom and Browser. You can do this by hovering over your DBMS and clicking the down arrow next to 'Open' and choosing any of the tools listed. We'll do this more later, so for now just stay in Desktop. 


#### Move your CSV Files to the Import Folder
1. Hovering over your DBMS, next to 'Open' are three grey dots. Hover over these dots, go to 'Open Folder' and from there click on 'import'. This will open the import folder of your Neo4j DBMS. 
2. Move your CSV file(s) into this folder: drag-and-drop, copy-and-paste, or if you're more comfortable in the Terminal you can use the provided path and the mv or cp commands.
3. Now that your files are in the import folder, you can begin creating the database using the Cypher query language. 

#### LOAD CSV
1. Open your favorite text editor and create a .cypher file. 
    
    i. If using Visual Studio Code, install the 'Cypher Query Language' Extension. Then, open a new file and type 'Command-K M' and choose 'Cypher Query Language' from the drop down list.
2. The first thing you will want to do is create [Constraints](https://neo4j.com/docs/cypher-manual/current/constraints/) on all of the nodes you are planning on creating.
3. Next, you will use the [LOAD CSV](https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/) command to read your CSV files and use the data to make a graph.
4. The next thing you'll want to do is visualize the architecture of your database. What properties will each Node contain? What types of relationships will be between certain Nodes? What are the properties of those certain relationships? Questions like these are easier to answer from a visualization rather than figuring them out straight in your code. I recommend using [arrows.app](https://neo4j.com/labs/arrows/), a Neo4j tool for drawing pictures of your graph.
5. Now that you have a good idea how to design your database, you are ready to write the cypher queries to turn the data to a graph. 

    i. To begin, you'll need to create the nodes and relationships. If you are sure there are no duplicate rows, you can use the CREATE command, and you can use MATCH to find existing data to do updates. But, if you are not sure whether you might have duplicates or not, especially if you are pulling data from multiple sources, then the MERGE clause is the right command. It searches if the data already exists in the graph, and if it does not exist then MERGE will create it. This is why the constraints are initialized first: an index is created on the nodes or relationships that are constrained and this helps with performance purposes when searching the graph. 

    ii. You can create nodes and relationships with labels and properties. There are a few different ways to go about doing this, one example is below using the SET command for setting properties, but [here](https://neo4j.com/docs/cypher-manual/current/syntax/) you can find more documentation on the Cypher query syntax. 

    iii. Note that all Cypher queries end with a semicolon.


```python
CREATE CONSTRAINT FOR (g:Gene) REQUIRE g.Name IS UNIQUE;
CREATE CONSTRAINT FOR (d:Drug) REQUIRE d.Name IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS 
FROM 'file:///demo.csv' AS row

MERGE (drug:Drug {Name: line.DRUG_NAME})
SET drug.Synonyms = line.Synonyms

MERGE (gene:Gene {Name: line.Target})

CREATE (drug)-[t:TARGETS]->(gene)
SET t.Disease = line.Disease,
    t.Date = line.Date,
;
```

#### Run Cypher Queries
1. Back in Neo4j Desktop, hover over your DBMS and click on the down arrow next to 'Open', choose 'Terminal'.
2. A terminal will open, here type 'bin/cypher-shell'
3. Login to your DBMS with username 'neo4j' and password is the one you set for your DBMS (not your Neo4j Desktop password).
4. Copy your Constraints from your text editor and paste them here into the terminal.
5. Once the constraints are created, copy your remaining cypher query (creating the nodes and relationships) from your text editor and paste that here into the terminal. This may take quite a few moments to run, but after a little time you will get a message saying some number of nodes, relationships, and properties were created. 
6. Type ':exit' to quit, and close the terminal.

#### Visualize and Query your Graph Database

1. In Neo4j Desktop, hover over your DBMS and click 'Open'. This will open your newly created graph database in Neo4j Browser.
    
    i. Neo4j Browser will open, and here you can query your database! First, I recommend entering ':schema' and push 'Run' (the play-arrow button). This tells you about your nodes, relationships, constraints, and other logistical information about your graph.
    
    ii. Entering 'CALL db.schema.visualization' allows you to see your nodes and relationships, similar to the visual you created earlier in arrows.app

    ii. Here you can enter any Cypher query you want. Refer to the Cypher [documentation](https://neo4j.com/docs/cypher-manual/current/syntax/) for writing these queries. 

2. In Neo4j Desktop, hover over your DBMS and click the down arrow next to 'Open', choose 'Neo4j Bloom'.

    i. Neo4j Bloom will open, and here you can visualize your database even better! You can enter Node labels to see just those specific nodes, you can enter nodes and the relationship labels between them to visualize those relationships, you can even zoom in close to see the actual labels and clicking on the nodes and relationships will bring up their properties. 

    ii. This is helpful for double checking that your Cypher code for creating the database was correct, and the graph is actually designed the way you intended it to be.


#### Future Steps
Future steps include exporting the database to an external platform, such as Google Cloud. 

#### Additional Links
If further explanation is needed, follow [this](https://neo4j.com/developer/desktop-csv-import/#loadcsv-desktop) tutorial from Neo4j for more help. 

Here is a useful [link](https://neo4j.com/docs/) to the documentation for all of Neo4j's different tools and the Cypher query language. 

## API Development
Query your database with this API guide.

### Downloads 
1. Download [Python3](https://www.python.org/downloads/)

### Install Packages

1. pip3 install neo4j
2. pip install "fastapi[all]"

#### Getting Started
1. Make sure to have your database username, uri, and password, as they are essential to connecting your database with a python script in order to query the database.

2. Download/install FastAPI and uvicorn in one go, as shown above. This is the framework used to make the api.

    ii. Uvicorn will display the api on localhost


#### Connect Script to Database
To connect your python script to the database, you need to include this code below:



```python
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
```

This is the class that connects you to the database. Below this, create an instance of that class and store it as a variable:


```python
connection = apiP("your uri","neo4j","your password") 
#put your info right here on top
```

This is where you need to have your password and uri on hand. Input those as parameters to the instance in order to connect to the database.

Once your done with that, you need to create an instance of FastAPI:


```python
app=FastAPI()
```

Now you can start making API endpoints. Here is one example: 


```python
@app.get('/')
def root():
    return {'root': 'you are in the root of the api'}
```

@app.get('/') dictates what the endpoint path will be. Just a slash indicates the root of the API.

You need to add paths that are meaningful to the information that will be displayed. 

Now, to query the database and display that information in the API, follow the code below:


```python
@app.get('/Genes')
async def genes(lim:int = 20):
    qString = "match (g:Gene) return g limit  {lim}".format(lim=lim)
    return {"Genes": connection.query(qString, db='neo4j')}
```

We use our class instance that we made earlier to query the database. 

connection.query(###) queries the database, though you need to insert two parameters: the name of the database, and the query code itself. 

In this example, the query code is stored in the variable called 'qSrtring'. At the end of that string there is a .formart(lim=lim), this is to tell the code that the lim inside the curly braces is a variable. 

The  variable lim is passed in through the parameter of the function itself. In this example, the function is called 'genes'. For your case, lim is the limit of response you want to get back form the query. The default amount is set to 20, you can change this when you add a '?lim= ' and set equals to some number. That number will be the new number of responses you get back from the query.   

#### Additional Links

If you have any further questions, here are [one](https://neo4j.com/developer/python/), [two](https://neo4j.com/docs/api/python-driver/current/api.html) links to Neo4j resources that may help with using Neo4j from Python and of Neo4j API documentation.
