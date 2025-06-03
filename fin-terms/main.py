# ... existing code ...
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .src.serch_terms import MilvusSearcher

milvus_data_path = 'fin-terms/db/fin_data.db'
collection_name = "financial_terms"
embedding_model_name = 'all-MiniLM-L6-v2'

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

# 初始化 MilvusSearcher
try:
    searcher = MilvusSearcher(milvus_data_path, collection_name, embedding_model_name)
except Exception as e:
    print(f"MilvusSearcher 初始化失败: {e}")
    searcher = None

@app.post("/search")
async def search_terms(request: SearchRequest):
    if not searcher:
        raise HTTPException(status_code=500, detail="MilvusSearcher 未初始化。")
    try:
        results = searcher.search(request.query, request.top_k)
        return {"query": request.query, "results": results}
    except Exception as e:
        print(f"搜索过程中发生错误: {e}")
        raise HTTPException(status_code=500, detail=f"搜索失败: {e}")

@app.get("/")
async def read_root():
    return {"message": "金融术语搜索 API 运行中"}