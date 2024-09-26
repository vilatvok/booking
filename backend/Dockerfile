FROM python:3.10

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
ENV PATH="/root/.local/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY poetry.lock pyproject.toml /backend/
RUN poetry install --no-root

COPY . .

ENTRYPOINT ["poetry", "run"]
CMD ["fastapi", "dev", "src/main.py", \
    "--host", "0.0.0.0", "--port", "8000"]
