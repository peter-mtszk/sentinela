# Sentinela

[![testes](https://github.com/peter-mtszk/sentinela/actions/workflows/testes.yml/badge.svg)](https://github.com/peter-mtszk/sentinela/actions/workflows/testes.yml)

Um mini-SOC em Python: lê logs de acesso de servidores web e aponta comportamentos suspeitos, como força bruta e varredura de páginas.

Estou construindo este projeto aos poucos, para aprender na prática o que um analista de SOC faz: ler logs, entender o que é normal e separar o que merece alerta.

## O que já funciona

- **Leitor de logs** (`sentinela/leitor.py`): lê linhas no formato *combined* (Apache e Nginx) e transforma cada uma num dicionário com IP, data com fuso, método, caminho, status, bytes, origem e navegador. Linhas corrompidas são ignoradas, sem derrubar o programa.
- **6 testes automatizados** (`tests/test_leitor.py`), incluindo os casos difíceis: `-` no lugar de valor, data com fuso horário e linha inválida.

## Como rodar

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install pytest
.venv\Scripts\python -m pytest
```

## Próximos passos

Veja o [ROADMAP.md](ROADMAP.md). Cada dia, um passo pequeno e testado.

## O que aprendi até aqui

- Um log é só texto: o primeiro trabalho é transformar texto em dados confiáveis.
- `split('"')` resolve o formato *combined* melhor do que cortar só nos espaços, porque o navegador e a origem têm espaços dentro.
- Testar primeiro os casos estranhos (linha vazia, `-`, fuso horário) evita que um log real quebre a análise.

Os IPs do arquivo de exemplo são de faixas reservadas para documentação (RFC 5737), não de pessoas reais.

Feito por **Peter Matuszak**, estudante de Engenharia de Software · [Portfólio](https://peter-mtszk.github.io)
