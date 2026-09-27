
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional

from src.database import get_db, engine, Base
from src.models import Book
from src.schemas import BookResponse, PaginatedBooksResponse, ScrapeResponse
from src.scraper import run_scraper

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Price Tracker API",
    description="Scrapes books.toscrape.com and serves the data via REST API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "Book Price Tracker API is running"}

@app.get("/books", response_model=PaginatedBooksResponse)
def get_books(
    page: int = Query(1, ge=1, description="Page number, starts at 1"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    db: Session = Depends(get_db),
):
    query = db.query(Book)

    # Filters — sirf tab lagenge jab client ne unhe bheja ho
    filters = []
    if category:
        filters.append(Book.category.ilike(category))  # ilike = case-insensitive match
    if min_price is not None:
        filters.append(Book.price >= min_price)
    if max_price is not None:
        filters.append(Book.price <= max_price)

    if filters:
        query = query.filter(and_(*filters))

    total = query.count()  # pagination se pehle total count (filtered)

    offset = (page - 1) * page_size
    books = query.offset(offset).limit(page_size).all()

    return PaginatedBooksResponse(
        total=total,
        page=page,
        page_size=page_size,
        books=books,
    )


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return book


@app.post("/scrape", response_model=ScrapeResponse)
def trigger_scrape(db: Session = Depends(get_db)):
    try:
        result = run_scraper(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

    return ScrapeResponse(
        message="Scraping completed successfully",
        total_scraped=result["total_scraped"],
        new_books_added=result["new_books_added"],
    )

