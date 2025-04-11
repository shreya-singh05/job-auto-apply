# Use Playwright base image with Python and all dependencies
FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

# Set working directory
WORKDIR /app

# Copy app files
COPY app.py /app

# Install Python dependencies
RUN pip install --no-cache-dir flask gunicorn && \
    playwright install --with-deps

# Expose the port your app runs on
EXPOSE 10000

# Use Gunicorn for production server
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
