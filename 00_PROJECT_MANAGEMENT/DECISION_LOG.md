# Histórico de decisões

Formato inspirado em ADR (Architecture Decision Record). Cada decisão tem estado: **Proposta** (aguarda aprovação), **Aceita**, **Rejeitada** ou **Substituída**.

Decisões estratégicas irreversíveis (nome, identidade, arquitetura de dados, integrações com custo) só passam a "Aceita" com aprovação explícita do responsável.

---

## DEC-0001 — Organização do repositório por fases

- **Data:** 21/11/2026
- **Estado:** Aceita (decisão operacional, dentro da autonomia prevista no briefing)
- **Contexto:** O briefing sugere uma estrutura de pastas de 00 a 15.
- **Decisão:** Adotar a estrutura sugerida na raiz do repositório, com um README por pasta indicando a fase e o estado.
- **Alternativas descartadas:** Uma pasta raiz `BECO/` dentro do repositório (descartada porque o próprio repositório já é o projeto).

## DEC-0002 — Fonte oficial como base da verdade

- **Data:** 21/11/2026
- **Estado:** Proposta
- **Contexto:** A pesquisa encontrou fontes oficiais abertas para HIS/HMP (camada de alvarás no GeoSampa, ITBI, IPTU).
- **Decisão proposta:** O Radar parte de fontes oficiais; sites de incorporadoras e anúncios complementam dados comerciais e nunca confirmam classificação sozinhos.
- **Alternativas descartadas:** Radar baseado em raspagem de portais (risco jurídico, termos de uso e baixa confiabilidade).
- **Consequências:** Depende de verificação da qualidade e da cadência de atualização da camada HIS/HMP (Fase 4).

## DEC-0003 — Cinco agentes de IA em vez de dez

- **Data:** 21/11/2026
- **Estado:** Proposta
- **Contexto:** A arquitetura inicial do briefing tem um orquestrador e dez agentes.
- **Decisão proposta:** Cinco agentes (Orquestrador e Assistente, Radar, Normativo HIS/HMP, Analista, Auditor) e serviços determinísticos para CRM, notificações, geoprocessamento e motor de regras. Data Quality e Compliance viram portões obrigatórios no fluxo.
- **Alternativas descartadas:** Dez agentes independentes (sobreposição de funções, custo e dificuldade de garantir portões).
- **Consequências:** Mantém todas as responsabilidades do briefing; reduz custo e pontos de falha.

## DEC-0004 — Classificação HIS/HMP por regra determinística versionada

- **Data:** 21/11/2026
- **Estado:** Proposta
- **Contexto:** Limites de renda e preço são numéricos, legais e mudam todo ano.
- **Decisão proposta:** Enquadramento feito por motor de regras com vigência por data. A IA só atua em casos ambíguos e na leitura de normas novas, sempre com aprovação humana.
- **Alternativas descartadas:** Classificação feita diretamente por modelo de IA (não auditável; risco de erro em valor legal).

## DEC-0005 — Estado "Classificação não confirmada" como padrão sem evidência

- **Data:** 21/11/2026
- **Estado:** Proposta (atende diretamente ao briefing, seção 8.2)
- **Decisão proposta:** Sem evidência mínima (alvará para empreendimento; matrícula ou tabela oficial conciliada para unidade), o estado é "Classificação não confirmada", visível na interface.
