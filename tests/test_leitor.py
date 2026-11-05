from datetime import datetime, timedelta, timezone

from sentinela.leitor import ler_arquivo, ler_linha

LINHA = '203.0.113.45 - - [28/Oct/2026:09:15:58 -0300] "GET /produtos/42 HTTP/1.1" 200 3310 "https://exemplo.com.br/produtos" "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X)"'


def test_le_os_campos_de_uma_linha():
    r = ler_linha(LINHA)
    assert r["ip"] == "203.0.113.45"
    assert r["metodo"] == "GET"
    assert r["caminho"] == "/produtos/42"
    assert r["status"] == 200          # número, não texto
    assert r["bytes"] == 3310          # número, não texto
    assert r["origem"] == "https://exemplo.com.br/produtos"
    assert r["agente"].startswith("Mozilla/5.0 (iPhone")


def test_converte_a_data_com_fuso():
    r = ler_linha(LINHA)
    assert r["quando"] == datetime(2026, 10, 28, 9, 15, 58, tzinfo=timezone(timedelta(hours=-3)))


def test_traco_vira_none():
    r = ler_linha('198.51.100.23 - - [28/Oct/2026:09:12:01 -0300] "GET / HTTP/1.1" 200 5320 "-" "Mozilla/5.0"')
    assert r["origem"] is None          # "-" no log significa "sem valor"


def test_bytes_traco_vira_zero():
    r = ler_linha('198.51.100.77 - - [28/Oct/2026:09:30:44 -0300] "GET /favicon.ico HTTP/1.1" 304 - "-" "Mozilla/5.0"')
    assert r["bytes"] == 0


def test_linha_invalida_devolve_none():
    assert ler_linha("esta linha está corrompida e não segue o formato") is None
    assert ler_linha("") is None


def test_le_o_arquivo_de_exemplo_e_pula_linhas_invalidas():
    registros = ler_arquivo("dados/exemplo_acesso.log")
    assert len(registros) == 9          # o arquivo tem 10 linhas, 1 é inválida
    assert registros[-1]["status"] == 500
