from pydantic import BaseModel, EmailStr, ValidationError, ConfigDict, conint, Field
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
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
    
class PostBase(BaseModel):
    title: str
    content: str    
    published: bool = True
    #rating: Optional[int] = None
    
class PostCreate(PostBase):
    pass
    '''why we are not adding owner_id to our requirement schema for creating post is that we already
    know that the user is logged in cuz by passing oauth2 dependency to our path parameters 
    it will handle the authentication process and we have it already.'''


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut 
    class Config:
        from_attributes = True
''' the intersting part of this line owner: UserOut was
    we had our user schema logic under and after post schemas but cuz python is interperter language
    and not doesn't have any compiler if you haven't define something before u can't use it
    so we had to change postion of classes and move user schema functions beforehand'''
class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    #we just create this schema after implementing vote and post join tables 
        
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenPayload(BaseModel):
    id: Optional[int] = None
    
    
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]
    
   