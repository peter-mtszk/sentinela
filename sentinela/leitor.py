"""Leitor de logs de acesso no formato "combined" (Apache e Nginx).

Sua tarefa: completar as duas funções abaixo até todos os testes de tests/test_leitor.py passarem.
Rode os testes com:  .venv\\Scripts\\python -m pytest
"""

from datetime import datetime


def ler_linha(linha):
    """Recebe uma linha do log e devolve um dicionário com os campos,
    ou None se a linha não estiver no formato esperado.

    Campos: ip, quando (datetime com fuso), metodo, caminho, status (int),
    bytes (int, "-" vira 0), origem ("-" vira None) e agente.
    """
    # 1) Corta a linha nas aspas. Uma linha certa vira 7 pedaços:
    #    [0] '203.0.113.45 - - [28/Oct/2026:09:15:58 -0300] '
    #    [1] 'GET /produtos/42 HTTP/1.1'
    #    [2] ' 200 3310 '
    #    [3] 'https://exemplo.com.br/produtos'   (origem)
    #    [4] ' '
    #    [5] 'Mozilla/5.0 (iPhone; ...)'         (agente)
    #    [6] ''
    pedacos = linha.strip().split('"')
    if len(pedacos) != 7:                       # não tem 7 pedaços? não é uma linha de log
        return None

    # 2) Agora sim, corta cada pedaço nos espaços
    inicio = pedacos[0].split()                 # ['203.0.113.45', '-', '-', '[28/Oct/2026:09:15:58', '-0300]']
    pedido = pedacos[1].split()                 # ['GET', '/produtos/42', 'HTTP/1.1']
    numeros = pedacos[2].split()                # ['200', '3310']
    if len(inicio) != 5 or len(pedido) != 3 or len(numeros) != 2:
        return None

    # 3) Converte texto em data e em número. Se algo vier estranho, a linha é inválida.
    try:
        data_texto = inicio[3].lstrip("[") + " " + inicio[4].rstrip("]")   # '28/Oct/2026:09:15:58 -0300'
        quando = datetime.strptime(data_texto, "%d/%b/%Y:%H:%M:%S %z")
        status = int(numeros[0])
        tamanho = 0 if numeros[1] == "-" else int(numeros[1])
    except ValueError:
        return None

    return {
        "ip": inicio[0],
        "quando": quando,
        "metodo": pedido[0],
        "caminho": pedido[1],
        "status": status,
        "bytes": tamanho,
        "origem": None if pedacos[3] == "-" else pedacos[3],
        "agente": pedacos[5],
    }



def ler_arquivo(caminho_arquivo):
    """Lê o arquivo inteiro e devolve a lista de registros, pulando as linhas inválidas."""
    registros = []                                         # lista vazia que vamos encher
    with open(caminho_arquivo, encoding="utf-8") as arquivo:  # abre o arquivo e fecha sozinho no fim
        for linha in arquivo:                              # repete uma vez para cada linha
            registro = ler_linha(linha)                    # transforma o texto em dicionário
            if registro is not None:                       # linha inválida volta None: pula
                registros.append(registro)                 # guarda no fim da lista
    return registros
