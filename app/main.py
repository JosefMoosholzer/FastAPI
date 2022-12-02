from . import models, schemas, utils, errors
from .database import engine, get_db
from .routers import post, user
from sqlalchemy.orm import Session

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

import psycopg2
from psycopg2.extras import RealDictCursor

from time import sleep

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# Run this in the terminal to start the server: uvicorn app.main:app --reload



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


# Including routes
app.include_router(post.router)
app.include_router(user.router)