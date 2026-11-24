# Faro — Inteligência imobiliária

<p align="center"><b>Português</b> · <a href="README.en.md">English</a></p>

> Nome proposto em 23/11/2026 (substitui "BECO" e "Radar HIS"). Falta a busca de anterioridade no INPI e a checagem de domínio antes do registro.

O Faro transforma informação imobiliária dispersa em inteligência organizada, rastreável e acessível. O primeiro foco é o mapeamento de **HIS** (Habitação de Interesse Social) e **HMP** (Habitação de Mercado Popular) no Município de São Paulo, com classificação separada para os demais segmentos, como studios de livre comercialização.

**Responsável:** Diogo

## Estado atual

| Fase | Nome | Estado |
|---|---|---|
| 0 | Pesquisa, benchmarking e diagnóstico | **Entregue para validação** (21/11/2026) |
| 1 | Estratégia de marca e branding | Aguardando aprovação da Fase 0 |
| 2 | Identidade visual completa | Não iniciada |
| 3 | Estratégia de produto e arquitetura de experiência | Não iniciada |
| 4 | Pesquisa imobiliária, HIS/HMP e inteligência territorial | Pesquisa preliminar feita na Fase 0; aprofundamento não iniciado |
| 5 | Arquitetura tecnológica e estrutura de dados | Não iniciada |
| 6 | Ecossistema de agentes e skills de IA | Proposta preliminar na Fase 0 |
| 7 | Desenvolvimento da plataforma e interfaces | Não iniciada |
| 8 | Integrações, automações e notificações | Não iniciada |
| 9 | Testes, segurança, validação e documentação | Não iniciada |
| 10 | Implantação, monitoramento e evolução contínua | Não iniciada |

## Comece por aqui

- **Site do Faro (boletim diário, mapa, fichas e contatos):** https://claude.ai/artifact/56WB6o988QdYjeTVMtX5j9
- **Manual da marca:** https://claude.ai/artifact/4GWnbgo3bev3XKnsu2kc6v ([03_BRAND_IDENTITY](03_BRAND_IDENTITY/))
- **Boletim por e-mail:** todo dia às 7h38 (São Paulo), gerado pela [rotina diária](11_APPLICATION/radar_his/ROTINA_DIARIA.md)

1. [Relatório da Fase 0](01_RESEARCH_BENCHMARK/FASE0_RELATORIO_DIAGNOSTICO.md) — documento principal da primeira entrega.
2. [Decisões pendentes](00_PROJECT_MANAGEMENT/DECISOES_PENDENTES.md) — o que precisa da sua resposta para seguir.
3. [Histórico de decisões](00_PROJECT_MANAGEMENT/DECISION_LOG.md) e [histórico de versões](00_PROJECT_MANAGEMENT/CHANGELOG.md).

## Estrutura

| Pasta | Conteúdo |
|---|---|
| [00_PROJECT_MANAGEMENT](00_PROJECT_MANAGEMENT/) | Decisões, versões, pendências |
| [01_RESEARCH_BENCHMARK](01_RESEARCH_BENCHMARK/) | Relatório da Fase 0, fichas de concorrentes, registro de fontes |
| [02_BRAND_STRATEGY](02_BRAND_STRATEGY/) | Territórios de posicionamento, análise do nome |
| [03_BRAND_IDENTITY](03_BRAND_IDENTITY/) | Marca Faro: logo, ícones, manual de marca |
| [04_DESIGN_SYSTEM](04_DESIGN_SYSTEM/) | Tokens, cores, tipografia e componentes do site e do e-mail |
| [05_PRODUCT_UX_UI](05_PRODUCT_UX_UI/) | Produto, jornadas, protótipos (Fase 3) |
| [06_REAL_ESTATE_INTELLIGENCE](06_REAL_ESTATE_INTELLIGENCE/) | Fontes de dados, análise do briefing do Radar |
| [07_HIS_HMP_LEGAL](07_HIS_HMP_LEGAL/) | Registro normativo HIS/HMP versionado |
| [08_DATA_ARCHITECTURE](08_DATA_ARCHITECTURE/) | Arquitetura de dados (Fase 5) |
| [09_AI_AGENTS](09_AI_AGENTS/) | Agentes de IA (Fase 6); referência da arquitetura inicial |
| [10_SKILLS](10_SKILLS/) | Catálogo de skills |
| [11_APPLICATION](11_APPLICATION/) | Código: coleta, análise, auditoria, boletim e site (`radar_his/`) |
| [12_INTEGRATIONS](12_INTEGRATIONS/) | Integrações e notificações (Fase 8) |
| [13_TESTING](13_TESTING/) | Testes e qualidade (Fase 9) |
| [14_DOCUMENTATION](14_DOCUMENTATION/) | Documentação técnica e de usuário |
| [15_DEPLOYMENT](15_DEPLOYMENT/) | Implantação e operação (Fase 10) |

## Regras de trabalho

- Nenhuma fase é pulada; cada uma termina com entregáveis, decisões, alternativas descartadas, pontos de validação e próximos passos.
- Decisões irreversíveis (nome, identidade, arquitetura de dados, integrações com custo) dependem de aprovação do responsável.
- Nenhum dado é inventado. Fatos têm fonte; hipóteses são marcadas como hipóteses.
- Dados de demonstração, quando usados, são identificados como fictícios e nunca se misturam a dados verificados.
