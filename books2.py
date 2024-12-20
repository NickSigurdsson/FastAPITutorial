from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

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
    published_date: int = Field(gt=1999, lt=2031)

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

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

# Path parameter checks the parameter of the path to make sure it conforms with the needed values
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')

# Query parameter checks the parameter of the query to see if what we're seacrching by is corect (same as path but this is more meant for filtering that is not done with variable within the path but the body instead)
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating:int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

# Note: books/{integer value} is an endpoint SHARED by both getting books by the id and by the publishing date, so you should try to either add to the endpoint or essentially look into putting the endpoint you'd like to test above the current existing endpoint
@app.get("/books/publish/{published_date}", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int = Path(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
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

@app.put("/book/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] == book 
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404,detail='Item not found')

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')