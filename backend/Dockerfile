
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --retries 10 --timeout 1000 \
    torch==2.6.0 \
    --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir --retries 10 --timeout 1000 \
    -r requirements.txt

# Create a non-root user
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --create-home appuser

# Copy only required application files
COPY --chown=appuser:appgroup app/ ./app/
COPY --chown=appuser:appgroup tests/ ./tests/

# Set permissions
RUN chown appuser:appgroup /app

# Run as non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
