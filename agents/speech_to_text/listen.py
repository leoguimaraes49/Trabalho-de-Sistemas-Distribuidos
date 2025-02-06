from fastapi import FastAPI, File, UploadFile, Query
import sounddevice as sd
import numpy as np
import wavio
import whisper
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Agente de fala rodando!"}

@app.get("/transcribe/microphone")
def gravar_e_transcrever_audio(duration: int = 5):
    try:
        print(f"\n🎤 Gravando por {duration} segundos...")

        # Captura áudio
        samplerate = 44100
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype=np.int16)
        sd.wait()

        # Salva o áudio em um arquivo WAV
        audio_path = "audio.wav"
        wavio.write(audio_path, audio_data, samplerate, sampwidth=2)

        # Usa Whisper para transcrever
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)

        transcricao = result["text"].strip()
        print(f"\n🔍 TRANSCRIÇÃO: {transcricao}")

        return {"status": "sucesso", "transcricao": transcricao}

    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

@app.post("/transcribe/file")
async def transcrever_arquivo(audio: UploadFile = File(...)):
    try:
        # Salva o arquivo recebido
        audio_path = f"temp_{audio.filename}"
        with open(audio_path, "wb") as buffer:
            buffer.write(await audio.read())

        # Usa Whisper para transcrever
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)

        transcricao = result["text"].strip()
        print(f"\n🔍 TRANSCRIÇÃO (arquivo): {transcricao}")

        # Remove o arquivo temporário após a transcrição
        os.remove(audio_path)

        return {"status": "sucesso", "transcricao": transcricao}

    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}
