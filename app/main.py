from typing_extensions import deprecated
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List
from fastapi import Body, FastAPI , Response , status , HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import time
from sqlalchemy.orm import Session
from .  import models, schemas, utils
from .database import engine, get_db
from .routers import login, posts, users


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

      
      
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
           
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(login.router)
 
    
@app.get("/")
def root():
    return {"message": "Welcome to my API"}


