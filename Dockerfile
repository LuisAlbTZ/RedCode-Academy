# ============================================================
# Dockerfile — RedCode Academy
# ============================================================
FROM python:3.11-slim

# Metadatos
LABEL maintainer="RedCode Academy"
LABEL description="Plataforma educativa para programadores enfocada en resolucion de problemas"
LABEL version="1.0"

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Variables de entorno de Flask (usadas por config.py)
ENV FLASK_ENV=production
ENV PORT=5000
ENV DATABASE_URL="postgresql://postgres:postgres@db:5432/redcode_academy"

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar para producción
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . .

# Crear un usuario no-root para seguridad 
RUN adduser --disabled-password --gecos '' appuser && \ 
    chown -R appuser:appuser /app 
USER appuser

# Exponer el puerto de la aplicación
EXPOSE $PORT

# Comando de inicio
CMD ["python", "app.py"]
