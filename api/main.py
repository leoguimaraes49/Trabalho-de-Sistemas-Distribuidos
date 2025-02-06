from fastapi import FastAPI, Query, UploadFile, File
import requests
import os

app = FastAPI()

# Endereços dos serviços
SPEECH_TO_TEXT_URL = "http://speech_to_text:8001/transcribe"
MUSIC_GENERATOR_URL = "http://music_generator:8002/generate_music"

@app.get("/")
def read_root():
    return {"message": "API Principal rodando!"}

@app.post("/processar")
async def processar(file: UploadFile = File(None), texto: str = Query(None, description="Texto para geração de música")):
    try:
        if file:
            print("\n🎤 Enviando arquivo para transcrição...")
            files = {"audio": (file.filename, file.file, file.content_type)}
            response = requests.post(f"{SPEECH_TO_TEXT_URL}/file", files=files)
        elif texto:
            print("\n🔍 Texto recebido diretamente.")
            transcricao = texto
        else:
            print("\n🎤 Gravando e transcrevendo pelo microfone...")
            response = requests.get(f"{SPEECH_TO_TEXT_URL}/microphone")
        
        # Processa a resposta do agente de fala
        if file or not texto:
            if response.status_code == 200:
                transcricao = response.json().get("transcricao", "").strip()
            else:
                raise ValueError(f"Erro na transcrição: {response.json()}")

        if not transcricao:
            raise ValueError("Falha na transcrição: áudio vazio ou incompreensível")

        print(f"\n🔍 TEXTO TRANSCRITO: {transcricao}\n")

        # Enviando o texto transcrito para o agente de geração de música
        print("🎹 GERANDO MÚSICA...")
        response = requests.post(MUSIC_GENERATOR_URL, json={"prompt": transcricao})

        if response.status_code == 200:
            caminho_musica = response.json().get("musica", "Erro ao gerar música")
        else:
            raise ValueError(f"Erro na geração musical: {response.json()}")

        return {
            "status": "sucesso",
            "musica": caminho_musica,
            "texto": transcricao
        }
    
    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
