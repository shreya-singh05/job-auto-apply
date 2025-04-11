FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

WORKDIR /app

COPY app.py /app

RUN pip install flask

EXPOSE 10000

CMD ["python", "app.py"]
