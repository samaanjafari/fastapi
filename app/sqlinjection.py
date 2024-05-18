import psycopg
from psycopg.rows import dict_row
from typing import Optional
from fastapi import Body, FastAPI , Response , status , HTTPException
from pydantic import BaseModel
from random import randrange
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str    
    published: bool = True
    #rating: Optional[int] = None
      
while True:
    try: 
        conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres',
                            password='samanJA1381', row_factory=dict_row)
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

#  url path: "/"
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM users""")
    posts = cursor.fetchall()
    #print(posts)
    return {"data": posts}

 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post : Post):   
    cursor.execute("""INSERT INTO users (title, content, published) VALUES (%s, %s, %s) RETURNING * """
                   , (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest():
    cursor.execute("""SELECT * FROM users ORDER BY created_at  DESC LIMIT 1;""")
    post = cursor.fetchone()
    return {"detail": post}

#asghar
# Updated vulnerable endpoint with SQL injection
@app.get("/posts/{id}")
def get_post_with_injection(id: str, response: Response):
    # Simulate unsafe SQL query construction (vulnerable to SQL injection)
    query = f"SELECT * FROM users WHERE id = {id}"
    cursor.execute(query)
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found."
        )

    return {"post_detail": post} 


@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM users WHERE id = %s RETURNING *"""
                   , (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist.")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int , post:Post):
    
    cursor.execute("""UPDATE users SET title = %s, content =  %s, published = %s WHERE id = %s RETURNING *"""
                   , (post.title, post.content, post.published, (str(id))))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
    # really important lesson that i get here is if not index is true even index==0 and we should use NONE here.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist.")
        
    return {"data": updated_post}

