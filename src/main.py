from fastapi import FastAPI
from pydantic import BaseModel
from langchain_utils import invoke_chain

app = FastAPI()

# Define request schema
class QueryRequest(BaseModel):
    question: str
    messages: list = []  # Chat history

@app.post("/nl2sql/")
async def get_sql(query: QueryRequest):
    response = invoke_chain(query.question, query.messages)
    return {"sql_query": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
