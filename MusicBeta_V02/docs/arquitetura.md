# Documento de Arquitetura do Sistema (DAS)

## Projeto: CARDC (Ciclo Artístico-Reflexivo de Dupla Checagem)

### 1. Visão Geral do Sistema

#### O **CARDC** é um aplicativo web projetado para servir como um diário de bordo digital na prática instrumental deliberada. O sistema fornece uma infraestrutura tecnológica capaz de transpor os protocolos objetivos e subjetivos da metodologia **CARDC** para um ambiente seguro, permitindo o registro de sessões de estudo, autoavaliação etnográfica e armazenamento de evidências multimídia (vídeo e áudio).

### 2. Padrão Arquitetural

#### O sistema adota o padrão **MVC (Model-View-Controller)** adaptado para o ecossistema Flask, com uma separação clara de responsabilidades em camadas independentes para desacoplamento de código e facilidade de manutenção e testes.

```
[ Camada de Visão / Cliente ] (HTML/CSS/JS + Recorder.js)
                       │  ▲
    Requisições HTTP   │  │  Renderização Dinâmica (Jinja2)
                       ▼  │
       [ Camada de Roteamento ] (Blueprints / routes.py)
                       │  ▲
       Chamada Direta  │  │  Retorno de Dados / Status
                       ▼  │
       [ Camada de Controle ] (controllers/) ───► [ Helpers / Serviços ] (Cloudinary/Mail)
                       │  ▲
       Manipulação ORM │  │  Objetos de Dados
                       ▼  │
       [ Camada de Modelo ] (models/) ◄────────► [ Banco de Dados ] (PostgreSQL/SQLite)
```

### 3. Mapeamento Estrutural de Diretórios e Componentes

#### Abaixo está a descrição funcional de cada componente presente na estrutura do projeto:

```
MusicBeta_V02/Main/
├── app.py                      # Inicializador (Bootstrapper) central do aplicativo. Configura extensões e registra rotas.
├── Procfile                    # Arquivo de especificação de processos para o servidor de produção (Gunicorn).
├── requirements.txt            # Manifesto de dependências e bibliotecas do projeto.
├── init_db_script.py           # Script utilitário para criação e inicialização das tabelas do banco de dados via ORM.
│
├── models/                     # CAMADA DE MODELO: Definição de dados e persistência (ORM)
│   ├── database_config.py      # Instanciação centralizada do SQLAlchemy para evitar importações circulares.
│   ├── bcrypt_config.py        # Instanciação centralizada do componente de criptografia.
│   ├── usuario.py              # Modelo de Entidade "User" com regras de autenticação (Flask-Login).
│   ├── ciclo_de_estudo.py      # Modelo de Entidade "Ciclo" contendo os campos da ficha de registro.
│   └── gravacao.py             # Modelo de Entidade "Gravacao" mapeando os metadados dos arquivos enviados à nuvem.
│
├── controllers/                # CAMADA DE CONTROLE: Implementação das regras de negócio
│   ├── auth_controller.py      # Lógica de controle de acesso (registro, login, logout e geração de tokens de senha).
│   ├── ciclo_controller.py     # Controlador responsável pelas operações de CRUD dos ciclos de estudo.
│   └── gravacao_controller.py  # Controlador encarregado de vincular mídias enviadas aos seus respectivos ciclos.
│
├── routes/                     # CAMADA DE ROTEAMENTO: Exposição de endpoints HTTP
│   └── routes.py               # Definição de Blueprints, interceptação de requisições e proteção de rotas (@login_required).
│
├── helpers/                    # CAMADA DE SERVIÇOS / UTILS: Integrações externas
│   ├── media_upload_helper.py  # Abstração de infraestrutura para comunicação direta com a API do Cloudinary (SDK).
│   └── mail_config.py          # Configuração e inicialização do serviço SMTP (Flask-Mail) para notificações.
│
├── views/                      # CAMADA DE VISÃO: Relação com o usuário
│   └── html/                   # Templates estruturados em Jinja2 para renderização dinâmica no lado do servidor.
│
└── static/                     # RECURSOS ESTÁTICOS
    ├── css/style.css           # Folha de estilo centralizada da interface visual.
    └── js/recorder.js          # Script cliente que manipula a API nativa MediaRecorder para captura de áudio/vídeo.
```

### 4. Fluxo de Dados Principal (Caso de Uso: Salvar Ciclo com Gravação)

1. Captura e Envio (Visão): O usuário encerra a prática instrumental; o arquivo `recorder.js` finaliza a captura da webcam, gera um blob multimídia e submete o formulário via requisição HTTP POST.

2. Interceptação (Rotas): O arquivo `routes.py` recebe a requisição no endpoint correspondente, valida que o usuário está autenticado e encaminha os dados para o controlador.

3. Processamento (Controle & Helper):

* O `ciclo_controller.py` processa os campos de texto (resultados técnicos/musicais, emoções e diário).
* O `gravacao_controller.py` delega o arquivo de mídia para o media_upload_helper.py, que realiza o upload para o servidor do Cloudinary de forma assíncrona/direta e retorna a URL segura gerada.

4. Persistência (Modelo): Os modelos `CicloDeEstudo` e `Gravacao` realizam o mapeamento dos dados inseridos junto à URL de mídia, executando o commit no banco de dados através do SQLAlchemy.

### 5. Mecanismos de Segurança Implementados

* Criptografia de Senhas: Utilização de algoritmo de hashing seguro (Bcrypt) com geração de salt aleatório, garantindo que credenciais confidenciais nunca sejam salvas em texto puro na base de dados.

* Segurança de Sessão: Controle de estado baseado em cookies criptografados gerenciados pelo `Flask-Login`.

* Proteção de Dados Sensíveis: Isolamento completo de credenciais de produção (chaves de API, credenciais de banco de dados e servidor SMTP) por meio de variáveis de ambiente configuradas no arquivo `.env` e ocultadas do repositório público.

#### Este formato direto e padronizado fornece aos avaliadores uma visão transparente da engenharia por trás do CARDC, evidenciando boas práticas como o isolamento de serviços de infraestrutura (Cloudinary/Email) e a separação estrita entre rotas e regras de negócio.