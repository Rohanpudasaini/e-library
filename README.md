# Elibrary

## Introduction
A very simple e-library backend built with FastAPI and SQLAlchemy.

### Points of Interest
1. Simple and modular architecture  
2. JWT-based authentication and authorization  
3. Developer-friendly tools like `pydantic-settings` for environment validation and Alembic for migrations  

## Usage
This app is currently in development. You can test it by following these steps:

### 1. Clone the repository
```bash
git clone https://github.com/Rohanpudasaini/e-library && cd e-library
````

### 2. Set up the environment file

```bash
cp .env.sample .env
```

Update `.env` with your actual configuration (e.g., database URL).

### 3. Install dependencies

Using **uv** for package management:

```bash
uv venv && uv sync
```

```bash
uv run alembic upgrade heads
```

### 4. Run the app

```bash
uv run uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` to explore the API documentation.

### 5. Enjoy 


