"""
routes/diagnostico.py
---------------------
Define o endpoint GET /diagnostico-produtividade para análise agregada.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import DiagnosticoOut
from ..services import gerar_diagnostico

router = APIRouter()


@router.get(
    "/diagnostico-produtividade",
    response_model=DiagnosticoOut,
    summary="Diagnóstico inteligente de produtividade",
    description=(
        "Retorna um resumo analítico de todas as sessões registradas, incluindo "
        "média de foco, tempo total, distribuição por categoria e feedback automático."
    ),
)
def get_diagnostico(db: Session = Depends(get_db)):
    """
    Gera o diagnóstico com base em todos os registros salvos.

    Retorna:
    - **media_foco**: média aritmética do nível de foco (1–5)
    - **tempo_total_minutos / horas**: soma de todas as sessões
    - **categoria_mais_frequente**: tipo de atividade predominante
    - **distribuicao_categorias**: contagem por categoria
    - **sessao_mais_produtiva**: registro com maior nível de foco
    - **feedback**: mensagem diagnóstica gerada automaticamente
    - **nivel_energia**: classificação geral do período
    """
    return gerar_diagnostico(db)
