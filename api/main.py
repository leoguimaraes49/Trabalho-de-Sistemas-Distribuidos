from fastapi import FastAPI, Query
import requests
import os
import uvicorn

# URLs dos agentes (definidas no Docker Compose)
SPEECH_TO_TEXT_URL = os.getenv("SPEECH_TO_TEXT_URL", "http://speech_to_text:8001")
MUSIC_GENERATOR_URL = os.getenv("MUSIC_GENERATOR_URL", "http://music_generator:8002")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API principal rodando!"}

@app.get("/processar")
def processar(texto: str = Query(None, description="Texto para geração de música")):
    try:
        # Se o texto não for enviado na requisição, chama o agente de fala
        if not texto:
            response = requests.get(f"{SPEECH_TO_TEXT_URL}/transcribe")
            data = response.json()
            texto = data.get("transcricao", "")
        
        if not texto:
            raise ValueError("Falha na transcrição: áudio vazio ou incompreensível")

        print(f"\n🔍 TEXTO RECEBIDO: {texto}\n")

        # Envia para o agente gerador de música
        print("=== ETAPA 2: GERAÇÃO MUSICAL ===")
        response = requests.post(f"{MUSIC_GENERATOR_URL}/generate_music", json={"prompt": texto})
        data = response.json()
        caminho_musica = data.get("musica", "")

        return {
            "status": "sucesso",
            "musica": caminho_musica,
            "texto": texto
        }
    
    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
