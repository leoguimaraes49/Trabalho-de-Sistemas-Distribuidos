from audiocraft.models import MusicGen
import torchaudio
import warnings

warnings.filterwarnings("ignore")

def gerar_musica(texto):
    try:
        print(f"\n🎹 GERANDO MÚSICA PARA: '{texto}'")
        
        # Carrega o modelo e gera música
        model = MusicGen.get_pretrained("facebook/musicgen-small")
        model.set_generation_params(duration=10)
        audio_tensor = model.generate([texto])  # Usa o texto original diretamente
        
        # Salva sem metadados (versão compatível)
        torchaudio.save("musica_gerada.wav", audio_tensor[0].cpu(), 32000)
        
        print("✅ Música gerada com sucesso!")
        return "musica_gerada.wav"
    
    except Exception as e:
        print(f"❌ Erro na geração: {str(e)}")
        return ""