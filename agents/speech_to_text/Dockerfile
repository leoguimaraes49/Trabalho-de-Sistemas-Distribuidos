FROM python:3.9-slim

# Instala dependências do sistema (Git e FFmpeg)
RUN apt-get update && apt-get install -y git ffmpeg

WORKDIR /app

# Copia o requirements.txt e instala dependências
COPY ../requirements.txt .
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código do agente
COPY agents/speech_to_text /app

EXPOSE 8001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]