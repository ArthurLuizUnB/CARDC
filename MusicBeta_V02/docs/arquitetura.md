# Documento de Arquitetura do Sistema (DAS)

## Projeto: CARDC (Ciclo Artístico-Reflexivo de Dupla Checagem)

### 1. Visão Geral do Sistema

#### O **CARDC** é um aplicativo web projetado para servir como um diário de bordo digital na prática instrumental deliberada. O sistema fornece uma infraestrutura tecnológica capaz de transpor os protocolos objetivos e subjetivos da metodologia **CARDC** para um ambiente seguro, permitindo o registro de sessões de estudo, autoavaliação etnográfica, salvamento contínuo e exportação acadêmica de documentos, além do armazenamento de evidências multimídia (vídeo e áudio).

### 2. Padrão Arquitetural

#### O sistema adota o padrão **MVC (Model-View-Controller)** adaptado para o ecossistema Flask, com uma separação clara de responsabilidades em camadas independentes para desacoplamento de código e facilidade de manutenção e testes.

```
[ Camada de Visão / Cliente ] (HTML Puro + CSS + static/js/*)
                       │  ▲
    Requisições HTTP   │  │  Renderização Dinâmica (Jinja2) / JSON (Fetch)
                       ▼  │
       [ Camada de Roteamento ] (Blueprints / routes.py)
                       │  ▲
       Chamada Direta  │  │  Retorno de Dados / Status / Streams
                       ▼  │
       [ Camada de Controle ] (controllers/) ───► [ Helpers / Serviços ] (Cloudinary/Mail/Export)
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
├── requirements.txt            # Manifesto de dependências e bibliotecas do projeto (codificado em UTF-8).
├── init_db_script.py           # Script utilitário para criação e inicialização das tabelas do banco de dados via ORM.
│
├── models/                     # CAMADA DE MODELO: Definição de dados e persistência (ORM)
│   ├── database_config.py      # Instanciação centralizada do SQLAlchemy para evitar importações circulares.
│   ├── bcrypt_config.py        # Instanciação centralizada do componente de criptografia.
│   ├── usuario.py              # Modelo de Entidade "User" com regras de autenticação.
│   ├── ciclo_de_estudo.py      # Modelo de Entidade "Ciclo" contendo os campos da ficha de registro.
│   └── gravacao.py             # Modelo de Entidade "Gravacao" mapeando os metadados dos arquivos enviados à nuvem.
│
├── controllers/                # CAMADA DE CONTROLE: Implementação das regras de negócio
│   ├── auth_controller.py      # Lógica de controle de acesso (registro, login, logout e geração de tokens de senha).
│   ├── ciclo_controller.py     # Controlador responsável pelas operações de CRUD dos ciclos de estudo.
│   └── gravacao_controller.py  # Controlador encarregado de vincular mídias enviadas aos seus respectivos ciclos.
│
├── routes/                     # CAMADA DE ROTEAMENTO: Exposição de endpoints HTTP e JSON
│   └── routes.py               # Definição de Blueprints, interceptação de requisições e proteção de rotas (@login_required).
│
├── helpers/                    # CAMADA DE SERVIÇOS / UTILS: Integrações externas e geradores
│   ├── media_upload_helper.py  # Abstração de infraestrutura para comunicação direta com a API do Cloudinary (SDK).
│   ├── export_helper.py        # Geração em memória (BytesIO) de documentos formatados (.pdf, .docx e .txt) dos ciclos.
│   └── mail_config.py          # Configuração e inicialização do serviço SMTP (Flask-Mail) para notificações.
│
├── views/                      # CAMADA DE VISÃO: Relação com o usuário
│   └── html/                   # Templates estruturados em Jinja2 puro (sem scripts inline).
│
├── static/                     # RECURSOS ESTÁTICOS E COMPORTAMENTO CLIENTE
│   ├── css/style.css           # Folha de estilo centralizada da interface visual.
│   └── js/
│       ├── autosave.js         # Gerencia o salvamento automático (Debounce de 6s), balão flutuante e toggle de finalização.
│       ├── biblioteca.js       # Controla o menu contextual de 3 barras e o modal de exportação na Biblioteca.
│       ├── recorder.js         # Manipula as abas de mídia e a API nativa MediaRecorder para captura de áudio/vídeo.
│       └── tooltips.js         # Gerencia a exibição dos balões de ajuda metodológica nos campos do formulário.
│
└── tests/                      # SUÍTE DE TESTES AUTOMATIZADOS (Pytest)
    ├── conftest.py             # Configuração de fixtures e banco SQLite em memória (:memory:) para testes isolados.
    ├── test_export_helper.py   # Testes unitários da geração de documentos (.txt, .pdf e .docx) e tratamento de campos.
    ├── test_gravacao_controller.py
    └── test_media_upload_helper.py
```

