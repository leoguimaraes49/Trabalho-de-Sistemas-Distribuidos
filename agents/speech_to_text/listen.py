import whisper
import sounddevice as sd
import numpy as np
import wavio
import os
from fastapi import FastAPI

app = FastAPI()

# Exemplo de endpoint para teste
@app.get("/")
def read_root():
    return {"message": "Speech-to-Text API is running!"}

def gravar_e_transcrever_audio(duration=5, rate=44100):
    """Grava áudio e transcreve usando sua solução bem-sucedida"""
    try:
        # 1. Gravação do áudio
        print("\n🎤 Gravando... (Fale agora!)")
        audio = sd.rec(int(duration * rate), 
                      samplerate=rate, 
                      channels=1,
                      dtype='float32')
        sd.wait()

        # 2. Conversão e salvamento temporário
        temp_file = "temp_audio.wav"
        audio_int16 = np.int16(audio / np.max(np.abs(audio)) * 32767)
        wavio.write(temp_file, audio_int16, rate)
        print(f"🔊 Áudio temporário salvo em: {temp_file}")

        # 3. Transcrição com Whisper
        model = whisper.load_model("base")
        result = model.transcribe(temp_file, language='pt')
        texto = result["text"].strip()
        
        # 4. Limpeza do arquivo temporário
        os.remove(temp_file)
        print("✅ Transcrição concluída com sucesso!")
        return texto

    except Exception as e:
        print(f"❌ Erro grave: {str(e)}")
        return ""

# Teste local direto
if __name__ == "__main__":
    texto = gravar_e_transcrever_audio()
    print(f"\n📝 Texto transcrito: {texto}")