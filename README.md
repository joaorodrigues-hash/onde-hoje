# Onde Hoje — Plataforma de Gestão e Descoberta de Eventos

Aplicação web completa desenvolvida para o mapeamento e promoção de eventos, com interface pública responsiva, portal exclusivo para produtores de eventos e painel administrativo protegido para moderação de conteúdo.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** FastAPI (Python 3.10+), Pydantic, Uvicorn
- **Base de Dados:** SQLite3 (com arquitetura modular em SQL nativo)
- **Segurança:** Autenticação HTTP Basic no Swagger, Criptografia SHA-256 e Sessões JWT (JSON Web Tokens)
- **Frontend:** HTML5 Semântico, Tailwind CSS, Chart.js, Vanilla JavaScript
- **Armazenamento:** Sistema de upload multipart físico (`/uploads`)
- **Qualidade/Testes:** Pytest e HTTPX para cobertura de endpoints REST

---

## 🚀 Como Executar o Projeto

### 1. Clonar e Instalar Dependências
```bash
# Na raiz do projeto:
pip install -r requirements.txt
```

### 2. Povoamento da Base de Dados (Seed Inicial)
Para carregar mais de 100 eventos realistas, categorias, parceiros e credenciais de avaliação:
```bash
python3 backend/seed.py
python3 backend/seed_mercos.py
```

### 3. Iniciar o Servidor
```bash
python3 backend/main.py
```
O servidor estará ativo em `http://127.0.0.1:8000`.

---

## 🔑 Credenciais de Acesso para Avaliação

### 1. Documentação da API (Swagger / OpenAPI)
- **URL:** `http://127.0.0.1:8000/docs`
- **Acesso Restrito (HTTP Basic Auth):**
  - **Avaliadores autorizados (E-mail / Senha):**
    - `joao.rodrigues@mercos.com` / `12345`
    - `renan@mercos.com` / `12345`
    - `niler.barcelos@mercos.com` / `12345`

### 2. Painel Administrativo e Moderação
- **Acesso:** Abrir `frontend/admin.html` no navegador.
- **Credenciais:** Qualquer um dos e-mails da Mercos listados acima com a senha `12345`.
- **Funcionalidades:** Moderação de propostas pendentes com notas internas, gestão de equipe, estatísticas visuais (Chart.js) e blindagem por token JWT.

### 3. Portal do Parceiro / Produtor
- **Acesso:** Abrir `frontend/parceiros.html` no navegador.
- **Conta de Demonstração pré-carregada:**
  - **E-mail:** `contato@vilacountry.com.br`
  - **Senha:** `parceiro123`
- **Funcionalidades:** Painel de métricas analíticas e acompanhamento dos próprios eventos publicados.

---

## 🧪 Testes Automatizados

O projeto conta com testes de integração cobrindo fluxos de API, autenticação e rotas públicas.
Para rodar os testes:

```bash
python3 -m pytest backend/test_main.py -v
```

---

## 📂 Estrutura de Arquivos Resumida

```text
meus-roles/
├── backend/
│   ├── database.py           # Conexão e esquemas de tabelas
│   ├── main.py               # Configurações FastAPI, CORS, middlewares e JWT
│   ├── security.py           # Funções de hashing (SHA-256) e validação
│   ├── seed.py               # Carga em massa de eventos e métricas
│   ├── seed_mercos.py        # Registro das credenciais dos avaliadores
│   ├── test_main.py          # Bateria de testes automatizados com Pytest
│   ├── uploads/              # Armazenamento físico das imagens
│   └── routers/              # Separação modular de rotas da API
├── frontend/                 # Aplicação SPA modular (HTML, JS, Tailwind)
├── requirements.txt
└── README.md
```