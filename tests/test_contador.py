from sentinela.contador import contar_por_ip
from sentinela.leitor import ler_arquivo


def test_lista_vazia_da_placar_vazio():
    assert contar_por_ip([]) == {}


def test_conta_cada_ip():
    registros = [{"ip": "192.0.2.1"}, {"ip": "192.0.2.2"}, {"ip": "192.0.2.1"}]
    assert contar_por_ip(registros) == {"192.0.2.1": 2, "192.0.2.2": 1}


def test_conta_o_arquivo_de_ataques():
    contagem = contar_por_ip(ler_arquivo("dados/ataques_acesso.log"))
    assert contagem["203.0.113.99"] == 7     # força bruta: 6 falhas + 1 login
    assert contagem["192.0.2.66"] == 8       # varredura
    assert contagem["198.51.100.23"] == 2    # usuário normal
