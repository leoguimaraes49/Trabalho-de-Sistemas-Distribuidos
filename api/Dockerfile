FROM python:3.9-slim

# Instala dependências do sistema (FFmpeg para Whisper)
RUN apt-get update && apt-get install -y ffmpeg\
git\

WORKDIR /app

# Copia o requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da API
COPY api /app/api

# Expõe a porta 8000
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]