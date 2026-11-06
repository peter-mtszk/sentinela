"""Conta quantas requisições cada IP fez.

É o primeiro passo de uma investigação: um IP que aparece muito mais
que os outros merece atenção (força bruta, varredura, robô).
"""


def contar_por_ip(registros):
    """Recebe a lista de registros (de ler_arquivo) e devolve um dicionário
    {ip: quantidade}. Ex.: {"203.0.113.99": 7, "192.0.2.66": 8}
    """
    contagem = {}               # dicionário vazio: o "placar" de cada IP

    for registro in registros:      # 1) repete para cada registro da lista
        ip = registro["ip"]         # 2) pega o IP desse registro
        if ip not in contagem:      # 3) IP novo? começa o placar em 0
            contagem[ip] = 0
        contagem[ip] += 1           # 4) soma 1 no placar desse IP

    return contagem
