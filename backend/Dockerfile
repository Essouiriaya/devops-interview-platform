
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Installer PyTorch en version CPU uniquement
RUN pip install --no-cache-dir \
    torch==2.6.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Installer les dépendances du projet
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
