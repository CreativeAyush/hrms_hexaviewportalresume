# Backend Dockerfile
FROM python:3.11-slim

# Install system dependencies for document processing and LibreOffice for DOCX to PDF conversion
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-writer \
    libreoffice-java-common \
    default-jre-headless \
    libfontconfig1 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    fonts-liberation \
    fonts-dejavu \
    fonts-freefont-ttf \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV HOME=/tmp

# Copy only the necessary parts from the root context
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ .

# The application expects templates and utils at specific relative paths
# We will copy them so they are accessible via "../templates" and "../utils"
# from the backend/ directory inside the container.
COPY templates/ /templates/
COPY utils/ /utils/

EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
