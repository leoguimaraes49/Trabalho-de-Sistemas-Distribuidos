import importlib
import os
import sys
import unittest
from types import ModuleType
from unittest.mock import MagicMock, Mock, patch

import requests
from fastapi.testclient import TestClient

from api.main import app


def response(body, status_error=None):
    result = Mock()
    result.json.return_value = body
    if status_error:
        result.raise_for_status.side_effect = status_error
    return result


class CoordinatorTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("api.main.requests.post")
    @patch.dict(os.environ, {"MUSIC_GENERATOR_URL": "http://musica:9002/"})
    def test_texto_usa_url_configurada(self, post):
        post.return_value = response({"status": "sucesso", "musica": "/app/output/teste.wav"})
        result = self.client.post("/processar", params={"texto": "  jazz  "})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()["texto"], "jazz")
        post.assert_called_once_with("http://musica:9002/generate_music", timeout=(5, 600), json={"prompt": "jazz"})

    @patch("api.main.requests.post")
    @patch.dict(os.environ, {"SPEECH_TO_TEXT_URL": "http://fala:9001", "MUSIC_GENERATOR_URL": "http://musica:9002"})
    def test_audio_e_encaminhado_aos_dois_servicos(self, post):
        post.side_effect = [response({"status": "sucesso", "transcricao": "café"}), response({"status": "sucesso", "musica": "saida.wav"})]
        result = self.client.post("/processar", files={"file": ("audio.wav", b"audio", "audio/wav")})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {"status": "sucesso", "texto": "café", "musica": "saida.wav"})
        self.assertEqual(post.call_args_list[0].args[0], "http://fala:9001/transcribe/file")
        self.assertEqual(post.call_args_list[1].kwargs["json"], {"prompt": "café"})

    @patch("api.main.requests.post")
    def test_entrada_vazia_nao_chama_servicos(self, post):
        self.assertEqual(self.client.post("/processar", params={"texto": " "}).status_code, 400)
        post.assert_not_called()

    @patch("api.main.requests.post")
    def test_servico_com_erro_em_json_nao_retorna_sucesso(self, post):
        post.return_value = response({"status": "erro", "detalhes": "interno"})
        result = self.client.post("/processar", params={"texto": "teste"})
        self.assertEqual(result.status_code, 502)
        self.assertNotIn("interno", result.text)

    @patch("api.main.requests.post", side_effect=requests.Timeout())
    def test_timeout_retorna_erro_de_gateway(self, post):
        self.assertEqual(self.client.post("/processar", params={"texto": "teste"}).status_code, 502)

    @patch("api.main.requests.post")
    def test_resposta_sem_arquivo_e_rejeitada(self, post):
        post.return_value = response({"status": "sucesso"})
        self.assertEqual(self.client.post("/processar", params={"texto": "teste"}).status_code, 502)

    @patch("api.main.requests.post")
    def test_json_invalido_e_rejeitado(self, post):
        post.return_value.json.side_effect = ValueError("invalid json")
        self.assertEqual(self.client.post("/processar", params={"texto": "teste"}).status_code, 502)


class AudioServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Mantém os testes leves: os modelos reais não são baixados nem carregados.
        cls.modules = patch.dict(sys.modules, {
            "numpy": ModuleType("numpy"), "sounddevice": ModuleType("sounddevice"),
            "wavio": ModuleType("wavio"), "whisper": ModuleType("whisper"),
        })
        cls.modules.start()
        cls.speech = importlib.import_module("agents.speech_to_text.listen")
        cls.client = TestClient(cls.speech.app)

    @classmethod
    def tearDownClass(cls):
        cls.modules.stop()

    def test_upload_usa_arquivo_temporario_e_remove_apos_sucesso(self):
        caminhos = []
        def transcrever(caminho):
            caminhos.append(caminho)
            with open(caminho, "rb") as arquivo:
                self.assertEqual(arquivo.read(), b"audio")
            return "texto"
        with patch.object(self.speech, "_transcrever", side_effect=transcrever):
            result = self.client.post("/transcribe/file", files={"audio": ("../../arq.wav", b"audio", "audio/wav")})
        self.assertEqual(result.json(), {"status": "sucesso", "transcricao": "texto"})
        self.assertFalse(os.path.exists(caminhos[0]))

    def test_erro_remove_arquivo_e_retorna_http_500(self):
        caminhos = []
        def falhar(caminho):
            caminhos.append(caminho)
            raise RuntimeError("detalhe interno")
        with patch.object(self.speech, "_transcrever", side_effect=falhar):
            result = self.client.post("/transcribe/file", files={"audio": ("audio.wav", b"audio", "audio/wav")})
        self.assertEqual(result.status_code, 500)
        self.assertNotIn("detalhe interno", result.text)
        self.assertFalse(os.path.exists(caminhos[0]))


class MusicServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        audiocraft = ModuleType("audiocraft")
        audiocraft_models = ModuleType("audiocraft.models")
        audiocraft_models.MusicGen = MagicMock()
        torchaudio = ModuleType("torchaudio")
        torchaudio.save = Mock()
        cls.modules = patch.dict(sys.modules, {"audiocraft": audiocraft, "audiocraft.models": audiocraft_models, "torchaudio": torchaudio})
        cls.modules.start()
        cls.music = importlib.import_module("agents.music_generator.music")
        cls.client = TestClient(cls.music.app)

    @classmethod
    def tearDownClass(cls):
        cls.modules.stop()

    def test_entrada_vazia_rejeitada(self):
        self.assertEqual(self.client.post("/generate_music", json={"prompt": " "}).status_code, 400)

    def test_gera_nomes_distintos(self):
        with patch.object(self.music.os, "makedirs"), patch.object(self.music.torchaudio, "save"):
            primeiro = self.client.post("/generate_music", json={"prompt": "café"})
            segundo = self.client.post("/generate_music", json={"prompt": "café"})
        self.assertEqual(primeiro.status_code, 200)
        self.assertEqual(segundo.status_code, 200)
        self.assertNotEqual(primeiro.json()["musica"], segundo.json()["musica"])

    def test_falha_do_modelo_retorna_http_500(self):
        with patch.object(self.music.MusicGen, "get_pretrained", side_effect=RuntimeError("detalhe interno")):
            result = self.client.post("/generate_music", json={"prompt": "café"})
        self.assertEqual(result.status_code, 500)
        self.assertNotIn("detalhe interno", result.text)


if __name__ == "__main__":
    unittest.main()
