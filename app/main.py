from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor

from time import sleep

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# Run this in the terminal to start the server: uvicorn app.main:app --reload


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Connecting to the postgres database
while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='FastAPI',
                                user='postgres',
                                password='password123',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as e:
        print("Connection to database failed")
        print("Error: ", e)
        print("Trying again in 10 seconds")
        sleep(10)


### CRUD-functions ###
# Create
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'data': new_post}



## Read
@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    return {'data': db.query(models.Post).all()}


@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')
        
    return {"data": post}



## Update
@app.put('/posts/{id}')
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id)
    if post_to_update.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')
    else:
        post_to_update.update(post.dict(), synchronize_session=False)
        db.commit()
        return {"data": post_to_update.first()}



## Delete
@app.delete('/posts/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)