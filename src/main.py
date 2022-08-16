import sys
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, List
from fastapi import FastAPI
from typing import Optional, Dict, List

# run this file with: python3 -m uvicorn main:app --reload

import KG

app = FastAPI()

#json_query = {"message": { "query_graph": { "edges": { "e00": { "object": "n01", "predicates": [ "biolink:targets" ], "subject": "n00" } }, "nodes": { "n00": { "categories": [ "biolink:Gene", ], "ids": [ "TP53" ],}, "n01": { "categories": [ "biolink:Drug"],}}}}}

@app.post("/KG")
async def KG_drKP(json_query: KG.Query):
    print(json_query)
    result = KG.Query_KG_all(json_query)
    return(result)