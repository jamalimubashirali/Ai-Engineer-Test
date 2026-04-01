FROM python:3.11-slim

WORKDIR /app

# Copy dependency manifest first (layer-cache friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full application package
COPY main.py .
COPY models/ models/
COPY routers/ routers/
COPY services/ services/

# The shared config/ package lives one directory above in the repo.
# Copy it into the image so imports resolve correctly.
COPY ../config/ config/

EXPOSE 8000

# OPENROUTER_API_KEY must be injected at runtime:
#   docker run -e OPENROUTER_API_KEY=sk-or-... -p 8000:8000 brief-analyzer
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
