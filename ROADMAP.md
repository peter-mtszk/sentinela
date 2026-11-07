# Roadmap

Um passo pequeno por dia, sempre com teste.

- [x] Ler uma linha de log no formato *combined*
- [x] Ler o arquivo inteiro, pulando linhas inválidas
- [x] Contar requisições por IP
- [ ] Listar os erros 4xx e 5xx por IP
- [x] Detectar força bruta: 5 ou mais `POST /login` com falha (401) do mesmo IP em 10 minutos
- [x] Detectar varredura: 5 ou mais 404 do mesmo IP em pouco tempo
- [x] Laboratório: servidor alvo, tráfego de ataque e vigia que alerta e bloqueia (`lab/`)
- [ ] Gerar um relatório em Markdown com os alertas
- [ ] Rodar pela linha de comando: `py -m sentinela dados/exemplo_acesso.log`
- [ ] Ler logs de login do Linux (`/var/log/auth.log`)
- [ ] Salvar os alertas em SQLite

## Diário

| Data | O que fiz |
|---|---|
| 28/10/2026 | Leitor de linhas e de arquivo, com 6 testes |
| 04/11/2026 | Publiquei o projeto, CI no GitHub Actions, cenários de força bruta e varredura, glossário de SOC |
| 05/11/2026 | Contador de requisições por IP, com 3 testes |
| 06/11/2026 | Detector de força bruta e varredura (4 testes) e laboratório em `lab/`: servidor alvo, tráfego de ataque e vigia que alerta e bloqueia os IPs |
