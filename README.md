# 🤖 Sistema RAG - Ingestão e Busca em Documentos PDF

Sistema de Recuperação Aumentada por Geração (RAG) desenvolvido como parte do MBA em Engenharia de Software com IA da Full Cycle. O projeto permite fazer perguntas inteligentes sobre documentos PDF usando embeddings vetoriais e modelos de linguagem.

## 📋 Objetivo do Projeto

Este projeto implementa um pipeline completo de RAG que:

1. **Ingestão**: Processa documentos PDF, divide em chunks e gera embeddings
2. **Armazenamento**: Armazena os embeddings em um banco de dados vetorial (PostgreSQL + pgvector)
3. **Busca Semântica**: Recupera os trechos mais relevantes do documento baseado em similaridade
4. **Geração de Respostas**: Utiliza LLM para gerar respostas contextualizadas baseadas apenas no conteúdo do documento

## 🚀 Tecnologias Utilizadas

### Backend & IA
- **Python 3.x** - Linguagem principal
- **LangChain** - Framework para desenvolvimento de aplicações com LLMs
- **OpenAI API** - Embeddings (text-embedding-3-small) e Chat (GPT)
- **PyPDF** - Processamento e leitura de arquivos PDF
- **python-dotenv** - Gerenciamento de variáveis de ambiente

### Banco de Dados
- **PostgreSQL 17** - Banco de dados relacional
- **pgvector** - Extensão para armazenamento e busca de embeddings vetoriais
- **SQLAlchemy** - ORM para Python

### Infraestrutura
- **Docker & Docker Compose** - Containerização e orquestração
- **asyncpg** - Driver assíncrono para PostgreSQL

## 📁 Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
│
├── src/                      # Código fonte da aplicação
│   ├── ingest.py            # Script de ingestão de documentos
│   ├── search.py            # Template de prompts e funções de busca
│   └── chat.py              # Interface CLI para interação
│
├── document.pdf             # Documento PDF para processamento
├── docker-compose.yml       # Configuração dos serviços (PostgreSQL + pgvector)
├── requirements.txt         # Dependências Python
├── .env                     # Variáveis de ambiente (criar)
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Este arquivo
```

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Docker** e **Docker Compose** ([Instalar Docker](https://docs.docker.com/get-docker/))
- **Python 3.9+** ([Instalar Python](https://www.python.org/downloads/))
- **Chave de API da OpenAI** ([Obter chave](https://platform.openai.com/api-keys))

## 🔧 Configuração e Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd mba-ia-desafio-ingestao-busca
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# OpenAI Configuration
OPENAI_API_KEY=sua-chave-api-aqui
OPENAI_MODEL=text-embedding-3-small

# PostgreSQL + pgvector Configuration
PGVECTOR_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=documents
```

### 3. Inicie o banco de dados

Execute o Docker Compose para subir o PostgreSQL com pgvector:

```bash
docker-compose up -d
```

Aguarde alguns segundos até o banco estar pronto. Você pode verificar o status com:

```bash
docker-compose ps
```

### 4. Instale as dependências Python

#### Opção 1: Usando ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Adicione seu documento PDF

Coloque o arquivo PDF que deseja processar na raiz do projeto com o nome `document.pdf`, ou edite o caminho no arquivo `src/ingest.py`.

## 📖 Como Usar

### Passo 1: Ingestão do Documento

Execute o script de ingestão para processar o PDF e armazenar os embeddings:

```bash
python src/ingest.py
```

Este processo irá:
- Carregar o arquivo PDF
- Dividir o texto em chunks de 1000 caracteres (com overlap de 150)
- Gerar embeddings usando OpenAI
- Armazenar no banco de dados vetorial

### Passo 2: Interaja com o Chat

Execute o script de chat para fazer perguntas sobre o documento:

```bash
python src/chat.py
```

Você verá a interface:

```
============================================================
CHAT COM DOCUMENTOS PDF
============================================================
Faça suas perguntas sobre o documento.
Digite 'sair' para encerrar.

PERGUNTA: 
```

### Exemplos de Uso

```
PERGUNTA: Qual é o tema principal do documento?
RESPOSTA: [Resposta baseada no conteúdo do PDF]

PERGUNTA: Quais são os pontos mais importantes mencionados?
RESPOSTA: [Resposta baseada no conteúdo do PDF]

PERGUNTA: sair
Encerrando. Até logo!
```

## 🎯 Características Técnicas

### Sistema de Busca Vetorial
- **Modelo de Embedding**: text-embedding-3-small (OpenAI)
- **Chunk Size**: 1000 caracteres
- **Chunk Overlap**: 150 caracteres
- **Top-K**: 10 documentos mais relevantes

### Geração de Respostas
- **Modelo LLM**: GPT (configurável)
- **Temperatura**: 0 (respostas determinísticas)
- **Estratégia**: Responde apenas com base no contexto fornecido

### Segurança e Boas Práticas
- ✅ Variáveis de ambiente para credenciais sensíveis
- ✅ Validação de variáveis obrigatórias
- ✅ Tratamento de erros
- ✅ Prompts estruturados para evitar alucinações

## 🛠️ Comandos Úteis

### Gerenciamento do Docker

```bash
# Iniciar os serviços
docker-compose up -d

# Parar os serviços
docker-compose down

# Ver logs
docker-compose logs -f

# Reiniciar os serviços
docker-compose restart

# Remover tudo (incluindo dados)
docker-compose down -v
```

### Desenvolvimento

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Desativar ambiente virtual
deactivate

# Atualizar dependências
pip install -r requirements.txt --upgrade
```

## 🐛 Solução de Problemas

### Erro: "Environment variable X is not set"
**Solução**: Verifique se o arquivo `.env` existe e contém todas as variáveis necessárias.

### Erro de conexão com PostgreSQL
**Solução**: 
1. Verifique se o Docker está rodando: `docker ps`
2. Verifique se o PostgreSQL está saudável: `docker-compose ps`
3. Aguarde alguns segundos para o banco inicializar completamente

### Erro de API Key da OpenAI
**Solução**: 
1. Verifique se a chave está correta no arquivo `.env`
2. Confirme se tem créditos disponíveis na conta OpenAI
3. Teste a chave em: https://platform.openai.com/api-keys

### PDF não encontrado
**Solução**: Certifique-se de que o arquivo `document.pdf` está na raiz do projeto.

## 📚 Referências e Documentação

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Docker Compose Reference](https://docs.docker.com/compose/)

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como parte do MBA em Engenharia de Software com IA da Full Cycle.

## 🤝 Contribuições

Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias!

---

**Desenvolvido por Samuel Britto para o Desafio Técnico - Full Cycle**