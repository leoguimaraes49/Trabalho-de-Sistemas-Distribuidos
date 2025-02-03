FROM python:3.9-slim

# Instala dependências do sistema (Git e ferramentas de build)
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    make \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os requisitos para instalação das dependências
COPY ../requirements.txt /app/requirements.txt

# Instala as dependências do Python
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copia o código do serviço para dentro do contêiner
COPY agents/music_generator /app/music_generator

# Expõe a porta 8002 para comunicação
EXPOSE 8002

# Define o comando de inicialização do FastAPI/Uvicorn
CMD ["sh", "-c", "PYTHONPATH=/app uvicorn music_generator.music:app --host 0.0.0.0 --port 8002"]
