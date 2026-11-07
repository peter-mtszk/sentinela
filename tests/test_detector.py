from datetime import datetime, timedelta, timezone

from sentinela.detector import detectar
from sentinela.leitor import ler_arquivo

INICIO = datetime(2026, 11, 6, 21, 0, tzinfo=timezone(timedelta(hours=-3)))


def falha(ip, segundos):
    return {"ip": ip, "quando": INICIO + timedelta(seconds=segundos),
            "metodo": "POST", "caminho": "/login", "status": 401}


def test_arquivo_de_ataques_gera_os_dois_alertas():
    alertas = detectar(ler_arquivo("dados/ataques_acesso.log"))
    tipos = {(a["ip"], a["tipo"]) for a in alertas}
    assert tipos == {("203.0.113.99", "forca_bruta"), ("192.0.2.66", "varredura")}


def test_usuario_normal_nao_gera_alerta():
    alertas = detectar(ler_arquivo("dados/exemplo_acesso.log"))
    assert "198.51.100.23" not in {a["ip"] for a in alertas}


def test_quatro_falhas_ainda_nao_e_ataque():
    assert detectar([falha("192.0.2.9", s) for s in range(4)]) == []


def test_falhas_espalhadas_no_tempo_nao_sao_forca_bruta():
    # 5 erros de senha, um a cada 5 minutos: passa de 10 minutos, é alguém esquecido
    assert detectar([falha("192.0.2.9", m * 300) for m in range(5)]) == []
