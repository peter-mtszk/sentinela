"""Servidor alvo do laboratório: um site falso com página de login.

Roda só no seu computador (127.0.0.1) e grava cada acesso em lab/logs/acesso.log,
no mesmo formato "combined" do Apache e do Nginx, que o Sentinela já sabe ler.

Antes de responder, ele confere lab/bloqueados.txt: IP que estiver lá recebe 403.
É o papel do firewall no laboratório.

Uso:  py lab/servidor.py
"""

import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

PASTA = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(PASTA, "logs", "acesso.log")
BLOQUEADOS = os.path.join(PASTA, "bloqueados.txt")
PORTA = 8080

# Usuário de teste, que só existe neste laboratório
USUARIO, SENHA = "aluno", "lab-2026"

PAGINA_LOGIN = b"""<!doctype html><meta charset="utf-8"><title>Login</title>
<h1>Painel da Loja (laboratorio)</h1>
<form method="post" action="/login">
<input name="usuario" placeholder="usuario"> <input name="senha" type="password" placeholder="senha">
<button>Entrar</button></form>"""


def ips_bloqueados():
    if not os.path.exists(BLOQUEADOS):
        return set()
    with open(BLOQUEADOS, encoding="utf-8") as f:
        return {linha.split()[0] for linha in f if linha.strip() and not linha.startswith("#")}


class Alvo(BaseHTTPRequestHandler):
    def ip_do_visitante(self):
        # Todo mundo no laboratório vem de 127.0.0.1. Para fingir atacantes diferentes,
        # o script atacante manda o IP falso no cabeçalho X-Lab-IP.
        # Isso só vale aqui: num servidor real, confiar num cabeçalho assim seria uma falha.
        return self.headers.get("X-Lab-IP") or self.client_address[0]

    def responder(self, status, corpo=b"", extra=None):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        for chave, valor in (extra or {}).items():
            self.send_header(chave, valor)
        self.end_headers()
        self.wfile.write(corpo)
        self.gravar_log(status, len(corpo))

    def gravar_log(self, status, tamanho):
        quando = datetime.now().astimezone().strftime("%d/%b/%Y:%H:%M:%S %z")
        origem = self.headers.get("Referer") or "-"
        agente = self.headers.get("User-Agent") or "-"
        linha = (f'{self.ip_do_visitante()} - - [{quando}] "{self.command} {self.path} {self.request_version}" '
                 f'{status} {tamanho} "{origem}" "{agente}"\n')
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(linha)

    def bloqueado(self):
        if self.ip_do_visitante() in ips_bloqueados():
            self.responder(403, b"Bloqueado pelo Sentinela")
            return True
        return False

    def do_GET(self):
        if self.bloqueado():
            return
        if self.path in ("/", "/login"):
            self.responder(200, PAGINA_LOGIN)
        elif self.path == "/painel":
            self.responder(200, "<h1>Painel (área restrita)</h1>".encode())
        else:
            self.responder(404, b"Nao encontrado")

    def do_POST(self):
        if self.bloqueado():
            return
        if self.path != "/login":
            self.responder(404, b"Nao encontrado")
            return
        tamanho = int(self.headers.get("Content-Length") or 0)
        dados = parse_qs(self.rfile.read(tamanho).decode("utf-8", "replace"))
        usuario = dados.get("usuario", [""])[0]
        senha = dados.get("senha", [""])[0]
        if usuario == USUARIO and senha == SENHA:
            self.responder(302, extra={"Location": "/painel"})
        else:
            self.responder(401, b"Usuario ou senha errados")

    def log_message(self, *args):
        pass  # o registro que importa vai para o arquivo; o terminal fica limpo


def main():
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    print(f"Alvo no ar: http://127.0.0.1:{PORTA}  (log em {LOG})")
    print("Ctrl+C para desligar.")
    try:
        ThreadingHTTPServer(("127.0.0.1", PORTA), Alvo).serve_forever()
    except KeyboardInterrupt:
        print("\nAlvo desligado.")


if __name__ == "__main__":
    main()
