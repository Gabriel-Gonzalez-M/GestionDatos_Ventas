# 1. Imagen base de Python
FROM python:3.9-slim

# 2. Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar archivos del proyecto al contenedor
COPY . .

# 4. Instalar dependencias
RUN pip install pandas

# 5. Comando para ejecutar el pipeline
CMD ["python", "src/pipeline.py"]