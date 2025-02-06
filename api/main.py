from fastapi import FastAPI, Query, UploadFile, File
import requests

app = FastAPI()

# Endereços dos serviços
SPEECH_TO_TEXT_URL = "http://speech_to_text:8001"
MUSIC_GENERATOR_URL = "http://music_generator:8002/generate_music"

@app.get("/")
def read_root():
    return {"message": "API Principal rodando!"}

@app.post("/processar")
async def processar_texto(texto: str = Query(..., description="Texto para geração de música")):
    try:
        print(f"\n🔍 Texto recebido: {texto}")

        response = requests.post(MUSIC_GENERATOR_URL, json={"prompt": texto})

        if response.status_code == 200:
            caminho_musica = response.json().get("musica", "Erro ao gerar música")
        else:
            raise ValueError(f"Erro na geração musical: {response.json()}")

        return {"status": "sucesso", "musica": caminho_musica, "texto": texto}

    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

@app.post("/processar/file")
async def processar_arquivo(audio: UploadFile = File(...)):
    try:
        print("\n🎤 Enviando arquivo para transcrição...")
        files = {"audio": (audio.filename, audio.file, audio.content_type)}
        response = requests.post(f"{SPEECH_TO_TEXT_URL}/transcribe/file", files=files)

        if response.status_code == 200:
            transcricao = response.json().get("transcricao", "").strip()
        else:
            raise ValueError(f"Erro na transcrição: {response.json()}")

        if not transcricao:
            raise ValueError("Falha na transcrição: áudio vazio ou incompreensível")

        print(f"\n🔍 TEXTO TRANSCRITO: {transcricao}\n")

        response = requests.post(MUSIC_GENERATOR_URL, json={"prompt": transcricao})

        if response.status_code == 200:
            caminho_musica = response.json().get("musica", "Erro ao gerar música")
        else:
            raise ValueError(f"Erro na geração musical: {response.json()}")

        return {"status": "sucesso", "musica": caminho_musica, "texto": transcricao}

    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


