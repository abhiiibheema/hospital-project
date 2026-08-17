FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build deps for building wheels from pyproject if needed
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project metadata first to leverage Docker layer cache
# Copy project metadata and requirements first to leverage Docker layer cache
COPY pyproject.toml README.md requirements.txt /app/
COPY src/ /app/src/

# Upgrade pip and install runtime requirements, then install the package
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir .

EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["python", "-m", "uvicorn", "myproject.main:app", "--host", "0.0.0.0", "--port", "8000"]
