# IA distribuída para transcrição de áudio e geração de música

Protótipo acadêmico de sistemas distribuídos, desenvolvido no contexto da cadeia produtiva do café. O repositório reúne três serviços Python: uma API que coordena o fluxo, um serviço de transcrição de áudio com Whisper e outro de geração musical com MusicGen. Os serviços se comunicam por HTTP e são definidos no Docker Compose.

> Estado do projeto: protótipo acadêmico. Os comandos abaixo descrevem a configuração e as rotas presentes no código; a execução completa e a compatibilidade das dependências precisam ser validadas no ambiente de destino.

## Como funciona

```text
Texto ───────────────────────────────────────┐
                                              v
Áudio ──> serviço de transcrição (Whisper) ──> API ──> serviço de música (MusicGen) ──> arquivo WAV
             HTTP :8001                     :8000              HTTP :8002
```

A API recebe texto ou arquivo de áudio. Quando recebe arquivo, solicita a transcrição ao serviço de fala e envia o texto ao serviço musical. O serviço musical usa `facebook/musicgen-small`, solicita 10 segundos de áudio e grava `musica_gerada.wav`. No Compose, o diretório `/app/output` desse serviço está mapeado para `./output` no computador anfitrião.

O serviço de fala também contém uma rota própria para captação pelo microfone; a rota principal `/processar` aceita texto ou arquivo e não aciona essa captação diretamente.

## Tecnologias e estrutura

- Python 3.9, FastAPI e Uvicorn para os serviços HTTP.
- Whisper para transcrição; AudioCraft/MusicGen, PyTorch e torchaudio para geração musical.
- Docker e Docker Compose para definir os serviços e a rede.

```text
api/                       API coordenadora e Dockerfile
agents/speech_to_text/     Serviço de transcrição e Dockerfile
agents/music_generator/    Serviço de geração musical e Dockerfile
docker-compose.yml         Serviços, portas, rede e volume
requirements.txt           Dependências Python
Relatórios/                Documentos acadêmicos do projeto
```

## Execução com Docker

Pré-requisitos: Docker com Compose, acesso à rede para instalar dependências e obter modelos, espaço em disco e recursos de processamento adequados. As portas `8000`, `8001` e `8002` devem estar disponíveis.

Na raiz do repositório:

```bash
git clone https://github.com/leoguimaraes49/Trabalho-de-Sistemas-Distribuidos.git
cd Trabalho-de-Sistemas-Distribuidos
docker compose up --build
```

Os serviços expõem suas interfaces OpenAPI em:

| Serviço | Interface |
| --- | --- |
| API coordenadora | http://localhost:8000/docs |
| Transcrição | http://localhost:8001/docs |
| Geração musical | http://localhost:8002/docs |

Para encerrar os serviços, execute `docker compose down` em outro terminal. O diretório local `output` contém a saída mapeada; novas gerações usam o mesmo nome de arquivo e podem sobrescrever a anterior.

## Exemplos de requisição

Os exemplos usam `curl`. O primeiro envia texto à API coordenadora:

```bash
curl -X POST 'http://localhost:8000/processar?texto=Uma%20melodia%20suave'
```

Para enviar um arquivo de áudio à API, substitua `audio.wav` por um arquivo local:

```bash
curl -X POST 'http://localhost:8000/processar' -F 'file=@audio.wav'
```

Para chamar os serviços diretamente:

```bash
curl -X POST 'http://localhost:8001/transcribe/file' -F 'audio=@audio.wav'
curl -X POST 'http://localhost:8002/generate_music' -H 'Content-Type: application/json' -d '{"prompt":"Uma melodia suave"}'
```

A rota `GET /transcribe/microphone` pertence ao serviço de transcrição e depende de acesso a um dispositivo de áudio no ambiente onde ele roda. Esse acesso não está configurado explicitamente no Compose; a disponibilidade varia conforme o ambiente.

## Limitações e pontos para evolução

- A construção e a execução ponta a ponta não foram verificadas nesta revisão. As dependências incluem uma instalação do AudioCraft diretamente de um repositório Git; versões, recursos e downloads de modelos podem afetar a reprodução.
- Os modelos são carregados dentro das requisições, o que pode aumentar a latência e o consumo de recursos.
- A API principal utiliza endereços de serviços definidos no código; alterar apenas as variáveis de ambiente declaradas no Compose não muda esses endereços.
- O projeto não demonstra autenticação nem isolamento para uso público. O fluxo grava arquivos e registra texto processado em logs; use dados de teste e avalie privacidade e segurança antes de expô-lo.

## Documentação acadêmica

Os relatórios disponíveis estão no diretório [Relatórios](Relat%C3%B3rios/). O repositório foi desenvolvido para fins acadêmicos.
