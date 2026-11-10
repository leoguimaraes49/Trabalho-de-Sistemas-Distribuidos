import logging
import os

import requests
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

app = FastAPI()
logger = logging.getLogger(__name__)


def _url_servico(variavel: str, padrao: str, rota: str) -> str:
    return f"{os.getenv(variavel, padrao).rstrip('/')}/{rota.lstrip('/')}"


def _chamar_servico(url: str, **kwargs) -> dict:
    try:
        response = requests.post(url, timeout=(5, 600), **kwargs)
        response.raise_for_status()
        resultado = response.json()
    except (requests.RequestException, ValueError) as exc:
        logger.warning("Falha na comunicação com serviço: %s", type(exc).__name__)
        raise HTTPException(status_code=502, detail="Falha na comunicação com um serviço de áudio") from exc

    if not isinstance(resultado, dict) or resultado.get("status") != "sucesso":
        raise HTTPException(status_code=502, detail="O serviço de áudio não concluiu a operação")
    return resultado


@app.get("/")
def read_root():
    return {"message": "API Principal rodando!"}


@app.post("/processar")
async def processar(texto: str = None, file: UploadFile = None):
    transcricao = (texto or "").strip()

    if file:
        url = _url_servico("SPEECH_TO_TEXT_URL", "http://speech_to_text:8001", "/transcribe/file")
        resultado = await run_in_threadpool(
            _chamar_servico,
            url,
            files={"audio": (file.filename, file.file, file.content_type)},
        )
        transcricao = resultado.get("transcricao")
        if not isinstance(transcricao, str) or not transcricao.strip():
            raise HTTPException(status_code=502, detail="O serviço não retornou uma transcrição válida")
        transcricao = transcricao.strip()

    if not transcricao:
        raise HTTPException(status_code=400, detail="Informe um texto ou envie um áudio")

    url = _url_servico("MUSIC_GENERATOR_URL", "http://music_generator:8002", "/generate_music")
    resultado = await run_in_threadpool(_chamar_servico, url, json={"prompt": transcricao})
    caminho = resultado.get("musica")
    if not isinstance(caminho, str) or not caminho.strip():
        raise HTTPException(status_code=502, detail="O serviço não retornou um arquivo de música")

    return {"status": "sucesso", "musica": caminho, "texto": transcricao}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
