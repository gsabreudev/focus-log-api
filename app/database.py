"""
database.py
-----------
Configura a conexão com o banco de dados SQLite usando SQLAlchemy.
O arquivo `focus_log.db` é criado automaticamente na raiz do projeto.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# URL do banco SQLite — arquivo local, simples e sem necessidade de servidor
DATABASE_URL = "sqlite:///./focus_log.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necessário para SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Classe base para todos os modelos ORM do projeto."""
    pass


def get_db():
    """
    Dependency do FastAPI que fornece uma sessão de banco de dados
    e garante que ela seja fechada após cada requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Cria todas as tabelas definidas nos modelos, se ainda não existirem."""
    from . import models  # noqa: F401 — importação necessária para registrar os modelos
    Base.metadata.create_all(bind=engine)
