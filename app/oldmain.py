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
    rating: Optional[int] = None
      
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
           
#my_post list work as database for us here:
my_posts = [{"title":"title of post 1", "content":"content of post 1", "id": 11} ,
            {"title": "favorite food", "content":"I like pizza" , "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
    
@app.get("/")
def root():
    return {"message": "Welcome to my API"}
'''if we pass same paths to multiple crud operations and their http method was similar our result
will be the first match fastapi would find in this case if pass same path to get_post as root
the result will be root.
'''

#  url path: "/"
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/createposts")
def create_post(payload :  dict = Body(...)):
    print(payload)
    return {"new_post": f"title: {payload['title']} content: {payload['content']}"}
 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post : Post):   
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0 , 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
    # print(post.title , post.content)
    # print(post.dict()) post.dict() is deprecated!
# new:  print(post.model_dump())


@app.get("/posts/latest")
def get_latest():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

'''Here is a thing that we have been talked about before at this point path orders are crucial
as we can see we will have errors cuz fastapi will send first match and at this point we 
have /posts/{id} and fastapi can't recognize /latest is a specific path and it coincides
match with {id} so we have to move /latest path before our general one.'''   

@app.get("/posts/{id}")
def get_post(id: int , response:Response):
    post = find_post(id)
    #if not post   means ==>    if post==None
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id: {id} was not found."}
    return {"post_detail":post}    
    # Be sure to validate id to integer cuz its default is string.

@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting post
    #find the index in the array that has required ID
    index = find_index_post(id)
    # print(index)
    
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist.")
    
    my_posts.pop(index)
    #return {"message":"the post has been successfully deleted."} : it doesn't throw me 
    #any error but in course danjee was recieving error and he said we shouldn't return anything
    #wxcept response code back in 204 no content status code.
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int , post:Post):
    index = find_index_post(id)
    
    if index == None:
    # really important lesson that i get here is if not index is true even index==0 and we should use NONE here.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist.")
        
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict   
    return {"data": post_dict}