---

### 4. Documentação de Funcionamento das Implementações

#### 4.1. Fluxo de Salvamento de Ciclo e Upload de Mídia
1. **Captura e Envio (Visão):** O usuário registra sua prática instrumental; o arquivo `recorder.js` gerencia a seleção/gravação de mídia e o formulário submete os dados via requisição HTTP POST.
2. **Interceptação (Rotas):** O arquivo `routes.py` recebe a requisição no endpoint correspondente, valida que o usuário está autenticado (`@login_required`) e encaminha os dados para o controlador.
3. **Processamento (Controle & Helper):**
   * O `ciclo_controller.py` persiste os campos de texto metodológicos.
   * O `gravacao_controller.py` delega o arquivo de mídia para o `media_upload_helper.py`, que realiza o upload para o Cloudinary e retorna a URL segura gerada.
4. **Persistência (Modelo):** Os modelos `CicloDeEstudo` e `Gravacao` realizam o mapeamento dos dados inseridos junto à URL de mídia, executando o commit no banco de dados através do SQLAlchemy.

---

#### 4.2. Salvamento Automático (Auto-Save) com Buffer de Inatividade e Balão Flutuante
* **Objetivo:** Evitar a perda acidental de reflexões durante a prática musical e eliminar a dependência de cliques manuais constantes no botão "Salvar".
* **Arquivos Envolvidos:** `static/js/autosave.js`, `views/html/form_ciclo.html`, `routes/routes.py` (`autosave_ciclo`) e `static/css/style.css`.
* **Como Funciona:**
  1. **Monitoramento e Debounce (`6000ms`):** O script `autosave.js` escuta eventos `input` em todos os 13 campos de texto do formulário. A cada tecla pressionada, um temporizador interno é reiniciado. O envio ao servidor só é disparado quando o usuário permanece **6 segundos sem digitar** (evitando sobrecarga de requisições no servidor).
  2. **Suporte a Ciclos Novos e Existentes (`/ciclo/autosave`):**
     * Se o formulário já possui um `ciclo_id` (edição), o backend valida a autoria do usuário e atualiza os campos no banco via `CicloController.atualizar(ciclo)`.
     * Se o usuário está na tela de **Novo Ciclo** (`/ciclo/novo`) e ainda não possui `ciclo_id`, o primeiro disparo do auto-save cria automaticamente o registro no banco (`CicloController.adicionar(ciclo)`), retorna o novo `ciclo_id` em JSON e o `autosave.js` atualiza silenciosamente a URL do navegador para `/ciclo/editar/<id>` usando `window.history.replaceState` (sem recarregar a página e evitando duplicação de ciclos).
  3. **Feedback Visual (Balão Flutuante `#autosave-toast`):** Quando o salvamento inicia, um balão flutuante fixo no canto inferior direito da tela exibe `"Salvando ciclo..."`, transita para `"✓ Ciclo salvo"` em tom verde sálvia pastel após a confirmação do servidor e desaparece suavemente após `3,2` segundos.
  4. **Finalização Rápida e Proteção de Saída:**
     * O rodapé do formulário conta com um botão-pílula interativo (`Marcar ciclo como finalizado` / `Ciclo marcado como finalizado`) que dispara o salvamento imediatamente ao ser alternado.
     * Caso o usuário clique em `"← Voltar para a Biblioteca"` antes de completar os 6 segundos de inatividade, o `autosave.js` intercepta a navegação, executa o salvamento pendente na hora e só então redireciona.

