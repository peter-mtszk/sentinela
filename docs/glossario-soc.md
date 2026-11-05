# Glossário de SOC: as siglas que eu estudo

## 1. IP: Internet Protocol (Protocolo de Internet)
O **endereço** de cada aparelho na rede. É como o endereço de uma casa, pra carta chegar.
Ex.: `192.168.0.10`
> "O IP identifica um dispositivo na rede. Em segurança, serve pra rastrear de onde veio um acesso suspeito."

## 2. TCP: Transmission Control Protocol (Protocolo de Controle de Transmissão)
Envio **confiável**: confere se chegou tudo, na ordem certa. É como uma **carta registrada**.
Usado em sites, e-mail e downloads.

## 3. UDP: User Datagram Protocol (Protocolo de Datagrama do Usuário)
Envio **rápido**, sem conferir se chegou. É como **gritar pela janela**.
Usado em chamada de vídeo, jogos e lives.
> "O TCP garante a entrega. O UDP é mais rápido, mas não confirma."

## 4. DNS: Domain Name System (Sistema de Nomes de Domínio)
A **agenda de contatos** da internet: transforma `ifood.com.br` no IP do site.

## 5. HTTPS: HyperText Transfer Protocol Secure (Protocolo de Transferência de Hipertexto Seguro)
Site **com criptografia**, o cadeado 🔒. Usa a **porta 443**. (O HTTP, sem o S, usa a porta 80.)

## 6. SOC: Security Operations Center (Centro de Operações de Segurança)
A **sala de vigilância** que monitora alertas de segurança o dia todo.

## 7. SIEM: Security Information and Event Management (Gerenciamento de Informações e Eventos de Segurança)
O sistema que **junta os logs** de todos os computadores e **gera alertas**.
Exemplos: Splunk, Wazuh, Microsoft Sentinel.

## 8. CIA: Confidentiality, Integrity, Availability (Confidencialidade, Integridade, Disponibilidade)
Os **3 pilares** da segurança:
- **C**onfidencialidade: só quem pode, vê
- **I**ntegridade: ninguém altera sem permissão
- **A** (Disponibilidade): funciona quando precisa

## 9. DDoS: Distributed Denial of Service (Negação de Serviço Distribuída)
Milhares de máquinas atacando ao mesmo tempo pra **derrubar** um site.
⚠️ Não confundir com **força bruta**, que é tentar várias senhas no mesmo usuário.

## 10. MFA: Multi-Factor Authentication (Autenticação Multifator)
**Senha + outra prova**: um código no celular, um app autenticador ou a digital.
Também chamado de **2FA** (dois fatores).

---

## 🚨 Bônus: o alerta de "50 logins com falha"
É **força bruta** (não DDoS). O que fazer, como estagiário:
1. **Investigar:** de qual IP, de qual país, em que horário
2. **Conferir** se alguma tentativa deu certo (se deu, é mais grave)
3. **Escalar** pro time responsável (bloquear o IP/conta, trocar a senha)
4. **Documentar** tudo no chamado

**Logs de login:**
- Windows: Visualizador de Eventos → Segurança. Evento **4624** = sucesso; **4625** = falha
- Linux: `/var/log/auth.log`
