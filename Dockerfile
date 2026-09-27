
# using Python 3.11 image
FROM python:3.11-slim

# Working directory
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FastAPI server run
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]