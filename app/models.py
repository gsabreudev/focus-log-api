"""
models.py
---------
Define o modelo de dados persistido no banco SQLite.
Cada instância de `RegistroFoco` representa uma sessão de trabalho registrada.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class RegistroFoco(Base):
    """
    Tabela `registros_foco` — armazena cada sessão de trabalho/estudo.

    Campos obrigatórios (conforme spec do desafio):
        - nivel_foco    : Inteiro de 1 (distraído) a 5 (flow).
        - tempo_minutos : Duração da sessão em minutos.
        - comentario    : Descrição da sessão ou causa de distração.

    Campos extras (diferenciais):
        - categoria     : Tipo de atividade (coding, reunião, estudo, etc.).
        - tags          : Palavras-chave separadas por vírgula.
        - criado_em     : Timestamp automático de criação.
    """

    __tablename__ = "registros_foco"

    id = Column(Integer, primary_key=True, index=True)
    nivel_foco = Column(Integer, nullable=False)
    tempo_minutos = Column(Integer, nullable=False)
    comentario = Column(String, nullable=False)
    categoria = Column(String, default="geral")       # diferencial
    tags = Column(String, default="")                  # diferencial — CSV
    criado_em = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),    # diferencial
    )
