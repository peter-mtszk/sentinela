"""Vigia do laboratório: lê o log do servidor, mostra os alertas e bloqueia os IPs.

É aqui que o Sentinela fecha o ciclo: pega o que o detector encontrou, escreve na
tela em português e acrescenta cada IP culpado em lab/bloqueados.txt. Da próxima vez
que aquele IP bater no servidor, ele leva 403.

Uso:  py lab/vigia.py            (lê o log e bloqueia)
      py lab/vigia.py --so-ver   (só mostra, não bloqueia)
"""

import os
import sys

# deixa importar o pacote sentinela mesmo rodando de dentro de lab/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentinela.detector import detectar          # noqa: E402
from sentinela.leitor import ler_arquivo          # noqa: E402

PASTA = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(PASTA, "logs", "acesso.log")
BLOQUEADOS = os.path.join(PASTA, "bloqueados.txt")

NOME = {"forca_bruta": "força bruta no login", "varredura": "varredura de páginas"}


def ja_bloqueados():
    if not os.path.exists(BLOQUEADOS):
        return set()
    with open(BLOQUEADOS, encoding="utf-8") as f:
        return {linha.split()[0] for linha in f if linha.strip() and not linha.startswith("#")}


def bloquear(ip, motivo):
    novo = not os.path.exists(BLOQUEADOS)
    with open(BLOQUEADOS, "a", encoding="utf-8") as f:
        if novo:
            f.write("# IPs bloqueados pelo Sentinela (ip  motivo)\n")
        f.write(f"{ip}  {motivo}\n")


def main():
    so_ver = "--so-ver" in sys.argv
    if not os.path.exists(LOG):
        print(f"Ainda não há log em {LOG}. Suba o servidor e gere tráfego primeiro.")
        return

    alertas = detectar(ler_arquivo(LOG))
    if not alertas:
        print("Nenhum ataque no log. Tudo tranquilo.")
        return

    print(f"{len(alertas)} alerta(s):\n")
    bloqueados = ja_bloqueados()
    for a in alertas:
        print(f"  [!] {a['ip']} — {NOME[a['tipo']]} ({a['quantidade']} pedidos)")
        if so_ver:
            continue
        if a["ip"] in bloqueados:
            print("      já estava bloqueado")
        else:
            bloquear(a["ip"], NOME[a["tipo"]])
            bloqueados.add(a["ip"])
            print("      -> bloqueado agora")

    if not so_ver:
        print(f"\nLista de bloqueio: {BLOQUEADOS}")


if __name__ == "__main__":
    main()
