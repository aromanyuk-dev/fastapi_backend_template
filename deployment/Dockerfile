# --- ЭТАП 1: Base (Общие переменные) ---
FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app:/app/src

WORKDIR /app



FROM base AS builder
ENV PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Устанавливаем ТОЛЬКО то, что нужно для компиляции
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock ./
# Устанавливаем зависимости в папку .venv внутри проекта
RUN poetry install --no-root --without dev


# --- ЭТАП 3: Development (Для локальной разработки) ---
FROM builder AS development
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "events.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# --- ЭТАП 4: Production (Финальный супер-легкий образ) ---
FROM base AS production

# Устанавливаем ТОЛЬКО runtime-библиотеки (например, для Postgres нужна libpq5, а не dev-версия)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Копируем из билдера ТОЛЬКО папку с установленными библиотеками (.venv)
COPY --from=builder /app/.venv /app/.venv

# Копируем код приложения
COPY . .

# Прокидываем путь к библиотекам из виртуального окружения
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Запуск через gunicorn
CMD ["gunicorn", "events.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000"]