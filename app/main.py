from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor

from datetime import datetime
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


@app.get('/')
async def today():
    return {'Date': datetime.now().date()}

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {"status": "success"}

# Create
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(query="""INSERT INTO posts (title, content, published)
                            VALUES (%s, %s, %s)
                            RETURNING *""",
                    vars=(post.title, post.content, post.published))
    conn.commit()
    return {'data': cursor.fetchone()}

## Read
@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 10""")
    posts = cursor.fetchall()
    return {'data': posts}

@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    cursor.execute(query="""SELECT * FROM posts WHERE id = %s""",
                    vars=(str(id),))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')

    return {'posts': post}

## Update
@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute(query="""UPDATE posts
                            SET title = %s, content= %s, published = %s
                            WHERE id = %s
                            RETURNING *""",
                    vars=(post.title, post.content, str(post.published), str(id)))
    conn.commit()
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')
    else:
        return {'data': updated_post}

## Delete
@app.delete('/posts/{id}')
def delete_post(id: int):
    cursor.execute(query="""DELETE FROM posts WHERE id = %s
                            RETURNING *""",
                    vars=(str(id),))
    conn.commit()
    if cursor.fetchone() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)