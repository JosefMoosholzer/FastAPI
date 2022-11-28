from fastapi import FastAPI
from fastapi.params import Body
from datetime import datetime

app = FastAPI()

@app.get('/')
async def today():
    return {'Date': datetime.now().date()}

@app.get('/posts')
def get_posts():
    return {'data': 'This is your posts'}

@app.post('/posts')
def create_post(payLoad: dict = Body(...)):
    print(payLoad)
    return {'message': 'Successfully created post'}