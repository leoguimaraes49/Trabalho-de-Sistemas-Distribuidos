# Inteligência Artificial Distribuída aplicada à Cadeia Produtiva do Café

## Descrição Geral
Este projeto faz parte de um trabalho acadêmico focado no **desenvolvimento de uma solução de inteligência artificial distribuída aplicada à cadeia produtiva do café**. Ele envolve a criação de uma API REST que interage com dois agentes inteligentes distintos, responsáveis por:
- **Agente de Fala:** Capta áudio e o transcreve para texto.
- **Agente Gerador de Música:** Gera uma música baseada no texto recebido.

Todos os agentes estão contidos em containers Docker, garantindo modularidade e escalabilidade da solução.

---

## Estrutura do Projeto
```
projeto_cafe/
├── api/
│   ├── main.py  # API principal
│   ├── Dockerfile  # Configuração Docker da API
├── agents/
│   ├── speech_to_text/  # Agente de Fala
│   │   ├── listen.py  # Módulo de transcrição de áudio
│   │   ├── Dockerfile  # Configuração Docker do agente
│   ├── music_generator/  # Agente de Geração de Música
│   │   ├── music.py  # Módulo de geração de música
│   │   ├── Dockerfile  # Configuração Docker do agente
├── docker-compose.yml  # Orquestração dos containers
├── requirements.txt  # Dependências do projeto
└── README.md  # Documentação do projeto
```

---

## Requisitos
Antes de executar o projeto, certifique-se de que possui os seguintes softwares instalados:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.9+](https://www.python.org/downloads/)
- Microfone (para testes de captação de áudio)

---

## Instalação e Execução
### 1. Clonar o Repositório
```sh
git clone [https://github.com/seu-usuario/projeto_cafe.git](https://github.com/leoguimaraes49/Trabalho-de-Sistemas-Distribuidos.git
cd Trabalho-de-Sistemas-Distribuidos
```

### 2. Construir e Executar os Containers
Para inicializar todo o ambiente:
```sh
docker-compose up --build
```
Esse comando:
- **Constrói** as imagens Docker.
- **Inicializa** os containers da API e dos agentes.

Se quiser rodar os containers em background:
```sh
docker-compose up -d
```

### 3. Testar os Componentes
#### **Verificar se os agentes estão rodando**
Abra o navegador e acesse:
- **API principal:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Agente de Fala:** [http://localhost:8001](http://localhost:8001)
- **Agente de Música:** [http://localhost:8002](http://localhost:8002)

#### **Gerar música diretamente**
Envie um comando para o agente de música:
```sh
curl -X POST "http://localhost:8002/generate_music" -H "Content-Type: application/json" -d '{"prompt": "Uma melodia relaxante"}'
```

#### **Testar a API completa**
Envie um texto para a API principal gerar a música correspondente:
```sh
curl -X GET "http://localhost:8000/processar?texto=Uma%20melodia%20suave"
```

---

## Detalhes dos Containers
### **API (porta 8000)**
Responsável por:
- Coordenar os agentes
- Receber solicitações REST
- Encaminhar o texto recebido ao gerador de música

### **Agente de Fala (porta 8001)**
Capta áudio do microfone e o converte em texto.
Pode ser chamado diretamente via:
```sh
curl -X GET "http://localhost:8001"
```

### **Agente Gerador de Música (porta 8002)**
Recebe um texto e gera uma música baseada nele.
Pode ser testado via:
```sh
curl -X POST "http://localhost:8002/generate_music" -H "Content-Type: application/json" -d '{"prompt": "Jazz animado"}'
```
O arquivo gerado será salvo em `output/musica_gerada.wav`.

---

## Encerrando o Projeto
Para parar os containers sem removê-los:
```sh
docker-compose down
```
Se quiser excluir todos os containers e volumes:
```sh
docker-compose down -v
```

---

## Possíveis Erros e Soluções
### 1. **Erro: Porta já em uso**
Se alguma porta estiver ocupada, altere a exposição no `docker-compose.yml`.

### 2. **Erro de acesso ao microfone**
- No **Windows**, verifique as permissões em `Configurações > Privacidade > Microfone`.
- No **Linux**, rode com `--device /dev/snd` no `docker-compose.yml`.

### 3. **Erro: Espaço em disco do Docker esgotado**
Execute:
```sh
docker system prune -a -f
```
Isso remove imagens, containers e volumes não utilizados.

---

## Contribuição
1. **Fork** o repositório.
2. Crie uma **branch**: `git checkout -b minha-feature`
3. Commit: `git commit -m 'Minha contribuição'`
4. Push: `git push origin minha-feature`
5. Envie um **Pull Request**!

---

## Licença
Este projeto é de uso acadêmico e segue os termos definidos pela instituição.

---

Desenvolvido para a disciplina de **Sistemas Distribuídos**. 🚀



