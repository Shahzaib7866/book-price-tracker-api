# Book Price Tracker API

A backend service built with FastAPI, PostgreSQL, and SQLAlchemy that scrapes book data
from [books.toscrape.com](https://books.toscrape.com) and exposes it through a RESTful API.
Fully containerized with Docker & Docker Compose — runs with a single command.

## Features

- **Web Scraping:** Scrapes book title, price, rating, availability, and category for every
  book on the site, with duplicate prevention (via each book's unique URL) and basic error
  handling for missing fields or failed page loads.
- **Relational Database Storage:** PostgreSQL with SQLAlchemy ORM.
- **RESTful Endpoints:** Pagination, category filtering, price range filtering, and an
  on-demand scrape trigger.
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
   git clone <your-repo-url>
   cd book_tracker
```

2. Create a `.env` file in the root (copy from `.env.example` and fill in your own values):

```bash
   cp .env.example .env
```

3. Start the project (app + database) with a single command:

```bash
   docker-compose up --build
```

4. The API will be available at: `http://localhost:8000`
   Interactive API docs (Swagger UI): `http://localhost:8000/docs`

## Running the Scraper

**Option 1 — via the API (recommended):**

```bash
curl -X POST http://localhost:8000/scrape
```

Or from Swagger UI: expand `POST /scrape` → **Try it out** → **Execute**.

**Option 2 — standalone script (independent of the API):**

```bash
docker exec -it fastapi_app python run_scraper_standalone.py
```

Both scrape all categories from books.toscrape.com and store new books in the database.
Running the scraper multiple times will not create duplicate entries — each book is checked
against its unique source URL before insertion.

## API Endpoints

| Method | Endpoint                           | Description                              |
| ------ | ---------------------------------- | ---------------------------------------- |
| GET    | `/books`                           | Get all books (paginated)                |
| GET    | `/books?page=2&page_size=20`       | Custom pagination                        |
| GET    | `/books/{id}`                      | Get a single book by ID                  |
| GET    | `/books?category=Travel`           | Filter books by category                 |
| GET    | `/books?min_price=10&max_price=50` | Filter books by price range              |
| POST   | `/scrape`                          | Trigger scraping and update the database |

Filters can also be combined, e.g. `/books?category=Travel&min_price=20&max_price=50`.

### Example Requests

```bash
# Get first page of books
curl http://localhost:8000/books

# Get a specific book
curl http://localhost:8000/books/1

# Filter by category
curl "http://localhost:8000/books?category=Travel"

# Filter by price range
curl "http://localhost:8000/books?min_price=20&max_price=50"

# Trigger scraper
curl -X POST http://localhost:8000/scrape
```

## Notes

- Database schema is auto-created on app startup — no manual migration needed.
- Duplicate prevention is handled via a unique constraint on each book's source URL.
- `rating` is stored as text (e.g. `"Three"`) as scraped from the site, not converted to a number.
