# Implementation of graph based API to expose knowledge graphs.

### How to use the API as it is now:

1. In terminal, navigate to the home of this repository and enter:

python3 -m uvicorn main:app --reload

2. When you run this a URL will be provided, copy and paste that into a search engine. Add to the end of the URL "/docs" and hit enter. Your URL should look something like: http://127.0.0.1:8000/docs

3. FastAPI user interface will open. Click on the green POST bar.

4. Click "Try it out"

5. Enter any json query into the "Request body" box. (This repository contains example json queries you could enter. Navigate to the docs/example_queries directory, and choose the json_queries notebook. Copy and paste any of these.)

6. Click "Execute" and scroll down to the "Responses" to see the results of your query.

### Summary of Current API

As of right now, the API only handles direct-relationship queries. For example, "What are the drugs approved to treat the disease Acute Myeloid Leukemia?" is a question that the current API can handle because drug and disease nodes share a common, direct, relationship (edge) between them in the graph database. This pattern is the same for gene-to-gene and drug-to-gene queries.

### Future Steps

Future steps include creating additional endpoints that would handle indirect-relationship queries, those that require multiple hops. For example, "What are the gene targets of the disease Acute Myeloid Leukemia?" is a question that we hope to be able to handle in the future. Gene and disease nodes do not share a direct relationship (edge) between them, so this query requires an additional step to find that middle connection, in this case a drug node. So, future goals include writing endpoints to handle such cases.

### Formatting Knowledge
To view the files on knowledge standardization, navigate to the database_formatting directory.

### Graph Database

To read about how the graph database was created, navigate to the docs/README_notebooks directory and choose the graph_database_development notebook.

To view the files on graph database development, navigate to the create_graph_db directory.

### API Development

To read about how the API was developed, navigate to the docs/README_notebooks directory and choose the api_development notebook.

To view the files on API development, see main.py in the home of this repository, and navigate to the src directory. 
