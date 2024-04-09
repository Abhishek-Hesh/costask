from typing import Union
from fastapi import FastAPI, Path
from pydantic import BaseModel
from pymongo import mongo_client

from fastapi.responses import HTMLResponse
from fastapi import requests
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


# mongodb connection
conn = MongoClient("mongodb+srv://48Q8aQRljAnhA0uX:48Q8aQRljAnhA0uX@cluster0.473rgbb.mongodb.net/")

# library management schema
class Book(BaseModel):
    book_no : int
    title: str
    author: str
    year: int
    pages: int

class User(BaseModel):
    user_no : int
    username: str

class Borrowings(BaseModel):
    user_id: int
    book_id: int
    
# Temporary storage for books and users
books_db = []
users_db = []
borrow_db = []

# mongodb collections
books = conn.book.books.find({})
users = conn.book.users.find({})
borrows = conn.book.borrowings.find({})

@app.get("/")
async def read_item():
    for doc in books:
        books_db.append(
            {'_id': doc['_id'], 'title': doc['title'], 'author': doc['author'], 'year': doc['year'], 'pages': doc['pages']}
        )
    print(books_db)
    return {'books': books_db}

# Routes for managing books
@app.post("/books/")
async def create_book(book: Book):
    books_db.append(book)
    return book

@app.get("/books/")
async def get_books():
    return books_db

# Routes for managing users
@app.post("/create_user/")
async def create_user(user: User):
    users_no = user.user_no
    username = user.username
    return {
        'user_no' : users_no,
        'username' : username
    }

@app.get("/users/")
async def get_users(request : Request):
    docs = conn.book.users.find({})
    for doc in docs:
        users_db.append(
            {'user_no': doc['user_no'], 'username': doc['username']}
        )
    print(users_db)
    return {'users' : users_db }

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id < len(users_db):
        return users_db[user_id-1]
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/create_borrowings/")
async def create_user(borr : Borrowings):
    users_id = borr.user_id
    book_id = borr.book_id
    return {
        'user_id' : user_id,
        'book_id' : book_id
    }

@app.get("/borrowings/")
async def get_users():
    for doc in borrows:
        borrow_db.append(
            {'_id': doc['_id'], 'title': doc['title'], 'author': doc['author'], 'year': doc['year'], 'pages': doc['pages']}
        )
    print(books_db)
    return {
        'borrows' : borrow_db
    }