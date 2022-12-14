FROM python:3.9

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.2.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --with local

COPY src/ ./

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8080", "main:app"]
