from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import *
from .. import schemas, models, token, utils


router =APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalidd email or password")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password")
    
    # create token
    # return token
    access_token = token.create_access_token(data = {'user_id': user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
    