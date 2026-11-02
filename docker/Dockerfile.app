# ==========================================
# Stage 1: Build dependencies and wheels
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Install system compilation packages needed for numerical libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy package requirement profiles
COPY requirements.txt .

# Compile Python dependencies into wheel packages
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# Stage 2: Final hardened runtime container
# ==========================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Prevent Python from writing .pyc files to disk and enable instant stream unbuffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/mitt_user/.local/bin:${PATH}"

# Install minimal operational runtime utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a secure, non-privileged system user for GxP runtime tracking
RUN useradd -u 8501 -m mitt_user && \
    mkdir -p /app/src /app/.streamlit && \
    chown -R mitt_user:mitt_user /app

USER mitt_user

# Copy installed Python packages from the builder stage
COPY --from=builder --chown=mitt_user:mitt_user /root/.local /home/mitt_user/.local
# Copy specific repository assets into workspace path scopes
COPY --chown=mitt_user:mitt_user .streamlit/config.toml /app/.streamlit/config.toml
COPY --chown=mitt_user:mitt_user app.py /app/app.py
COPY --chown=mitt_user:mitt_user src/ /app/src/

# Expose Streamlit's default networking endpoint port
EXPOSE 8501

# Add standard health status interrogation checks to monitor system liveness
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch the primary Streamlit Bio-Twin gateway application console
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
