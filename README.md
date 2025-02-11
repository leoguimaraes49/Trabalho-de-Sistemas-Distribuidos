# Inteligência Artificial Distribuída aplicada à Cadeia Produtiva do Café

## 📌 Descrição Geral
Este projeto faz parte de um trabalho acadêmico focado no **desenvolvimento de uma solução de inteligência artificial distribuída aplicada à cadeia produtiva do café**. Ele envolve a criação de uma **API REST** que interage com dois agentes inteligentes distintos:

- **🎤 Agente de Fala:** Capta áudio do microfone ou recebe um arquivo de áudio e transcreve para texto usando **Whisper**.
- **🎵 Agente Gerador de Música:** Utiliza o modelo **Audiocraft (MusicGen)** para gerar uma música baseada no texto transcrito.

Todos os agentes estão contidos em containers **Docker**, garantindo modularidade e escalabilidade da solução.

---

## 📚 Estrutura do Projeto
```
projeto_cafe/
├── api/
│   ├── main.py  # API principal
│   ├── Dockerfile  # Configuração Docker da API
├── agents/
│   ├── speech_to_text/  # Agente de Fala
│   │   ├── listen.py  # Módulo de transcrição de áudio (microfone e upload)
│   │   ├── Dockerfile  # Configuração Docker do agente
│   ├── music_generator/  # Agente de Geração de Música
│   │   ├── music.py  # Módulo de geração de música usando Audiocraft
│   │   ├── Dockerfile  # Configuração Docker do agente
├── docker-compose.yml  # Orquestração dos containers
├── requirements.txt  # Dependências do projeto
└── README.md  # Documentação do projeto
```

---

### 📌 **Requisitos**
Para executar o projeto, você precisará do **Docker** e do **Docker Compose**. A instalação varia de acordo com o sistema operacional:

- **Windows**: Recomendado instalar o **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**, que já inclui o **Docker Compose**.
- **Linux**: Instale o **Docker** e o **Docker Compose** manualmente com os seguintes comandos:

  ```sh
  sudo apt update && sudo apt install docker.io docker-compose -y

- [Python 3.9+](https://www.python.org/downloads/)
- Microfone (para testes de captação de áudio)
  
---

## 🚀 Instalação e Execução

### 1️⃣ Clonar o Repositório
```sh
git clone https://github.com/leoguimaraes49/Trabalho-de-Sistemas-Distribuidos.git
cd Trabalho-de-Sistemas-Distribuidos
```

### 2️⃣ Construir e Executar os Containers
Para **construir e rodar** todos os serviços:
```sh
docker-compose up --build
```
Se quiser rodar os containers em **background**:
```sh
docker-compose up 
```

---

## 🔎 Testando a API

### 📌 **1. Verificar se os agentes estão rodando**
Abra o navegador e acesse:
- **API principal:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Agente de Fala:** [http://localhost:8001](http://localhost:8001)
- **Agente de Música:** [http://localhost:8002](http://localhost:8002)

---

### 🎤 **2. Testar o Agente de Fala (Whisper)**
O agente de fala pode ser testado de três maneiras diferentes:

#### 🛠️ **Gravar áudio e transcrever (via microfone)**
```sh
curl -X GET "http://localhost:8001/transcribe/microphone"
```
Esse comando grava 5 segundos de áudio e transcreve o texto.

#### 🛠️ **Enviar um arquivo de áudio para transcrição**
```sh
curl -X POST "http://localhost:8001/transcribe/file" -F "audio=@audio.wav"
```
> **Nota:** O arquivo `audio.wav` deve estar no mesmo diretório onde você executa o comando.

#### 🛠️ **Entrada direta de texto (simulação de transcrição)**
```sh
curl -X GET "http://localhost:8001/transcribe?texto=Teste de transcrição"
```
Esse comando não grava áudio, mas simula o envio de um texto diretamente.

---

### 🎵 **3. Testar o Agente de Música (Audiocraft)**
#### 🛠️ **Gerar música a partir de um texto**
```sh
curl -X POST "http://localhost:8002/generate_music" -H "Content-Type: application/json" -d '{"prompt": "Que café gostoso"}'
```
O arquivo gerado será salvo em:
```
output/musica_gerada.wav
```

---

### 🎧 **4. Testar o Fluxo Completo da API**
Agora podemos testar o sistema inteiro, **desde a fala até a geração da música**:

1- Enviando um texto diretamente para gerar música
```sh
curl -X POST "http://localhost:8000/processar?texto=Uma%20melodia%20suave"
```
2- Se quiser testar enviando um **arquivo de áudio**:
```sh
curl -X POST "http://localhost:8000/processar" -F "file=@audio.wav"
```
3- Gravação de áudio via microfone e geração de música:
```sh
curl -X POST "http://localhost:8000/processar"

```

---

## 🛠️ Encerrando o Projeto
Para **parar os containers sem removê-los**:
```sh
docker-compose down
```
Se quiser excluir **todos os containers e volumes**:
```sh
docker-compose down -v
```

---

## 🚨 Possíveis Erros e Soluções

### ❌ **1. Erro: Porta já em uso**
Se alguma porta estiver ocupada, altere as portas no `docker-compose.yml`.

### ❌ **2. Erro de acesso ao microfone**
- No **Windows**, verifique se o Docker tem permissão para acessar o microfone em:
  **Configurações > Privacidade > Microfone**.

### ❌ **3. Erro: Falha na Transcrição**
Se o Whisper não conseguir transcrever:
- Teste com um áudio de melhor qualidade.
- Certifique-se de que o modelo Whisper foi baixado corretamente.

---

## 💪 Contribuição
1. **Fork** o repositório.
2. Crie uma **branch**: `git checkout -b minha-feature`
3. Envie um **Pull Request**! 🚀

---

## 📜 Licença
Este projeto foi desenvolvido para fins acadêmicos.





