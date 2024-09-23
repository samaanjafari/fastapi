from pydantic import BaseModel, EmailStr, ValidationError, ConfigDict
from datetime import datetime
from typing import Optional
class PostBase(BaseModel):
    title: str
    content: str    
    published: bool = True
    #rating: Optional[int] = None
    
class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    
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
        

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenPayload(BaseModel):
    id: Optional[int] = None
    
   