FROM python:3.12-slim

# Evita que Python genere archivos .pyc y asegura que la salida por consola no se retrase
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV WORKDIR=/workspace

WORKDIR ${WORKDIR}

# Actualizar el sistema e instalar utilidades básicas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# El código se montará en vivo vía volúmenes en el docker-compose