from turtle import title
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from fastapi import Body, FastAPI , Response , status , HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import time
from sqlalchemy.orm import Session
from .  import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str    
    published: bool = True
    #rating: Optional[int] = None
      
while True:
    try: 
        conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres',
                            password='samanJA1381', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Datebase connection was succesfull!")
        break
    except Exception as error:
        print('Connecting to database failed.')
        print("Error is:", error)
        time.sleep(4)
           
    
@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).order_by(models.Post.id).all()
    return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # #print(posts)
    posts = db.query(models.Post).all()
    return {"data": posts}

 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post : Post, db: Session = Depends(get_db)):   
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """
    #                , (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    '''we are using post.dict() and we unpack it with **kwargs method and it automatically fill our
    need columns and put it into right place and we do not have to fill it manually anymore every
    column'''
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest():
    cursor.execute("""SELECT * FROM posts ORDER BY created_at  DESC LIMIT 1;""")
    post = cursor.fetchone()
    return {"detail": post}




@app.get("/posts/{id}")
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

    return {"post_detail":post}    


@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
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


@app.put("/posts/{id}")
def update_post(id: int , updated_post:Post, db: Session = Depends(get_db)):
    
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
    
        
    return {"data": updated_post}
