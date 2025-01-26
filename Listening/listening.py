import whisper
import sounddevice as sd
import numpy as np
import wavio

def gravar_e_transcrever_audio(duration=5, output_filename="audio.wav", rate=44100, channels=1):
    # Gravação de áudio
    print("Gravando...")
    audio_data = sd.rec(int(duration * rate), samplerate=rate, channels=channels, dtype='float32')
    sd.wait()  # Aguarda o término da gravação

    # Converte os dados de float para int16 (16-bit PCM)
    audio_data_int16 = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)

    # Salvando o áudio em um arquivo WAV
    wavio.write(output_filename, audio_data_int16, rate)
    print(f"Áudio gravado em {output_filename}")

    # Carrega o modelo Whisper
    model = whisper.load_model("turbo")

    # Transcrição do áudio
    result = model.transcribe(output_filename)

    # Retorna o texto da transcrição
    return result["text"]

# Exemplo de uso da função
texto_transcrito = gravar_e_transcrever_audio(duration=5)
print(f"Texto transcrito: {texto_transcrito}")