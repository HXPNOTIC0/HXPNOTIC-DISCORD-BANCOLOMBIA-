# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto (no requerido por bots de Discord, pero útil si añades webhooks o dashboards)
EXPOSE 8000

# Establece la variable de entorno para dotenv si lo deseas
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar el bot
CMD ["python", "main.py"]
