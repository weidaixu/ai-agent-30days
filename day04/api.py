from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from day03.llm_extract_test import run_agent
import logging
logger = logging.getLogger("uvicoen.error")
app = FastAPI()

@app.get("/health")
def health():
    result = {
        "status":"day05"
    }
    return result




class ChatRequest(BaseModel):
    message : str

class ChatResponse(BaseModel):
    answer : str

@app.post("/test")
def test(request:ChatRequest):

    result = {
        "message":request.message
    }

    return result

@app.post("/chat",response_model = ChatResponse)
def chat(request:ChatRequest):
    logger.info("收到/chat请求")
    message = request.message.strip()  

    if not message:
        raise HTTPException(
            status_code = 400,
            detail = "message 不能为空"    
        )
        
    try:
        llm_response = run_agent(message)
        
    except Exception as error:
        logger.exception("Agent 执行失败")
        raise HTTPException(
            status_code=500,
            detail="Agent 服务执行失败"
        )
    result = {
        "answer":llm_response
    }
    return result


