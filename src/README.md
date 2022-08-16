How to use our API right now:


1) In the terminal, navigate to the src directory of this repo and enter:


python3 -m uvicorn main:app --reload


2) Click on the URL that is provided, or copy/paste it into your search engine. Type "/docs" to the end of the URL and hit enter. Should look something like: http://127.0.0.1:8000/docs

3) FastAPI user interface will open, click on the green POST bar

4) Click "Try it out"

5) Enter this json query in the "Request body"

{
    "message": {
      "query_graph": {
        "edges": {
          "e00": {
            "subject": "n00",
            "object": "n01",
            "predicates": [
              "biolink:physically_interacts_with"
            ]
          }
        },
        "nodes": {
          "n00": {
            "categories": [
              "biolink:Gene"
            ],
            "ids": [
              "Symbol:\"TP53\""
            ]
          },
          "n01": {
            "categories": [
              "biolink:Gene"
            ],
            "ids": [
              "Symbol:\"BCL2\""
            ]
          } 
        }
      }
    }
  }
  

6) Click "Execute", scroll down to "Responses", and see the results of the query! 
