# Dados de exemplo

Todos os IPs são de faixas reservadas para documentação (RFC 5737). Nenhum dado é real.

| Arquivo | O que tem |
|---|---|
| `exemplo_acesso.log` | Tráfego normal de um site, com uma linha corrompida e um erro 500 |
| `ataques_acesso.log` | Cenários para os próximos detectores |

## Cenários em `ataques_acesso.log`

- **Usuário legítimo** (`198.51.100.23`): abre o login e entra na primeira tentativa.
- **Força bruta** (`203.0.113.99`): 6 `POST /login` com 401 em 11 segundos, por um script (`python-requests`), e depois um 302. O 302 depois das falhas é o pior caso: **a senha foi descoberta**.
- **Varredura** (`192.0.2.66`): 8 pedidos em 4 segundos atrás de arquivos sensíveis (`.env`, `.git/config`, `backup.zip`, `phpmyadmin`). Quase tudo 404: o atacante está procurando o que esquecemos exposto.
