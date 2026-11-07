# Laboratório: fingir um ataque e barrar com o Sentinela

Um laboratório é um ambiente fechado, no seu próprio computador, para testar
ataque e defesa sem mexer em nada de verdade. Tudo aqui fala só com `127.0.0.1`
(o seu PC), nunca com a internet.

## As peças

| Arquivo | Papel | Analogia |
|---|---|---|
| `servidor.py` | O site alvo, com página de login. Grava cada acesso em `logs/acesso.log` e nega quem está na lista de bloqueio. | O prédio que você quer proteger |
| `trafego.py` | Gera os visitantes: um normal, um tentando adivinhar a senha, um procurando páginas escondidas. | Os visitantes (um deles mal-intencionado) |
| `vigia.py` | Lê o log pelo Sentinela, mostra os alertas e escreve os IPs culpados em `bloqueados.txt`. | O segurança que olha as câmeras e tranca a porta |

O "cérebro" fica no pacote `sentinela/` (o `detector.py` é quem decide o que é ataque).
O laboratório só dá a ele um alvo real para observar.

## Roteiro (3 terminais, ou um de cada vez)

1. **Suba o alvo** e deixe rodando:
   ```powershell
   py lab\servidor.py
   ```
2. **Dispare o tráfego** (em outro terminal):
   ```powershell
   py lab\trafego.py
   ```
3. **Chame o vigia**: ele aponta os ataques e bloqueia os IPs:
   ```powershell
   py lab\vigia.py
   ```
4. **Prove que barrou**: ataque de novo. O mesmo IP agora leva `403`:
   ```powershell
   py lab\trafego.py senha-errada
   ```

Para recomeçar do zero, apague `lab\logs\acesso.log` e `lab\bloqueados.txt`.

## O que o detector considera ataque

- **Força bruta:** 5 ou mais `POST /login` com senha errada (401) do mesmo IP em 10 minutos.
- **Varredura:** 5 ou mais respostas 404 do mesmo IP em 5 minutos.

Os números ficam em `sentinela/detector.py` (dicionário `REGRAS`): mude ali para o
vigia ficar mais rígido ou mais tolerante.

## Detalhes honestos (para a entrevista)

- O `X-Lab-IP` deixa o `trafego.py` fingir IPs diferentes só para o log ter variedade.
  Num servidor real, **nunca** se confia num cabeçalho desses para identificar alguém —
  aqui é só cenário de estudo.
- O bloqueio é um arquivo de texto que o próprio servidor consulta. Na vida real, o
  Sentinela mandaria essa lista para um firewall (iptables, nftables, um grupo de
  segurança na nuvem). A ideia é a mesma: **detectar no log e cortar o acesso**.
- O laboratório não ataca ninguém: é o seu computador testando a sua própria defesa.
