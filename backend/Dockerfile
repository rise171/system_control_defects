# Используем официальный Python образ
FROM python:3.11-slim-bookworm

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы с зависимостями
COPY backend/requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код бэкенда
COPY backend/ .

# Копируем собранный фронтенд в статику бэкенда
COPY frontend/dist/ backend/app/static/

# Создаем непривилегированного пользователя
RUN useradd -m -u 1000 user && \
    chown -R user:user /app

USER user

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]