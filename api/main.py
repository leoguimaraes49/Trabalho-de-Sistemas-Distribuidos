from fastapi import FastAPI, Query, UploadFile, File, HTTPException
import requests

app = FastAPI()

# Endereços dos serviços
SPEECH_TO_TEXT_URL = "http://speech_to_text:8001/transcribe"
MUSIC_GENERATOR_URL = "http://music_generator:8002/generate_music"

@app.get("/")
def read_root():
    return {"message": "API Principal rodando!"}

@app.post("/processar")
async def processar_texto(texto: str = Query(None, description="Texto para geração de música"), audio: UploadFile = File(None)):
    try:
        transcricao = texto

        # Caso um arquivo de áudio seja enviado, faz a transcrição
        if audio:
            print("\n🎤 Enviando arquivo para transcrição...")
            files = {"audio": (audio.filename, audio.file, audio.content_type)}
            response = requests.post(f"{SPEECH_TO_TEXT_URL}/file", files=files)

            if response.status_code == 200:
                transcricao = response.json().get("transcricao", "").strip()
            else:
                raise HTTPException(status_code=500, detail=f"Erro na transcrição: {response.json()}")

        if not transcricao:
            raise HTTPException(status_code=400, detail="Falha na transcrição: áudio vazio ou incompreensível")

        print(f"\n🔍 TEXTO PROCESSADO: {transcricao}")

        # Envia o texto transcrito ou o texto inserido para a geração de música
        response = requests.post(MUSIC_GENERATOR_URL, json={"prompt": transcricao})

        if response.status_code == 200:
            caminho_musica = response.json().get("musica", "Erro ao gerar música")
        else:
            raise HTTPException(status_code=500, detail=f"Erro na geração musical: {response.json()}")

        return {"status": "sucesso", "musica": caminho_musica, "texto": transcricao}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

