FROM python:3.12-slim

RUN apt-get update
RUN apt-get install -y build-essential
RUN rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend ./backend

EXPOSE 8000
WORKDIR /app
CMD ["sh", "-c", "python backend/manage.py runserver 0.0.0.0:8000"]
