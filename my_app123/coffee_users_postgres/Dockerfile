FROM python:3.10-slim

# Установка необходимых зависимостей

RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование вашего скрипта в контейнер
COPY . .

# Определение команды для выполнения скрипта
CMD ["python", "app.py"]


