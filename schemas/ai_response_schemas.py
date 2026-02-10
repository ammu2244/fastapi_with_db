
from pydantic import BaseModel

class AIRequest(BaseModel):
    message:str
    system_prompt:str="you are a helpful assistant"

class AIResponse(BaseModel):
    response:str