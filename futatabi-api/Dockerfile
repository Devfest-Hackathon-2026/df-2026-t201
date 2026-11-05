FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.10.7 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /srv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY app ./app
COPY data ./data
ENV PATH="/srv/.venv/bin:$PATH"

EXPOSE 8080
# Cloud Run injects PORT; default 8080 for local runs.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
