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

## DEC-0006 — Nome e identidade: Faro

- **Data:** 23/11/2026
- **Estado:** Proposta (decisão irreversível: depende de aprovação e da busca no INPI)
- **Contexto:** "BECO" soa negativo (sombrio, perigoso) e "Radar HIS" foi considerado genérico e fraco. A identidade anterior (H de quadra, azul e amarelo) não tinha personalidade.
- **Decisão proposta:** Nome **Faro** ("ter faro para negócio" e farol). Símbolo: o F como farol, haste Tinta e facho laranja. Paleta Tinta #0F1E46 e Facho #FF5A1F; tipografia Schibsted Grotesk e JetBrains Mono. Base: análise de 24 projetos "real estate" do Behance (Astrix, Alliance, Lumen e Bilge como referências principais).
- **Alternativas descartadas:** Lastro (proptech existente), Prumo (associado à Prumo Logística), Radar (genérico), BECO (conotação negativa); visual preto e dourado de luxo (padrão dominante do Behance e errado para habitação social).
- **Consequências:** Site, e-mail e design system já usam Faro. Antes de registrar: busca no INPI (classes 9, 35, 36 e 42) e domínio. A pasta de código continua `11_APPLICATION/radar_his/` para não quebrar a rotina agendada.

## DEC-0007 — Identidade Faro v3: alto padrão

- **Data:** 23/11/2026
- **Estado:** Proposta (aguarda aprovação)
- **Contexto:** A versão 2 (grotesca pesada, laranja) foi considerada pouco sofisticada. Pedido: "mais sofisticado, algo alta renda". O Faro serve a quem investe.
- **Decisão proposta:** Conceito "endereço nobre": monograma F em Bodoni Moda com facho de latão; logotipo em versais espaçadas; paleta dos materiais dos prédios de alto padrão de São Paulo (verde Jardim, latão, travertino); Jost para texto. Referências: Brickell, Forte, Orchard Hill e SOLA (Behance).
- **Alternativas descartadas:** Preto com dourado brilhante (clichê do luxo); marrom e cobre (muito próximo da Brickell); Cormorant e Marcellus (números de estilo antigo, ruins para dados); moldura em placa e raios finos para o monograma (testados em prancha).
- **Consequências:** Site, e-mail, tokens e manual já usam a v3. O nome Faro continua (DEC-0006).

## DEC-0008 — Identidade Faro v5: só o nome, preto e branco

- **Data:** 23/11/2026
- **Estado:** Aprovada ("show! é isso!")
- **Contexto:** As versões com símbolo (círculo com F, facho, torre) e a v3 com Bodoni e latão foram consideradas pouco modernas ou clichê de luxo. Pedido: moderno, minimalista, alto padrão sem clichê, fonte SF e Liquid Glass.
- **Decisão:** Logotipo FARO em Geist Light, maiúsculas espaçadas, preto e branco; a cidade acesa como imagem da marca; interface no estilo Apple com SF Pro (fonte do sistema) e Liquid Glass na camada de navegação.
- **Alternativas descartadas:** Símbolos das direções Torre, Facho e Lente e a fusão das três; "o" aceso (v4); Bodoni com verde e latão (v3).
- **Consequências:** Site, e-mail, tokens e manual já usam a v5. Faltam fotos de arquitetura licenciadas para as aplicações. Supersede a DEC-0007.

