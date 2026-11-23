# Decisões pendentes do responsável (Diogo)

Gerado ao fim da Fase 0, em 21/11/2026. Responda diretamente neste arquivo (coluna "Resposta") ou na conversa. Nenhuma fase seguinte começa antes de D1 a D5.

| # | Decisão | Opções | Recomendação | Bloqueia | Resposta |
|---|---|---|---|---|---|
| D1 | Validar o diagnóstico da Fase 0 | Aprovar / aprovar com ajustes / refazer partes | — | Todas as fases | |
| D2 | Cliente primário do MVP | (a) imobiliárias e corretores de lançamentos HIS/HMP; (b) incorporadoras; (c) bancos e correspondentes; (d) portais (API); (e) outro | (a) como entrada e (b) como cliente de maior valor | Fases 1 e 3 | |
| D3 | Postura sobre investidores em HIS | (a) não promover HIS como investimento e atender investidores no segmento de livre comercialização; (b) outra | (a) | Fases 1, 3 e 7 | |
| D4 | Território de posicionamento | Procedência / Antecipação / Cidade legível / combinação | Procedência + Antecipação como funcionalidade de entrada | Fase 1 | |
| D5 | Enviar o briefing original do Radar (anexo) | — | — | Tarefa 3 completa; Fase 7 | |
| D6 | Fase 4 em paralelo às Fases 1 a 3 | Sim / não (sequência estrita) | Sim | Prazo do MVP | |
| D7 | Liberar acesso de rede no ambiente de trabalho | Liberar os domínios abaixo / manter bloqueado | Liberar | Verificação primária (Fase 4) | |
| D8 | Teto de orçamento mensal (infra e IA) da v1 e orçamento para validação jurídica | Valor a definir | Até US$ 600/mês na v1; jurídico a cotar | Fase 5 | |
| D9 | Busca formal de anterioridade do nome BECO | Autorizar / adiar | Autorizar antes de qualquer criação visual | Fase 2 | 22/11/2026: a equipe considera que "beco" soa negativo (sombrio, perigoso). Gerar nomes alternativos na Fase 1. 23/11/2026: proposto **Faro** (DEC-0006); falta busca no INPI e domínio. |
| D10 | WhatsApp na v1 ou na v1.1 | v1 / v1.1 | v1.1 | Fase 8 | |
| D11 | Perfil do responsável e da equipe | Quem fará as validações de mercado, jurídica e de usuários? | Indicar pelo menos um advogado urbanista e 5 a 8 usuários para entrevistas | Fases 3 e 4 | |

## Domínios a liberar (D7)

Para que a próxima fase leia os textos oficiais na íntegra, a política de rede do ambiente precisa permitir:

- `prefeitura.sp.gov.br` e `www.prefeitura.sp.gov.br`
- `gestaourbana.prefeitura.sp.gov.br`
- `geosampa.prefeitura.sp.gov.br` e `metadados.geosampa.prefeitura.sp.gov.br`
- `dados.prefeitura.sp.gov.br`
- `www.saopaulo.sp.leg.br`
- `busca.inpi.gov.br`
- `rdap.registro.br`
- `www.planalto.gov.br`
- `secovi.com.br`

A liberação é feita nas configurações do ambiente de nuvem do Claude Code (política de rede). Em ambiente local, não é necessária.
