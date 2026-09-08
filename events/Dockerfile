
FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN pip install --no-cache-dir uv \
    && uv sync --frozen

COPY core ./core
COPY consumer.py .

CMD ["uv", "run", "python", "consumer.py"]
