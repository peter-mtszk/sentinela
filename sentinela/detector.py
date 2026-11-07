"""Detector de ataques: olha os registros do log e devolve alertas.

Duas regras, as mesmas do ROADMAP:
- Força bruta: 5 ou mais POST /login com falha (401) do mesmo IP em 10 minutos.
- Varredura: 5 ou mais respostas 404 do mesmo IP em 5 minutos.
"""

from datetime import timedelta

REGRAS = {
    "forca_bruta": {"limite": 5, "janela": timedelta(minutes=10)},
    "varredura": {"limite": 5, "janela": timedelta(minutes=5)},
}


def _eh_falha_de_login(r):
    return r["metodo"] == "POST" and r["caminho"] == "/login" and r["status"] == 401


def _eh_pagina_inexistente(r):
    return r["status"] == 404


def _horarios_por_ip(registros, filtro):
    """Separa os horários dos registros que passam no filtro, um grupo por IP."""
    grupos = {}
    for r in registros:
        if filtro(r):
            grupos.setdefault(r["ip"], []).append(r["quando"])
    return grupos


def _janela_estourou(horarios, limite, janela):
    """True se, em algum trecho de tempo do tamanho da janela, couberem `limite` eventos.

    Ideia: com os horários em ordem, o evento i e o evento i+limite-1 estão
    a menos de `janela` de distância? Então houve `limite` eventos nesse trecho.
    """
    horarios = sorted(horarios)
    for i in range(len(horarios) - limite + 1):
        if horarios[i + limite - 1] - horarios[i] <= janela:
            return True
    return False


def detectar(registros):
    """Devolve a lista de alertas: {"ip", "tipo", "quantidade"}, um por IP e tipo."""
    alertas = []
    checagens = [
        ("forca_bruta", _eh_falha_de_login),
        ("varredura", _eh_pagina_inexistente),
    ]
    for tipo, filtro in checagens:
        regra = REGRAS[tipo]
        for ip, horarios in _horarios_por_ip(registros, filtro).items():
            if _janela_estourou(horarios, regra["limite"], regra["janela"]):
                alertas.append({"ip": ip, "tipo": tipo, "quantidade": len(horarios)})
    return alertas
