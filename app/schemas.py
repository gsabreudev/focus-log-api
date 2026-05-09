"""
schemas.py
----------
Define os schemas Pydantic usados para validação de entrada (request body)
e serialização de saída (response body) dos endpoints da API.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Schemas de entrada
# ---------------------------------------------------------------------------

class RegistroFocoCreate(BaseModel):
    """
    Schema de entrada para POST /registro-foco.
    Valida e documenta os campos aceitos pelo endpoint.
    """

    nivel_foco: int = Field(
        ...,
        ge=1,
        le=5,
        description="Nível de foco de 1 (muito distraído) a 5 (estado de flow)",
        examples=[4],
    )
    tempo_minutos: int = Field(
        ...,
        gt=0,
        description="Duração da sessão em minutos (deve ser maior que zero)",
        examples=[45],
    )
    comentario: str = Field(
        ...,
        min_length=3,
        description="Descrição do que foi feito ou o que causou distração",
        examples=["Implementei o endpoint de diagnóstico sem interrupções"],
    )
    categoria: Optional[str] = Field(
        default="geral",
        description="Tipo de atividade: coding, reunião, estudo, leitura, geral…",
        examples=["coding"],
    )
    tags: Optional[list[str]] = Field(
        default=[],
        description="Lista de palavras-chave para classificação da sessão",
        examples=[["fastapi", "backend", "desafio"]],
    )

    @field_validator("comentario")
    @classmethod
    def comentario_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O comentário não pode ser apenas espaços em branco.")
        return v.strip()


# ---------------------------------------------------------------------------
# Schemas de saída
# ---------------------------------------------------------------------------

class RegistroFocoOut(BaseModel):
    """Schema de resposta para um único registro de foco."""

    id: int
    nivel_foco: int
    tempo_minutos: int
    comentario: str
    categoria: str
    tags: list[str]
    criado_em: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_with_tags(cls, obj):
        """Converte a string CSV de tags de volta para lista antes de retornar."""
        data = {
            "id": obj.id,
            "nivel_foco": obj.nivel_foco,
            "tempo_minutos": obj.tempo_minutos,
            "comentario": obj.comentario,
            "categoria": obj.categoria,
            "tags": [t.strip() for t in obj.tags.split(",") if t.strip()],
            "criado_em": obj.criado_em,
        }
        return cls(**data)


class DiagnosticoOut(BaseModel):
    """Schema de resposta para GET /diagnostico-produtividade."""

    total_registros: int
    media_foco: float = Field(description="Média aritmética do nível de foco (1–5)")
    tempo_total_minutos: int = Field(description="Soma de todos os minutos registrados")
    tempo_total_horas: float = Field(description="Tempo total convertido para horas")
    categoria_mais_frequente: Optional[str]
    distribuicao_categorias: dict[str, int]
    sessao_mais_produtiva: Optional[RegistroFocoOut]
    feedback: str = Field(description="Mensagem de diagnóstico gerada automaticamente")
    nivel_energia: str = Field(description="Classificação geral do período de trabalho")
