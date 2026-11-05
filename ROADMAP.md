# Roadmap

Um passo pequeno por dia, sempre com teste.

- [x] Ler uma linha de log no formato *combined*
- [x] Ler o arquivo inteiro, pulando linhas inválidas
- [ ] Contar requisições por IP
- [ ] Listar os erros 4xx e 5xx por IP
- [ ] Detectar força bruta: 5 ou mais `POST /login` com falha (401) do mesmo IP em 10 minutos
- [ ] Detectar varredura: muitos 404 do mesmo IP em pouco tempo
- [ ] Gerar um relatório em Markdown com os alertas
- [ ] Rodar pela linha de comando: `py -m sentinela dados/exemplo_acesso.log`
- [ ] Ler logs de login do Linux (`/var/log/auth.log`)
- [ ] Salvar os alertas em SQLite

## Diário

| Data | O que fiz |
|---|---|
| 28/10/2026 | Leitor de linhas e de arquivo, com 6 testes |
| 04/11/2026 | Publiquei o projeto, CI no GitHub Actions, cenários de força bruta e varredura, glossário de SOC |
