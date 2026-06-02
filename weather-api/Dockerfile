FROM python:3.11-slim

WORKDIR /app

# Copiar solo los archivos de la app y dependencias
COPY requirements.txt .
COPY app.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usa la app
EXPOSE 5000

# Comando por defecto
CMD ["python", "app.py"]