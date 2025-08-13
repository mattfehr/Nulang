FROM python:3.11-slim

# Faster/cleaner Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

# Non-root user for safety
RUN adduser --disabled-password --gecos "" appuser

# Workdir
WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY pages ./pages
COPY src ./src

# Port for Flask
EXPOSE 3000

# Drop privileges
USER appuser

# Start server (webserver.py reads $PORT)
CMD ["python", "src/webserver.py"]
