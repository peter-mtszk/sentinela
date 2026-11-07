"""Gerador de tráfego do laboratório, para testar o Sentinela no seu próprio computador.

Fala só com 127.0.0.1 (o servidor que você subiu em lab/servidor.py). Ele produz
três tipos de visitante, para o detector ter o que separar:

- normal: entra, erra a senha uma vez e acerta;
- senha-errada: repete POST /login com senha errada (o cenário "força bruta");
- paginas-escondidas: pede vários caminhos que não existem (o cenário "varredura").

Cada visitante manda um IP falso no cabeçalho X-Lab-IP, só para o log distinguir um do
outro. Isso é truque de laboratório; não serve para esconder ninguém de verdade.

Uso:  py lab/trafego.py            (roda os três)
      py lab/trafego.py normal     (roda só um)
"""

import sys
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8080"


def pedir(metodo, caminho, ip, corpo=None, agente="curl-lab/1.0"):
    dados = corpo.encode() if corpo else None
    req = urllib.request.Request(BASE + caminho, data=dados, method=metodo,
                                 headers={"X-Lab-IP": ip, "User-Agent": agente})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code            # 401, 404 etc. também interessam
    except urllib.error.URLError:
        print("  Servidor fora do ar. Rode antes:  py lab/servidor.py")
        sys.exit(1)


def normal(ip="198.51.100.23"):
    print("normal: um usuário comum")
    pedir("GET", "/login", ip, agente="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    pedir("POST", "/login", ip, "usuario=aluno&senha=errei")      # errou uma vez
    pedir("POST", "/login", ip, "usuario=aluno&senha=lab-2026")   # acertou
    time.sleep(0.2)


def senha_errada(ip="203.0.113.99"):
    print("senha-errada: 6 tentativas seguidas com senha errada (força bruta)")
    for i in range(6):
        st = pedir("POST", "/login", ip, f"usuario=aluno&senha=tentativa{i}",
                   agente="python-requests/2.32.3")
        print(f"  tentativa {i + 1}: {st}")
        time.sleep(0.2)


def paginas_escondidas(ip="192.0.2.66"):
    print("paginas-escondidas: pede caminhos que não existem (varredura)")
    for caminho in ("/.env", "/wp-admin/", "/phpmyadmin/", "/.git/config",
                    "/backup.zip", "/admin", "/config.php"):
        st = pedir("GET", caminho, ip, agente="Mozilla/5.0 zgrab/0.x")
        print(f"  {caminho}: {st}")
        time.sleep(0.2)


CENARIOS = {"normal": normal, "senha-errada": senha_errada,
            "paginas-escondidas": paginas_escondidas}


def main():
    escolhido = sys.argv[1] if len(sys.argv) > 1 else None
    if escolhido:
        CENARIOS[escolhido]()
    else:
        for funcao in CENARIOS.values():
            funcao()
    print("Pronto. Agora rode o vigia:  py lab/vigia.py")


if __name__ == "__main__":
    main()
