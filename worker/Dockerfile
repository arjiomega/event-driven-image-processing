FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN pip install --no-cache-dir uv \
    && uv sync --frozen

COPY app ./app

CMD ["uv", "run", "celery", "-A", "app.celery_app", "worker", "--loglevel=info", "--hostname=worker@%h"]
