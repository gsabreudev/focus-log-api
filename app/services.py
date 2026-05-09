"""
services.py
-----------
Camada de serviço — contém a lógica de negócio da aplicação.
Mantida separada das rotas para facilitar testes unitários e reutilização.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import Counter

from . import models
from .schemas import RegistroFocoCreate, RegistroFocoOut, DiagnosticoOut


# ---------------------------------------------------------------------------
# Serviço de Registro
# ---------------------------------------------------------------------------

def criar_registro(db: Session, dados: RegistroFocoCreate) -> models.RegistroFoco:
    """
    Persiste um novo registro de foco no banco de dados.
    Converte a lista de tags para string CSV antes de salvar.
    """
    tags_csv = ",".join(dados.tags) if dados.tags else ""

    registro = models.RegistroFoco(
        nivel_foco=dados.nivel_foco,
        tempo_minutos=dados.tempo_minutos,
        comentario=dados.comentario,
        categoria=dados.categoria or "geral",
        tags=tags_csv,
    )
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro


# ---------------------------------------------------------------------------
# Serviço de Diagnóstico
# ---------------------------------------------------------------------------

def gerar_diagnostico(db: Session) -> DiagnosticoOut:
    """
    Agrega todos os registros e retorna um diagnóstico inteligente de
    produtividade com métricas e feedback automático.
    """
    registros = db.query(models.RegistroFoco).all()

    if not registros:
        return DiagnosticoOut(
            total_registros=0,
            media_foco=0.0,
            tempo_total_minutos=0,
            tempo_total_horas=0.0,
            categoria_mais_frequente=None,
            distribuicao_categorias={},
            sessao_mais_produtiva=None,
            feedback="Nenhum registro encontrado. Comece a registrar suas sessões!",
            nivel_energia="—",
        )

    # --- Métricas básicas ---
    total = len(registros)
    media_foco = sum(r.nivel_foco for r in registros) / total
    tempo_total = sum(r.tempo_minutos for r in registros)

    # --- Distribuição por categoria ---
    categorias = [r.categoria for r in registros]
    dist_categorias = dict(Counter(categorias))
    categoria_top = max(dist_categorias, key=dist_categorias.get)

    # --- Sessão mais produtiva (maior nível de foco; desempate pelo tempo) ---
    sessao_top = max(registros, key=lambda r: (r.nivel_foco, r.tempo_minutos))

    # --- Feedback e classificação inteligente ---
    feedback, nivel_energia = _gerar_feedback(media_foco, tempo_total, total)

    return DiagnosticoOut(
        total_registros=total,
        media_foco=round(media_foco, 2),
        tempo_total_minutos=tempo_total,
        tempo_total_horas=round(tempo_total / 60, 1),
        categoria_mais_frequente=categoria_top,
        distribuicao_categorias=dist_categorias,
        sessao_mais_produtiva=RegistroFocoOut.from_orm_with_tags(sessao_top),
        feedback=feedback,
        nivel_energia=nivel_energia,
    )


def _gerar_feedback(media: float, tempo: int, total: int) -> tuple[str, str]:
    """
    Gera uma mensagem de feedback e classifica o nível de energia
    com base na média de foco, tempo total e quantidade de sessões.

    Retorna:
        (mensagem_feedback, classificacao_nivel_energia)
    """
    # Nível de energia com base na média de foco
    if media < 2:
        nivel = "🔴 Crítico"
        msg = (
            "Seu foco está muito baixo. Experimente sessões menores (Pomodoro de 25 min), "
            "elimine notificações e identifique o maior distrator do seu ambiente."
        )
    elif media < 3:
        nivel = "🟠 Abaixo do ideal"
        msg = (
            "Você até está trabalhando, mas as distrações estão pesando. "
            "Considere pausas mais longas entre sessões e revisar suas prioridades do dia."
        )
    elif media < 4:
        nivel = "🟡 Moderado"
        msg = (
            "Desempenho razoável! Algumas sessões foram boas, outras não. "
            "Tente identificar o que diferencia suas melhores sessões e replique esse contexto."
        )
    elif media < 4.5:
        nivel = "🟢 Bom"
        msg = (
            "Você está com um ótimo ritmo de foco! "
            "Continue protegendo seus blocos de trabalho profundo — você está quase no flow."
        )
    else:
        nivel = "🚀 Flow total"
        msg = (
            "Incrível! Você está em uma maratona produtiva de alto nível. "
            "Documente o que está funcionando — esse estado é raro e valioso."
        )

    # Ajuste adicional baseado em volume de sessões
    if total >= 5 and media >= 4:
        msg += " Consistência + alto foco = resultados exponenciais. 🎯"
    elif total == 1:
        msg += " Registre mais sessões para um diagnóstico mais preciso."

    return msg, nivel
