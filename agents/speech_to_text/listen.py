import logging
import os
from tempfile import NamedTemporaryFile

import numpy as np
import sounddevice as sd
import wavio
import whisper
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.concurrency import run_in_threadpool

app = FastAPI()
logger = logging.getLogger(__name__)


def _transcrever(audio_path: str) -> str:
    model = whisper.load_model("base")
    return model.transcribe(audio_path)["text"].strip()


@app.get("/")
def read_root():
    return {"message": "Agente de fala rodando!"}


@app.get("/transcribe/microphone")
def gravar_e_transcrever_audio(duration: int = Query(5, ge=1, le=60)):
    caminho = None
    try:
        samplerate = 44100
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype=np.int16)
        sd.wait()
        with NamedTemporaryFile(suffix=".wav", delete=False) as arquivo:
            caminho = arquivo.name
        wavio.write(caminho, audio_data, samplerate, sampwidth=2)
        return {"status": "sucesso", "transcricao": _transcrever(caminho)}
    except Exception as exc:
        logger.exception("Falha ao transcrever áudio do microfone")
        raise HTTPException(status_code=500, detail="Falha ao transcrever áudio do microfone") from exc
    finally:
        if caminho and os.path.exists(caminho):
            os.remove(caminho)


@app.post("/transcribe/file")
async def transcrever_arquivo(audio: UploadFile = File(...)):
    caminho = None
    try:
        # Um nome gerado pelo sistema evita colisões e não depende do nome enviado pelo cliente.
        with NamedTemporaryFile(suffix=".audio", delete=False) as arquivo:
            caminho = arquivo.name
            while bloco := await audio.read(1024 * 1024):
                arquivo.write(bloco)
        transcricao = await run_in_threadpool(_transcrever, caminho)
        return {"status": "sucesso", "transcricao": transcricao}
    except Exception as exc:
        logger.exception("Falha ao transcrever arquivo de áudio")
        raise HTTPException(status_code=500, detail="Falha ao transcrever arquivo de áudio") from exc
    finally:
        await audio.close()
        if caminho and os.path.exists(caminho):
            os.remove(caminho)
