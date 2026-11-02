FROM python:3.11-slim AS builder
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runner
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH="/home/mitt_user/.local/bin:${PATH}"
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
RUN useradd -u 8501 -m mitt_user && chown -R mitt_user:mitt_user /app
USER mitt_user

COPY --from=builder --chown=mitt_user:mitt_user /root/.local /home/mitt_user/.local
COPY --chown=mitt_user:mitt_user .streamlit/config.toml /app/.streamlit/config.toml
COPY --chown=mitt_user:mitt_user app.py /app/app.py
COPY --chown=mitt_user:mitt_user src/ /app/src/
COPY --chown=mitt_user:mitt_user config/ /app/config/

EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
