from fastapi import FastAPI
import sounddevice as sd
import numpy as np
import wavio
import whisper

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Agente de fala rodando!"}

@app.get("/transcribe")
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
