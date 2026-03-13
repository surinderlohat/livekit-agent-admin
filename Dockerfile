# ---- Base image ----
FROM python:3.11-slim

# ---- Environment settings ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

# ---- Install system dependencies (needed for healthcheck curl) ----
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Create non-root user ----
RUN useradd -m appuser

# ---- Set working directory ----
WORKDIR /app

# ---- Copy dependency files first (IMPORTANT for caching) ----
COPY requirements.txt pyproject.toml* ./

# ---- Install Python dependencies ----
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# ---- Copy application code ----
COPY . .

# ---- Set permissions ----
RUN chown -R appuser:appuser /app

# ---- Switch to non-root user ----
USER appuser

# ---- Default exposed port ----
EXPOSE 8000

# ---- Container health check ----
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# ---- Start FastAPI ----
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]