from pydantic import BaseModel
from datetime import datetime
class PostBase(BaseModel):
    title: str
    content: str    
    published: bool = True
    #rating: Optional[int] = None
    
class PostCreate(PostBase):
    pass


class Response(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True