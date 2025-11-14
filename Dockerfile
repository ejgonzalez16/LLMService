# Usamos una imagen base de Python 3.11 slim
FROM python:3.12.2-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    cmake \
    g++ \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libpq-dev \
    curl \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Creamos directorio de la app
WORKDIR /app

# Copiamos requirements
COPY requirements.txt .

# Instalamos dependencias de Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el proyecto
COPY .. .
COPY wait-for-mysql.sh /wait-for-mysql.sh
RUN chmod +x /wait-for-mysql.sh


# Exponemos el puerto de Django
EXPOSE 8001

# Comando por defecto para correr la app con gunicorn
ENTRYPOINT ["/wait-for-mysql.sh", "argy-db", "gunicorn", "LLMService.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "1"]