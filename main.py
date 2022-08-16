import sys
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, List
from fastapi import FastAPI
from typing import Optional, Dict, List

sys.path.append('./src/')
import KG

app = FastAPI()

@app.post("/KG")
async def query_knowledge_graph(json_query: KG.Query):
    db = KG.db_connect("neo4j://34.171.95.111:7687","neo4j","GeneData")
    result = KG.Query_KG_all(json_query,db)
    return(result)