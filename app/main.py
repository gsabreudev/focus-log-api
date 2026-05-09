"""
Focus Log API - Backend de Produtividade
========================================
API para registrar sessões de foco e gerar diagnósticos inteligentes
de produtividade com base nos dados coletados.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import registro, diagnostico
from .database import init_db

# Inicializa a aplicação FastAPI com metadados para documentação automática
app = FastAPI(
    title="Focus Log API",
    description="Log de Performance e Diagnóstico de Produtividade",
    version="1.0.0",
)

# Permite requisições de qualquer origem (útil para integração com frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra os roteadores de cada domínio da aplicação
app.include_router(registro.router, tags=["Registros"])
app.include_router(diagnostico.router, tags=["Diagnóstico"])


@app.on_event("startup")
def startup():
    """Inicializa o banco de dados SQLite ao subir a aplicação."""
    init_db()


@app.get("/", tags=["Health"])
def root():
    """Endpoint raiz — verifica se a API está no ar."""
    return {"status": "ok", "mensagem": "Focus Log API rodando com sucesso 🚀"}
