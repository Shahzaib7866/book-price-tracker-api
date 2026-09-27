# Book Price Tracker API

A backend service built with FastAPI, PostgreSQL and SQLAlchemy that scrapes book data
from [books.toscrape.com](https://books.toscrape.com) and exposes it through a RESTful API.
Fully containerized with Docker & Docker Compose, runs with a single command.

## Features

- **Web Scraping:** Scrapes book title, price, rating, availability and category for every
  book on the site, with duplicate prevention (via each book's unique URL) and basic error
  handling for missing fields or failed page loads.
- **Relational Database Storage:** PostgreSQL with SQLAlchemy ORM.
- **RESTful Endpoints:** Pagination, category filtering, price range filtering, and a scrape trigger.
- **Dockerized Environment:** App + database run together with a single command.
- **Data Validation:** Pydantic models validate every request and response.

## Tech Stack

- **Framework:** FastAPI (Python 3.11)
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy
- **Scraping:** BeautifulSoup & Requests
- **Containerization:** Docker & Docker Compose

## Setup & Run

1. Clone the repository:

```bash
   git clone https://github.com/Shahzaib7866/book-price-tracker-api.git
   cd book-price-tracker-api
```

2. Create a `.env` file in the root (copy from `.env.example` and fill in your own values)(this is only needed the first time):

```bash
   cp .env.example .env
```

3. Start the project(app + database) with a single command(Docker Desktop must be running):

```bash
   docker-compose up --build
```

4. The API will be available at: `http://localhost:8000`

   Interactive API docs (Swagger UI): `http://localhost:8000/docs`

## Running the Scraper

** via the API (recommended):**

```bash
curl -X POST http://localhost:8000/scrape
```

from Swagger UI: expand `POST /scrape` → **Try it out** → **Execute**.

Scrape all categories from books.toscrape.com and store new books in the database.
Running the scraper multiple times will not create duplicate entries — each book is checked
against its unique source URL before insertion.

## API Endpoints

| Method | Endpoint                           | Description                              |
| ------ | ---------------------------------- | ---------------------------------------- |
| GET    | `/books`                           | Get all books (paginated)                |
| GET    | `/books?page=2&page_size=20`       | Custom pagination                        |
| GET    | `/books/{id}`                      | Get a single book by ID                  |
| GET    | `/books?category=Mystery`          | Filter books by category                 |
| GET    | `/books?min_price=10&max_price=50` | Filter books by price range              |
| POST   | `/scrape`                          | Trigger scraping and update the database |

Filters can also be combined, e.g. `/books?category=Mystery&min_price=20&max_price=50`.

### Example Requests

```bash
# GET - first page of books
GET http://localhost:8000/books

# GET - a specific book
GET http://localhost:8000/books/1

# GET - filter by category
GET "http://localhost:8000/books?category=Travel"

# GET - filter by price range
GET "http://localhost:8000/books?min_price=20&max_price=50"

# POST - trigger scraper (use Swagger UI)
POST http://localhost:8000/scrape
```

## Notes

- Database schema is auto-created on app startup — no manual migration needed.
- Duplicate prevention is handled via a unique constraint on each book's source URL.
