from audiocraft.models import MusicGen
import torchaudio
import warnings
from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()
warnings.filterwarnings("ignore")

# Modelo para a entrada da API
class MusicRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "Agente de música rodando!"}

@app.post("/generate_music")
def generate_music(request: MusicRequest):
    try:
        texto = request.prompt
        print(f"\n🎹 GERANDO MÚSICA PARA: '{texto}'")

        # Carrega o modelo e gera música
        model = MusicGen.get_pretrained("facebook/musicgen-small")
        model.set_generation_params(duration=10)
        audio_tensor = model.generate([texto])

        # Define o caminho para salvar o arquivo
        output_dir = "/app/output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = f"{output_dir}/musica_gerada.wav"

        torchaudio.save(output_path, audio_tensor[0].cpu(), 32000)
        print("✅ Música gerada com sucesso!")

        return {"status": "sucesso", "musica": output_path}

    except Exception as e:
        print(f"❌ Erro na geração: {str(e)}")
        return {"status": "erro", "detalhes": str(e)}