---

#### 4.3. Exportação de Ciclos em Documentos Formatados (`.pdf`, `.docx`, `.txt`)
* **Objetivo:** Permitir que o artista-pesquisador exporte seus ciclos de estudo em formatos portáteis para leitura, impressão, edição e citação em teses/dissertações.
* **Arquivos Envolvidos:** `helpers/export_helper.py`, `routes/routes.py` (`exportar_ciclo`), `views/html/home.html`, `static/js/biblioteca.js` e `tests/test_export_helper.py`.
* **Como Funciona:**
  1. **Menu Contextual e Modal Único (`home.html` + `biblioteca.js`):**
     * Na Biblioteca, cada ciclo possui um botão discreto de 3 barras horizontais (`☰`) que abre um menu flutuante com as opções `Exportar documento...`, `Finalizar ciclo` e `Excluir ciclo` (com confirmação de segurança).
     * Ao clicar em `Exportar documento...`, abre-se uma única janela `<dialog id="modal-exportar">` reutilizada dinamicamente para qualquer ciclo da lista (otimizando o uso de memória DOM no navegador), oferecendo os formatos **PDF**, **DOCX** e **TXT**.
  2. **Padronização Metodológica (`obter_campos_ciclo`):** Centraliza a extração dos metadados e das 9 seções reflexivas na ordem oficial do CARDC. Campos em branco ou `None` recebem automaticamente a indicação `"Nenhum conteúdo registrado"`, mantendo a integridade estrutural do documento.
  3. **Geração 100% em Memória RAM (`io.BytesIO`):**
     * `gerar_txt(ciclo)`: Gera arquivo texto codificado em `UTF-8` com divisores visuais.
     * `gerar_pdf(ciclo)`: Utiliza a biblioteca `ReportLab` (`SimpleDocTemplate` e `Paragraph`) para construir um PDF paginado em folha A4 com quebra automática de linhas longas.
     * `gerar_docx(ciclo)`: Utiliza a biblioteca `python-docx` para estruturar cabeçalhos e parágrafos editáveis no Microsoft Word / Google Docs.
     * Nenhum arquivo temporário é gravado no disco do servidor; o buffer em memória é entregue diretamente pela rota `/ciclo/exportar/<ciclo_id>/<formato>` via `send_file(..., as_attachment=True)`.

---

#### 4.4. Isolamento Estrito entre HTML e JavaScript (`views/html/` vs `static/js/`)
* **Diretriz Arquitetural:** Nenhum template em `views/html/` contém blocos `<script>` inline ou atributos de evento `onclick="..."` misturados às tags HTML.
* **Comunicação via Atributos `data-*`:** Os elementos HTML declaram apenas atributos de dados semânticos (como `data-menu-target`, `data-ciclo-id`, `data-aba-midia` e `data-confirm`), enquanto os módulos em `static/js/` (`autosave.js`, `biblioteca.js`, `recorder.js` e `tooltips.js`) registram os ouvintes de eventos via `addEventListener`. Isso garante segurança contra quebras por caracteres especiais (aspas em nomes de obras) e facilita a manutenção.

---

### 5. Mecanismos de Segurança Implementados

* **Criptografia de Senhas:** Utilização de algoritmo de hashing seguro (Bcrypt) com geração de salt aleatório, garantindo que credenciais confidenciais nunca sejam salvas em texto puro na base de dados.
* **Controle de Acesso e Propriedade:** Todas as rotas de visualização, edição, salvamento automático, exportação e remoção validam se o usuário está autenticado (`@login_required`) e se `ciclo.id_usuario == g.usuario_atual.id`.
* **Proteção de Dados Sensíveis:** Isolamento completo de credenciais de produção (chaves de API, credenciais de banco de dados e servidor SMTP) por meio de variáveis de ambiente configuradas no arquivo `.env` e ocultadas do repositório público.
