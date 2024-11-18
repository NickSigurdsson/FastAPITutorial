from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    # The constructor is a method that is called when an object is created from a class and it allows the class to initialize the attributes of the class.
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

# We are making a pydantic model as seen by the importing of "Base Model"
class BookRequest(BaseModel):
    id: Optional[int] = Field(description='id is not required on creates', default = None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int

    # the code below will basically make a user defined example for any book requests that are made - can be seen on SwaggerUI (when the pydantic model of book request is made)
    model_config = {
        'json_schema_extra': {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2021),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2021),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2023),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2024),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2024),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2028)
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{published_date}")
async def read_book_by_date(published_date:int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_id}")
async def read_book(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book

@app.get("/books/")
async def read_book_by_rating(book_rating:int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.post("/create-book")
# BookRequest is a Pydantic model that will be used to validate the request body to fulfill the requirements of the API. We're saying here the our book_request is OF the same type as the pydantic model
async def create_book(book_request:BookRequest):
    # **  takes the keys of a dictionary and uses them as parameter names, and their corresponding values as parameter values when passing them to a function or class
    # model_dump basically converts the object into a dictionary
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

# This function basically makes it so that a unique Id is generated EVERY time (in relation to the last item's ID)
def find_book_id(book:Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1] + 1
    else:
        book.id = 1   
    return book   

@app.put("/book/update_book")
async def update_book(book:BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] == book 


@app.delete("/books/{book_id}")
async def delete_book(book_id:int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break


