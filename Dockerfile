FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/botuser/.local

# Copy application code
COPY --chown=botuser:botuser . .

# Ensure local bin is in PATH
ENV PATH=/home/botuser/.local/bin:$PATH

# Switch to non-root user
USER botuser

# Run the bot
CMD ["python", "main.py"]

