FROM python:3.9-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    gcc \
    g++ \
    make \
    python3-dev \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt /app/requirements.txt

# Instala as dependências do Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia todo o código necessário para o contêiner
COPY api /app/api

# Define variáveis de ambiente para comunicação REST entre os agentes
ENV SPEECH_TO_TEXT_URL="http://speech_to_text:8001"
ENV MUSIC_GENERATOR_URL="http://music_generator:8002"

# Define o caminho para o Python encontrar os módulos corretamente
ENV PYTHONPATH=/app

# Expõe a porta 8000
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

