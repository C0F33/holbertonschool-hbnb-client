# Usa una imagen base de Alpine Linux con Python 3.9
FROM python:3.9-alpine

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt en el directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación en el directorio de trabajo
COPY . .

# Establece una variable de entorno para el puerto
ENV PORT 8000

# Define un volumen para el almacenamiento persistente
VOLUME /app/data

# Expone el puerto configurado
EXPOSE $PORT

# Define el comando para ejecutar Gunicorn
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]
