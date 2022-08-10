import sys
import uvicorn
from flask import request
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, List

# This file is from the BigGIM_fastapi GitHub repository 
# Accessible at: https://github.com/gloriachin/BigGIM_fastapi/blob/main/main.py
# Modified the last function at the end of the file.


#sys.path.append('./src/')
import KG

app = FastAPI()


#@app.post("/BigGIM/DrugTarget")
#async def BigGIM_DrugTarget(json_query: BigGIM_DT.Query):
#    print(json_query)
#    result = BigGIM_DT.BigGim_Target_Drug_interaction(json_query)
#    return(result)

#@app.post("/BigGIM/GTEx")
#async def BigGIM_GTEx(json_query: BigGIM_GTEx_lib.Query):
#    print(json_query)
#    result = BigGIM_GTEx_lib_sqlite3.BigGim_GTEx_co_expr(json_query)
#    return result

#@app.post("/BigGIM/DrugResponseKP_mut")
#def BigGIM_drKP_mut(json_query:BigGIM_DrugResponseKP_Mut.Query):
#    print(json_query)
#    result = BigGIM_DrugResponseKP_Mut.BigGim_DrugResponse_mut(json_query)
#    return(result)

#@app.post("/BigGIM/DrugResponseKP_expr")
#def BigGIM_drKP_expr(json_query:BigGIM_DrugResponseKP_Expr.Query):
#    print(json_query)
#    result = BigGIM_DrugResponseKP_Expr.BigGim_DrugResponse_expr(json_query)
#    return(result)

@app.post("/BigGIM/DrugResponse")
async def KG_drKP(json_query: KG.Query):
    print(json_query)
    #result = BigGIM.Query_bigGIM_all(json_query)
    result = KG.query_KG(json_query)
    return(result)