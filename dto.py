from pydantic import BaseModel

class TodoCreate(BaseModel):
    content: str
  
class TodoUpdate(BaseModel):
    content: str

class TodoResponse(BaseModel):
    id: int
    content: str