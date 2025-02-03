FROM python:3.9-slim

# Instala dependências do sistema (FFmpeg para Whisper)
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

# Copia o requirements.txt e instala as dependências
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do agente
COPY agents/speech_to_text /app

# Expõe a porta 8001
EXPOSE 8001

# Comando para iniciar o agente
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]