import logging
import os
from uuid import uuid4

import torchaudio
from audiocraft.models import MusicGen
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
logger = logging.getLogger(__name__)


class MusicRequest(BaseModel):
    prompt: str


@app.get("/")
def read_root():
    return {"message": "Agente de música rodando!"}


@app.post("/generate_music")
def generate_music(request: MusicRequest):
    texto = request.prompt.strip()
    if not texto:
        raise HTTPException(status_code=400, detail="Informe um texto para gerar música")

    try:
        model = MusicGen.get_pretrained("facebook/musicgen-small")
        model.set_generation_params(duration=10)
        audio_tensor = model.generate([texto])

        output_dir = "/app/output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"musica_{uuid4().hex}.wav")
        torchaudio.save(output_path, audio_tensor[0].cpu(), 32000)
        return {"status": "sucesso", "musica": output_path}
    except Exception as exc:
        logger.exception("Falha ao gerar música")
        raise HTTPException(status_code=500, detail="Falha ao gerar música") from exc
