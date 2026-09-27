from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BookResponse(BaseModel):
    id: int
    title: str
    price: float
    rating: str
    category: str
    availability: str
    book_url: str
    scraped_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedBooksResponse(BaseModel):
    total: int              
    page: int
    page_size: int
    books: list[BookResponse]

class ScrapeResponse(BaseModel):
    message: str
    total_scraped: int
    new_books_added: int

