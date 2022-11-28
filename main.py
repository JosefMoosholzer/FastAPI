from collections import defaultdict
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

from datetime import datetime

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = defaultdict(dict)
my_posts[1] = {'title': 'Title of first post', 'content': 'Content of first post', 'id': 1}
my_posts[2] = {'title': 'Favorite foods', 'content': 'I like pizza', 'id': 2}


@app.get('/')
async def today():
    return {'Date': datetime.now().date()}


# Create
@app.post('/posts')
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = len(my_posts) + 1
    my_posts[post_dict['id']] = post_dict
    return post_dict

## Read
@app.get('/posts')
def get_posts():
    return {'data': list(my_posts.values())}

@app.get('/posts/{id}')
def get_post(id: int):
    print('GET-request for ' + str(id))
    return {'posts': my_posts.get(id)}

## Update
@app.put('posts/{id}')
def update_post():
    return {'data': 'This is your posts'}

## Delete
@app.delete('/posts')
def delete_post():
    return {'data': 'This is your posts'}

