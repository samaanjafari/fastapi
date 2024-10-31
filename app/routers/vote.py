from fastapi import Body, FastAPI , Response , status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from  ..database import get_db
from .posts import *

router = APIRouter(prefix="/vote",
                   tags=['Vote'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    

    
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {vote.post_id} does not exist")
    
    
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir== 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f"user {current_user.id} already voted for {vote.post_id}")
            
        new_vote = models.Vote(post_id = vote.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Vote does not exist.")    
            
        vote_query.delete()
        db.commit()
        return {"message": "successfully deleted vote!"}
    #we can implement it this logic in another way which there is no vote_direction in that way
    #and actually it is how real applications right now like instagram facebook and,... works.
    #it just check if there was a vote already on that post we we will delete it and if there is not we gonna add that vote and like.
    #That is exactly how instagram like buttom or toggle like works.