import re
import time
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from src.models import Book

BASE_URL = "https://books.toscrape.com/"


def get_categories(session: requests.Session) -> list[dict]:
    resp = session.get(BASE_URL, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    category_links = soup.select("div.side_categories ul li ul li a")
    categories = []
    for link in category_links:
        categories.append({
            "name": link.text.strip(),
            "url": BASE_URL + link["href"],
        })
    return categories


def parse_book_card(article, category_name: str) -> dict | None:
    """Ek book card (<article>) se data nikalta hai."""
    try:
        title = article.h3.a["title"].strip()

        price_text = article.select_one("p.price_color").text
        price = float(re.sub(r"[^\d.]", "", price_text))

        rating_class = article.select_one("p.star-rating")["class"]
        rating = rating_class[1] if len(rating_class) > 1 else "Unknown"

        availability = article.select_one("p.instock.availability").text.strip()

        relative_link = article.h3.a["href"]
        book_url = requests.compat.urljoin(BASE_URL + "catalogue/", relative_link)

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "category": category_name,
            "availability": availability,
            "book_url": book_url,
        }
    except (AttributeError, TypeError, ValueError) as e:
        print(f"[WARN] Book skip hui, parsing error: {e}")
        return None


def scrape_category(session: requests.Session, category: dict) -> list[dict]:
    books = []
    url = category["url"]

    while url:
        try:
            resp = session.get(url, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[WARN] Page load nahi hui: {url} — {e}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.select("article.product_pod")

        for article in articles:
            book_data = parse_book_card(article, category["name"])
            if book_data:
                books.append(book_data)

        next_link = soup.select_one("li.next a")
        if next_link:
            url = requests.compat.urljoin(url, next_link["href"])
        else:
            url = None

        time.sleep(0.1)

    return books

def run_scraper(db: Session) -> dict:
    session = requests.Session()
    categories = get_categories(session)

    existing_urls = {row[0] for row in db.query(Book.book_url).all()}

    total_scraped = 0
    total_new = 0

    for category in categories:
        books = scrape_category(session, category)
        total_scraped += len(books)

        for book_data in books:
            if book_data["book_url"] in existing_urls:
                continue  

            new_book = Book(**book_data)
            db.add(new_book)
            existing_urls.add(book_data["book_url"])  
            total_new += 1

        db.commit()

    return {"total_scraped": total_scraped, "new_books_added": total_new}