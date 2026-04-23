# Ciclo Artístico-Reflexivo de Dupla Checagem
> “Acredita-se que a Prática Artística como metodologia possa colaborar na validação de procedimentos práticos aplicados ao estudo instrumental.” - Leonardo Vieira Feichas

#### O **CARDC** é uma plataforma web desenvolvida com a aplicação de uma ferramenta teórico-metodológica replicável específica para a construção de uma interpretação musical por estímulo autor reflexivo e autor regulatório.
#### Baseado na pesquisa do Dr. Leonardo Feichas, este projeto foi desenvolvido como parte de atividades acadêmicas na Universidade de Brasília (UnB), campus Gama (FGA), em colaboração com o Instituto Tecnológico de Aeronáutica (ITA).

## Funcionalidades Principais
* Gestão de Usuários: Sistema completo de cadastro, login e autenticação segura com criptografia de senhas via Bcrypt.
* Recuperação de Senha: Funcionalidade de redefinição de acesso via e-mail utilizando tokens temporários seguros.
* Ciclos de Estudo (CRUD): Criação, edição, visualização e remoção de registros detalhados de prática.
* Integração Multimídia:
  * Upload de fotos de perfil e vídeos de performance para o Cloudinary.
  * Gravação de vídeo diretamente pelo navegador (Webcam/WebRTC) integrada ao fluxo de envio.
* Persistência de Dados: Armazenamento estruturado utilizando SQLAlchemy ORM para garantir integridade entre usuários, ciclos e gravações.

## Stack Tecnológica
* Linguagem: Python 3.x
* Framework Web: [Flask](https://flask.palletsprojects.com/en/stable/)
* Banco de Dados: PostgreSQL (Produção) / SQLite (Desenvolvimento/Testes)
* Servidor WSGI: Gunicorn
* Armazenamento de Mídia:[Cloudinary](https://cloudinary.com/)
* Segurança: Flask-Bcrypt e URLSafeTimedSerializer
* Testes: Pytest e Pytest-Mock

## Metodologia Aplicada no Software

#### A estrutura do aplicativo foi traduzida no fluxo metodológico do CARDC:
1. Estruturação: Definição da obra e compositor.
2. Estratégias/Objetivos: Preenchimento das considerações preliminares e descrição da tarefa.
3. Aplicação/Prática: Realização do estudo com registro de data e gravação audiovisual.
4. Autoavaliação: Registro de resultados técnicos e musicais, seguidos por observações subjetivas (pensamentos e emoções).
5. Diário Reflexivo: Consolidação de insights para o planejamento do próximo ciclo.

#### A metodologia CARDC é densa, caso queira saber mais sobre acesse a área de documentação para mais informações. 👍

## Configuração e Instalação

#### Pré-requisitos
* Python 3.10+
* Conta no Cloudnary (para upload de mídia)
* Conta no Render (para deploy)
* Servidor SMTP (Gmail/Outlook) para envio de e-mails

#### Passo a passo
1. Clonar o repositório:
`git clone https://github.com/ArthurLuizUnB/CARDC.git
cd CARDC`
2. Criar ambiente virtual:
`python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows`
3. Instalar dependências:
`pip install -r requirements.txt`
4. Configurar variáveis de ambiente na raiz (criar um .env):
`SECRET_KEY=sua_chave_secreta
DATABASE_URL=seu_link_do_banco
CLOUDINARY_CLOUD_NAME=seu_name
CLOUDINARY_API_KEY=sua_key
CLOUDINARY_API_SECRET=seu_secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=seu_email
MAIL_PASSWORD=sua_senha_app`
5. Inicializar o Banco de Dados:
`python MusicBeta_V02/Main/init_db_script.py`
6. Executar:
`flask run`

## Testes

#### O projeto utiliza a suíte de testes pytest para garantir a estabilidade dos controladores e auxiliares de mídia.
Para rodar os testes:
`pytest`

### Autoria e Agradecimentos
* Desenvolvimento de Software: Arthur Luiz
* Metodologia e Orientação: Leonardo Vieira Feichas e Carlos Henrique
* Instituições: Universidade de Brasília (UnB) e Instituto Tecnológico de Aeronáutica (ITA)
