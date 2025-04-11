# Use official Python image with Playwright dependencies
FROM mcr.microsoft.com/playwright/python:v1.43.1

# Set working directory
WORKDIR /app

# Copy app code
COPY app.py /app
COPY requirements.txt /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port (Render uses env var PORT)
EXPOSE 8080

# Default command
CMD ["python", "app.py"]
