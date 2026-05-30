# 📚 Books REST API

A fully async REST API built with **FastAPI** and **SQLModel**, demonstrating clean architectural separation across a database layer, service layer, and route layer. Uses PostgreSQL as the database with async session management.

---

## 🏗️ Architecture

```
src/
├── books/
│   ├── model.py        # SQLModel table definition (maps to DB table)
│   ├── schemas.py      # Pydantic schemas (request/response validation)
│   ├── service.py      # Business logic & database operations
│   └── routes.py       # FastAPI route handlers (HTTP layer)
├── db/
│   └── main.py         # Engine, connection pool, session factory
└── config.py           # Environment settings (DATABASE_URL etc.)
```

### Layer Responsibilities

| Layer | File | Responsibility |
|---|---|---|
| Route | `routes.py` | Receives HTTP requests, returns HTTP responses |
| Service | `service.py` | Business logic, database queries |
| Database | `db/main.py` | Engine, connection pool, session lifecycle |

---

## 🛠️ Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — async web framework
- **[SQLModel](https://sqlmodel.tiangolo.com/)** — ORM combining SQLAlchemy + Pydantic
- **[PostgreSQL](https://www.postgresql.org/)** — relational database
- **[SQLAlchemy AsyncEngine](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)** — async database engine
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI server

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL running locally or via Docker

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/books-api.git
cd books-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/booksdb
```

### Run the API

```bash
uvicorn src.main:app --reload
```

API will be available at `http://localhost:8000`

Interactive docs at `http://localhost:8000/docs`

---

## 📡 API Endpoints

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| `GET` | `/books/` | Fetch all books | 200 |
| `POST` | `/books/` | Create a new book | 201 |
| `GET` | `/books/{book_uid}` | Fetch a single book by UID | 200 |
| `PATCH` | `/books/{book_uid}` | Partially update a book | 200 |
| `DELETE` | `/books/{book_uid}` | Delete a book | 204 |

---

## 📦 Request & Response Examples

### Create a Book — `POST /books/`

**Request body:**
```json
{
  "title": "Dune",
  "author": "Frank Herbert",
  "published_year": 1965
}
```

**Response `201`:**
```json
{
  "uid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "title": "Dune",
  "author": "Frank Herbert",
  "published_year": 1965,
  "created_at": "2026-05-27T10:30:00"
}
```

### Update a Book — `PATCH /books/{book_uid}`

Only send the fields you want to update (partial update supported):

```json
{
  "title": "Dune Messiah"
}
```

### Delete a Book — `DELETE /books/{book_uid}`

Returns `204 No Content` on success, `404 Not Found` if the book doesn't exist.

---

## 🔑 Key Concepts

### One Session Per Request

Every HTTP request gets its own isolated `AsyncSession` via FastAPI's dependency injection:

```python
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session   # session open for duration of request
                        # automatically closed after response is sent
```

This ensures clean state, no data leakage between requests, and automatic connection pool management.

### Async Throughout

All database operations use `await` to keep the event loop non-blocking:

```python
result = await session.exec(statement)   # non-blocking DB query
await session.commit()                   # non-blocking commit
await session.refresh(new_book)          # re-sync object with DB
```

### PATCH vs PUT

The `update_book` endpoint uses `PATCH` semantics — only the fields explicitly sent by the client are updated, existing fields are preserved:

```python
update_data.model_dump(exclude_unset=True)
# {"title": "New Title"} — only what was sent, nothing else overwritten
```

---

## 🗂️ Database Session Lifecycle

```
Request arrives
    ↓
get_session() called by FastAPI
    ↓
Session created, connection borrowed from pool
    ↓
yield session → injected into route handler
    ↓
Route handler runs, queries execute
    ↓
Response sent to client
    ↓
get_session() resumes past yield
    ↓
Session closed, connection returned to pool
```

---

## 📁 Project Structure Detail

```
src/
├── books/
│   ├── __init__.py
│   ├── model.py          # class BookModel(SQLModel, table=True)
│   ├── schemas.py        # BookModel, BookCreateModel, PatchBookModel
│   ├── service.py        # BookService class — all DB operations
│   └── routes.py         # APIRouter with CRUD endpoints
├── db/
│   ├── __init__.py
│   └── main.py           # async_engine, init_db(), get_session()
├── config.py             # Settings class reading from .env
└── main.py               # FastAPI app entry point, router registration
```

---

## ⚙️ Requirements

```
fastapi
uvicorn[standard]
sqlmodel
asyncpg
sqlalchemy
python-dotenv
```

Generate `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
