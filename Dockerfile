FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

WORKDIR /app

# Copy the application file
COPY app.py /app

# Install required Python packages and browser dependencies
RUN pip install --no-cache-dir flask gunicorn playwright && \
    playwright install --with-deps

# Expose the port that the app will run on
EXPOSE 10000

# Run the app using Gunicorn in production mode
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
