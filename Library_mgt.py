from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

app = FastAPI()

class BookCreate(BaseModel):
    title:str = None #  optional
    author:str = None   # optional
    language:str = 'English'
    year:int = None # optional
    pages:int = None # optional

class Book(BookCreate):
    id:str

class BookUpdate(BookCreate):
    pass

class Books(BaseModel):
    books:list[Book]

class Response(BaseModel):
    message: Optional[str] = None
    has_error: Optional[bool] = False
    error_message: Optional[str] = None
    data: Optional[Book | Books] = None

books:dict[str, Book] = {}

@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return Response(message = "Hello, Welcome to my Library Management API")

@app.get("/books", status_code=status.HTTP_200_OK)
def menu():
    if books == {}:
        return Response(message = "Database is empty")
    return books

@app.get("/books/{id}", status_code=status.HTTP_200_OK)
def get_books_by_id(id:UUID):
    book = books.get(str(id))
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            details = "Book not found"
        )
    return book

@app.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book_in: BookCreate):
    book = Book(
        id = str(UUID(int=len(books)+1)),
        **book_in.dict(),
    )
    books[book.id] = book
    return Response(message = "Book added Succefully",
        data = book)
    
@app.put("/books/{id}", status_code=status.HTTP_201_OK)
def edit_book(id:UUID, book_in: BookUpdate):
    book = books.get(str(id))
    if not book:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            details = "Book not found"
        )
    book.title = book_in.title
    book.author = book_in.author
    book.language = book_in.language
    book.year = book_in.year
    book.pages = book_in.pages
    return Response(message ="Book updated successfully", data = book)

@app.delete("/books/{id}")
def delete_book(id:UUID):
    book = books.get(str(id))
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail = "Book not found"
        )
    del books[book.id]
    
    return Response(message = "Book deleted Succefully",  data  = book)