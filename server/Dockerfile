FROM python:3.11-slim

WORKDIR /app

# Rendszer függőségek telepítése
RUN apt-get update && apt-get install -y \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Poetry telepítése
RUN curl -sSL https://install.python-poetry.org | python3 -

# Path-hoz adás
ENV PATH="/root/.local/bin:$PATH"

# Poetry konfiguráció: ne hozzon létre virtuális környezetet
RUN poetry config virtualenvs.create false

# Függőségek másolása és telepítése
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-interaction --no-ansi --no-root

# Alkalmazás másolása
COPY . .

# Alkalmazás indítása
CMD ["poetry", "run", "uvicorn", "wealth.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 