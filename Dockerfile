# Use Python slim image as base
FROM python:3.10-slim

# Install build dependencies and clean up in one layer
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir . \
    && apt-get purge -y gcc python3-dev \
    && apt-get autoremove -y

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8108

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8108
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the application
CMD ["uvicorn", "rovercard.core:app", "--host", "0.0.0.0", "--port", "8108"]
