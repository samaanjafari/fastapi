from .. import models, schemas
from fastapi import Body, FastAPI , Response , status , HTTPException, Depends, APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)

@router.get("/", response_model= List[schemas.Response])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #print(posts)
    posts = db.query(models.Post).all()
    return  posts

 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def create_post(post : schemas.PostCreate, db: Session = Depends(get_db)):   
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  """
    #                , (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(post)
    new_post = models.Post(**post.model_dump())
    '''we are using post.dict() and we unpack it with **kwargs method and it automatically fill our
    need columns and put it into right place and we do not have to fill it manually anymore every
    column'''
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@router.get("/{id}", response_model= schemas.Response)
def get_post(id: int , db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = (%s) """ , (str(id),))
    '''the comma after str(id), is for if we don't pass that comma it doesn't different from
    a single regular variable in parentheses and we have to pass tuple or a list to avoid 
    sql injection so we have to pass that comma to specify thay it is a single tuple.'''
    # post = cursor.fetchone()
    #print(post)
    post = db.query(models.Post).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found.")

    return post 


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *"""
    #                , (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist.")
        
    post.delete()    
    db.commit()   
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.Response)
def update_post(id: int , updated_post:schemas.PostCreate, db: Session = Depends(get_db)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content =  %s, published = %s WHERE id = %s RETURNING *"""
    #                , (post.title, post.content, post.published, (str(id))))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
    # really important lesson that i get here is if not index is true even index==0 and we should use NONE here.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist.")
    post_query.update(updated_post.model_dump())
    
    db.commit()
       
    return  post_query.first()