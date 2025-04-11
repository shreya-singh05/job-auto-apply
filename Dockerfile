# Use official Playwright Python image from Docker Hub
FROM playwrightcommunity/playwright-python:1.43.1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port for Render
EXPOSE 10000

# Run the Flask app
CMD ["python", "app.py"]
