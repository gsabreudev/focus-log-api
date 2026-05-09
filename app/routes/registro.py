"""
routes/registro.py
------------------
Define o endpoint POST /registro-foco para criação de sessões de trabalho.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import RegistroFocoCreate, RegistroFocoOut
from ..services import criar_registro

router = APIRouter()


@router.post(
    "/registro-foco",
    response_model=RegistroFocoOut,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar uma sessão de foco",
    description=(
        "Salva os dados de um bloco de trabalho recém-encerrado. "
        "O campo `nivel_foco` deve ser um inteiro de 1 (muito distraído) a 5 (flow)."
    ),
)
def post_registro_foco(
    dados: RegistroFocoCreate,
    db: Session = Depends(get_db),
):
    """
    Cria um novo registro de foco.

    - **nivel_foco**: 1–5
    - **tempo_minutos**: duração da sessão (> 0)
    - **comentario**: o que foi feito ou o que causou distração
    - **categoria** *(opcional)*: coding | reunião | estudo | leitura | geral
    - **tags** *(opcional)*: lista de palavras-chave
    """
    try:
        registro = criar_registro(db, dados)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar o registro: {exc}",
        )

    return RegistroFocoOut.from_orm_with_tags(registro)
