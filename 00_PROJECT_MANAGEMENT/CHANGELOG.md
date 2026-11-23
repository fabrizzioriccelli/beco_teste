# Histórico de versões

## [0.8.0] — 23/11/2026 — Site leve e Liquid Glass nítido

### Alterado

- Barra do topo deixa de ser fixa: rola com a página.
- Liquid Glass no estilo da Apple: vidro nítido, borda que pega luz e lente de refração nas bordas (Chrome/Edge).
- Desempenho: boletim e cidade carregam primeiro; base em tabela e vendas em pedaços pequenos (Empacotador); mapa em canvas sem a biblioteca d3; cidade desenhada uma vez, anéis em CSS; modo leve para aparelhos fracos.
- Medido antes → depois: 3,9 → 1,6 MB; JavaScript 4,15 → 0,03 s; 17.584 → 1.465 elementos; rolagem 13 → 59 quadros/s.

## [0.7.1] — 23/11/2026 — Refinamento de layout, textos e assistente

### Alterado

- Herói: texto sobre preto liso; a cidade acesa passa a ser uma faixa sangrada própria, sem luz atrás do texto; menos brilho no celular.
- Grade única de 920 px para barra, herói, listas e rodapé; 72 px entre seções; títulos das seções não ficam sob a barra.
- Textos mais curtos e diretos no site, na ficha e no boletim (e-mail e site).
- "Pergunte ao Faro" virou barra de vidro fixa no pé da tela com painel de conversa; nova ação para levar às seções do app.

## [0.7.0] — 23/11/2026 — Faro v5 (proposta aprovada)

### Alterado

- Identidade: só o nome, FARO em Geist Light com espaçamento largo, preto e branco. Sem símbolo e sem cor de destaque.
- Imagem da marca: a cidade acesa (`ilustrador.py`), São Paulo à noite com os 5.250 prédios HIS/HMP como pontos de luz.
- Design system v5: fonte do sistema (SF Pro) com Geist de reserva, escala e cores de sistema da Apple, Liquid Glass só na navegação.
- Site: barra de vidro flutuante, herói com a cidade acendendo na ordem dos alvarás, números em vidro, listas agrupadas, ficha de vidro.
- E-mail: topo preto com FARO e a imagem da cidade do dia (servida pelo repositório), números em painéis, listas brancas, botão cápsula.
- Boletim automático pausado: nada é enviado ao Diogo até a aprovação do conjunto.

### Arquivado

- v3 (Bodoni, verde e latão) e v4 recusada (logotipo com o "o" aceso) em `03_BRAND_IDENTITY/arquivo/`.

## [0.6.0] — 23/11/2026 — Faro v3: direção alto padrão

### Alterado

- Identidade refeita a pedido ("mais sofisticado, algo alta renda"): monograma F em Bodoni com facho de latão, logotipo FARO em versais espaçadas, paleta verde Jardim (#17302A), latão (#B08D57) e travertino (#EFEAE1).
- Tipografia: Bodoni Moda (nome, títulos e números) e Jost (texto e rótulos), no lugar de Schibsted Grotesk e JetBrains Mono.
- Design system v3.0, site e e-mail redesenhados: fios de latão, numerais romanos nas seções, losango como marcador, botões em versais.
- Endereços da Prefeitura passam a aparecer em grafia de título no e-mail e no site.
- Manual de marca v3 com a direção, as referências de alto padrão do Behance (Brickell, Forte, Orchard Hill, SOLA) e o antes × agora.

### Arquivado

- Versão 2 (grotesca e laranja) em `03_BRAND_IDENTITY/arquivo/faro-v2/`.

## [0.5.0] — 23/11/2026 — Rebrand: Faro

### Alterado

- Nome do produto: **Faro** (proposto; substitui "BECO" e "Radar HIS"). Pendente: busca no INPI e domínio.
- Identidade nova: o F como farol, com haste Tinta (#0F1E46) e facho laranja (#FF5A1F). Arquivos em `03_BRAND_IDENTITY/faro/` (SVG e PNG).
- Design system v2.0: paleta Tinta e Facho, Schibsted Grotesk e JetBrains Mono, banda de marca com borda Facho, números do dia em laranja.
- Site e boletim por e-mail redesenhados com a marca nova; assunto do e-mail passa a ser "Faro · DD/MM · ...".

### Adicionado

- Manual de marca (`03_BRAND_IDENTITY/manual/`), com a análise dos projetos do Behance, o raciocínio do nome, construção do símbolo, cores, tipografia, componentes, aplicações e usos incorretos.

### Arquivado

- Identidade "Radar HIS" (H de quadra) em `03_BRAND_IDENTITY/arquivo/radar-his-v1/`.

## [0.4.0] — 23/11/2026 — Boletim editorial e benchmark visual

### Adicionado

- Benchmark visual de 24 projetos "real estate" do Behance (`01_RESEARCH_BENCHMARK/BENCHMARK_VISUAL_BEHANCE.md`).
- Design system v1.1: banda de marca, rótulo editorial, herói numérico, seção numerada e item do boletim.
- Boletim "O que rolou ontem" com conteúdo único para e-mail e site (seção `#boletim`), mais histórico dos boletins anteriores.

## [0.3.0] — 23/11/2026 — Identidade, design system e boletim diário

### Adicionado

- Identidade visual "H de quadra" (`03_BRAND_IDENTITY/`) e design system com tokens (`04_DESIGN_SYSTEM/`).
- Rotina diária com agentes (Coletor, Analista, Auditor, Redator, Distribuidor) e roteiro do orquestrador.
- Tarefa agendada todo dia às 7h38 (São Paulo): atualiza o site e envia o boletim "O que mapeamos ontem" por e-mail.

## [0.2.0] — 22/11/2026 — Radar HIS (primeira versão com dados reais)

### Adicionado

- `11_APPLICATION/radar_his/`: coleta e processamento de dados oficiais (GeoSampa, ITBI 2006–set/2026, IPCA e CDI) e o site do relatório.
- Relatório publicado com mapa, lista filtrável, vendas e revendas por prédio, "antes × agora" por unidade e calculadora de investimento.
- Tetos de preço de HIS/HMP conferidos no texto oficial dos Decretos 64.244/2025 e 64.895/2026.

## [0.1.0] — 21/11/2026 — Fase 0 (rascunho para validação)

### Adicionado

- Estrutura de pastas do projeto (00 a 15), com README por pasta.
- Relatório da Fase 0: pesquisa, benchmarking e diagnóstico estratégico (`01_RESEARCH_BENCHMARK/FASE0_RELATORIO_DIAGNOSTICO.md`).
- Fichas de benchmarking de concorrentes nacionais e internacionais.
- Registro de fontes consultadas, com links e data de consulta.
- Registro normativo HIS/HMP em YAML, com parâmetros de 2025 e 2026 (`07_HIS_HMP_LEGAL/REGISTRO_NORMATIVO_HIS_HMP.yaml`).
- Mapa preliminar de fontes de dados.
- Análise do briefing do Radar (o anexo original não foi encontrado).
- Catálogo preliminar de 30 skills.
- Três territórios de posicionamento e análise preliminar do nome BECO.
- Histórico de decisões (DEC-0001 a DEC-0005) e lista de decisões pendentes (D1 a D11).
- Imagem de referência da arquitetura inicial do briefing (`09_AI_AGENTS/referencia_arquitetura_inicial_briefing.jpg`).

### Limitações conhecidas

- Pesquisa feita por busca indexada; textos integrais das normas não lidos (bloqueio de rede do ambiente).
- Disponibilidade do nome e do domínio BECO não verificada.
