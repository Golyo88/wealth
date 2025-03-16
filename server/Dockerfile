FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
  curl \
  && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-interaction --no-ansi --no-root

COPY . .

CMD ["poetry", "run", "uvicorn", "wealth.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 