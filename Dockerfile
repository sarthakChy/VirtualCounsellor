# Build stage
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    g++ \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-alpine AS production

# Install only runtime dependencies (if any)
RUN apk add --no-cache \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy only the necessary Python modules
COPY agentic_layer/ ./agentic_layer/
COPY config/ ./config/
COPY core/ ./core/
COPY models/ ./models/
COPY scrapers/ ./scrapers/
COPY server/ ./server/
COPY ui/ ./ui/
COPY utils/ ./utils/

# Copy any root-level Python files
COPY *.py ./

# Create non-root user
RUN adduser -D -s /bin/sh appuser \
    && chown -R appuser:appuser /app
USER appuser

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8080

CMD ["uvicorn", "server.run:app", "--host", "0.0.0.0", "--port", "8080"]