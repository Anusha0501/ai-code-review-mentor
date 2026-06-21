FROM python:3.11-slim AS backend
WORKDIR /app
COPY backend/pyproject.toml ./pyproject.toml
RUN pip install --no-cache-dir fastapi uvicorn pydantic pydantic-settings httpx
COPY backend/app ./backend/app
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
