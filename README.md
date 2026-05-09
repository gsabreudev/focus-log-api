# 🧠 Focus Log API

> API de registro e diagnóstico inteligente de produtividade — Desafio Técnico

---

## 📌 Sobre o Projeto

A **Focus Log API** permite registrar sessões de trabalho/estudo com métricas de foco e, ao final, receber um **diagnóstico inteligente** sobre o seu período de trabalho.

### Stack utilizada

| Componente | Tecnologia |
|---|---|
| Linguagem | Python 3.11+ |
| Framework | FastAPI |
| Banco de dados | SQLite (via SQLAlchemy ORM) |
| Validação | Pydantic v2 |
| Servidor | Uvicorn |

---

## 🚀 Como rodar o projeto

### Pré-requisitos

- Python 3.11 ou superior
- `pip` atualizado

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/focus-log-api.git
cd focus-log-api
```

### 2. Crie e ative o ambiente virtual

```bash
# Criar
python -m venv venv

# Ativar — Linux/macOS
source venv/bin/activate

# Ativar — Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Suba o servidor

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: **http://localhost:8000**

---

## 📖 Documentação interativa

Após subir o servidor, acesse:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🛣 Endpoints

### `POST /registro-foco`

Registra uma sessão de trabalho recém-encerrada.

**Request body:**

```json
{
  "nivel_foco": 4,
  "tempo_minutos": 50,
  "comentario": "Implementei o endpoint de diagnóstico sem interrupções",
  "categoria": "coding",
  "tags": ["fastapi", "backend", "desafio"]
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `nivel_foco` | `int` | ✅ | Nível de 1 (distraído) a 5 (flow) |
| `tempo_minutos` | `int` | ✅ | Duração da sessão em minutos (> 0) |
| `comentario` | `string` | ✅ | O que foi feito ou o que causou distração |
| `categoria` | `string` | ❌ | coding / reunião / estudo / leitura / geral |
| `tags` | `list[string]` | ❌ | Palavras-chave da sessão |

**Response `201`:**

```json
{
  "id": 1,
  "nivel_foco": 4,
  "tempo_minutos": 50,
  "comentario": "Implementei o endpoint de diagnóstico sem interrupções",
  "categoria": "coding",
  "tags": ["fastapi", "backend", "desafio"],
  "criado_em": "2025-01-20T14:30:00Z"
}
```

---

### `GET /diagnostico-produtividade`

Retorna o diagnóstico completo com base em todos os registros.

**Response `200`:**

```json
{
  "total_registros": 5,
  "media_foco": 3.8,
  "tempo_total_minutos": 210,
  "tempo_total_horas": 3.5,
  "categoria_mais_frequente": "coding",
  "distribuicao_categorias": {
    "coding": 3,
    "reunião": 1,
    "estudo": 1
  },
  "sessao_mais_produtiva": { ... },
  "feedback": "Você está com um ótimo ritmo de foco! Continue protegendo seus blocos de trabalho profundo.",
  "nivel_energia": "🟢 Bom"
}
```

---

## 🎨 Diferenciais implementados

- ✅ **Campo `categoria`** — classifica o tipo de atividade da sessão
- ✅ **Campo `tags`** — permite etiquetar sessões com palavras-chave
- ✅ **Timestamp automático** — `criado_em` registra quando a sessão foi salva
- ✅ **Sessão mais produtiva** — identifica o melhor bloco do período
- ✅ **Distribuição por categoria** — mostra onde você passa mais tempo
- ✅ **Feedback em 5 níveis** — de "Crítico" a "Flow total 🚀"
- ✅ **Documentação automática** — Swagger e ReDoc disponíveis
- ✅ **Tratamento de erros** — validações com mensagens claras

---

## 🧪 Testando com curl

```bash
# Criar um registro
curl -X POST http://localhost:8000/registro-foco \
  -H "Content-Type: application/json" \
  -d '{"nivel_foco": 5, "tempo_minutos": 90, "comentario": "Deep work total", "categoria": "coding"}'

# Ver o diagnóstico
curl http://localhost:8000/diagnostico-produtividade
```

---

## 📁 Estrutura do projeto

```
focus-log-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # Configuração da aplicação e middlewares
│   ├── database.py      # Conexão SQLite e session factory
│   ├── models.py        # Modelos ORM (SQLAlchemy)
│   ├── schemas.py       # Schemas de validação (Pydantic)
│   ├── services.py      # Lógica de negócio e diagnóstico
│   └── routes/
│       ├── __init__.py
│       ├── registro.py  # POST /registro-foco
│       └── diagnostico.py # GET /diagnostico-produtividade
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🤖 Uso de IA

Este projeto foi desenvolvido com auxílio do **Claude (Anthropic)** para:
- Geração da estrutura inicial do projeto
- Sugestões de boas práticas FastAPI/SQLAlchemy
- Redação dos docstrings e README

Todo o código foi revisado, entendido e adaptado pelo desenvolvedor.

---

*Desenvolvido para o Desafio Técnico — Focus Log API*
