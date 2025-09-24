FROM python:3.12-slim

RUN apt-get update
RUN apt-get install -y curl build-essential
RUN apt-get install -y unzip
RUN curl -fsSL https://bun.com/install | bash
RUN rm -rf /var/lib/apt/lists/*

RUN mv /root/.bun/bin/bun /usr/local/bin/bun

WORKDIR /app
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend ./backend
COPY frontend ./frontend
WORKDIR /app/frontend
RUN bun install
RUN bun run build
EXPOSE 8000 3000
WORKDIR /app
CMD ["sh", "-c", "python backend/manage.py runserver 0.0.0.0:8000 & bun x serve -s frontend/dist -l 3000"]
