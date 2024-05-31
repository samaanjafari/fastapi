from pydantic import BaseModel, EmailStr, ValidationError, ConfigDict
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
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at: datetime
    class Config:
        from_attributes = True
    
   