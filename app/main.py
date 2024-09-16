
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str 
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host ='127.0.0.1', database= 'fastapi', port = '5432', 
                                user='postgres', password='qazplm1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database conenction succesfull!")
        break
    except Exception as error:
        print("Connection to Database Error")
        print("Error: ", error)
        time.sleep(2)


my_posts = [{"title": "title post1", "content": "post content 1", "id": 1}, {"title": "favorite food", "content": "I love pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return{"message":"Hello World!"}

@app.get("/posts")
def get_posts():
    # posts = cursor.execute('SELECT * FROM posts') 
    # posts = cursor.execute('CREATE TABLE fastapitable(id SERIAL PRIMARY KEY NOT NULL, table_name VARCHAR NOT NULL)')
    
    posts = cursor.execute('SELECT * FROM posts')
    # posts = cursor.fetchall()
    print(posts)
    return{"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return{"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"post with id {id} not exist")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'message': f"post with {id} was not found"}
    return{"post detals": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delet_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Id {id} not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id {id} update")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message": post_dict}
