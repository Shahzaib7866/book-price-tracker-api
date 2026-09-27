from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BookResponse(BaseModel):
    """Ek single book ka API response shape — GET /books/{id} aur list ke andar use hoga."""
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
    """GET /books ka response — sirf books ki list nahi, pagination info bhi."""
    total: int              
    page: int
    page_size: int
    books: list[BookResponse]


class ScrapeResponse(BaseModel):
    """POST /scrape ka response — scraping ka summary."""
    message: str
    total_scraped: int
    new_books_added: int

