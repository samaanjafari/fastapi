from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .  import models
from .database import engine
from .routers import login, posts, users, vote
from .config import settings



# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
        
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(vote.router)
    
@app.get("/")
def root():
    return {"message": "Welcome to my API"}


