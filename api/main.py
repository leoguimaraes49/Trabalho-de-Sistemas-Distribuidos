
from fastapi import FastAPI
import uvicorn
from agents.speech_to_text.listen import gravar_e_transcrever_audio
from agents.music_generator.music import gerar_musica
import os
import sys 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["XFORMERS_DISABLE"] = "1"  

app = FastAPI()

@app.get("/processar")
def processar():
    try:
        # 1. Gravação e transcrição
        print("\n=== ETAPA 1: GRAVAÇÃO ===")
        texto = gravar_e_transcrever_audio(duration=7)
        
        if not texto:
            raise ValueError("Falha na transcrição: áudio vazio ou incompreensível")
        
        # Exibe o texto transcrito no terminal da API
        print(f"\n🔍 TEXTO TRANSCRITO: {texto}\n")
        
        # 2. Geração de música
        print("=== ETAPA 2: GERAÇÃO MUSICAL ===")
        caminho_musica = gerar_musica(texto)
        
        return {
            "status": "sucesso",
            "musica": caminho_musica,
            "texto": texto  # Texto incluído na resposta JSON
        }
    
    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)