FROM python:3.9-slim

WORKDIR /app

# Copia o requirements.txt e instala as dependências
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do agente
COPY agents/music_generator /app

# Expõe a porta 8002
EXPOSE 8002

# Comando para iniciar o agente
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]