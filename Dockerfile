FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy
WORKDIR /app
COPY app.py /app
# Install dependencies including Gunicorn and Playwright
RUN pip install flask playwright gunicorn && \
    playwright install --with-deps
EXPOSE 10000
# Run using Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
