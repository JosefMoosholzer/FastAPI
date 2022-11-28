from collections import defaultdict
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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
@app.post('/posts', status_code=status.HTTP_201_CREATED)
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
def get_post(id: int, response: Response):
    post = my_posts.get(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')

    return {'posts': post}

## Update
@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    if not my_posts.get(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')
    else:
        post_dict = post.dict()
        post_dict['id'] = id
        my_posts[id] = post_dict
        return {'data': post_dict}

## Delete
@app.delete('/posts/{id}')
def delete_post(id: int):
    if not my_posts.get(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')
    else:
        my_posts.pop(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)