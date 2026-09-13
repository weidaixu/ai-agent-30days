from fastapi import FastAPI
from pydantic import BaseModel
from day03.llm_extract_test import run_agent

app = FastAPI()

@app.get("/health")
def health():
    result = {
        "status":"OK"
    }
    return result




class ChatRequest(BaseModel):
    message : str

@app.post("/test")
def test(request:ChatRequest):

    result = {
        "message":request.message
    }

    return result

@app.post("/chat")
def chat(request:ChatRequest):
    llm_response = run_agent(request.message)
    result = {
        "answer":llm_response
    }
    return result




