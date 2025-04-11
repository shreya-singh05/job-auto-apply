FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

WORKDIR /app

COPY app.py /app

RUN pip install flask gunicorn && \
    playwright install --with-deps

EXPOSE 10000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10000", "app:app"]
