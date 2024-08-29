# Usa una imagen oficial de Python
FROM python:3.11

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo requirements.txt a la imagen
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del proyecto a la imagen
COPY . .

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]