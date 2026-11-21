# Mapa preliminar de fontes de dados

Anexo do [Relatório da Fase 0](../01_RESEARCH_BENCHMARK/FASE0_RELATORIO_DIAGNOSTICO.md). Avaliação preliminar em 21/11/2026, a ser testada na Fase 4 com download real de cada fonte.

**Princípios:**

1. **Fonte oficial primeiro.** Anúncio não é comprovação documental.
2. **Respeitar termos de uso, licenças e robots.txt.** Nada de contornar autenticação, captcha ou bloqueio.
3. **Toda captura gera evidência:** URL, data e hora, hash do conteúdo e trecho usado.

Escala de avaliação: Alta / Média / Baixa. "?" = não verificado.

## Fontes oficiais (base da verdade)

| Fonte | Conteúdo | Disponibilidade | Qualidade | Atualização | Custo | Licença | Confiabilidade | Uso no BECO | Fonte |
|---|---|---|---|---|---|---|---|---|---|
| GeoSampa — camada HIS/HMP (Alvará de Execução) | Alvarás de HIS-1, HIS-2 e HMP aprovados pela SMUL desde ago/2019 | Download aberto (`HIS_HMP_Habitacao_Popular`) | ? (testar) | ? | Gratuito | Aberta (Decreto 56.701/2015) | Alta | **Núcleo do radar e da classificação de empreendimentos** | [F15] |
| GeoSampa — zoneamento (SISZON) | Zoneamento de cerca de 3,5 milhões de lotes, incluindo ZEIS | Download e consulta | Alta | Conforme a legislação | Gratuito | Aberta | Alta | Enquadramento EZEIS; mapa | [F49] |
| GeoSampa — lotes fiscais | Cerca de 2,5 milhões de lotes vetorizados integrados ao cadastro fiscal | Download | Alta | ? | Gratuito | Aberta | Alta | Geometria e chave setor-quadra-lote | [F49] |
| Cadastro do IPTU | Mais de 3 milhões de registros (cerca de 120 MB) | Download no GeoSampa | Alta | Anual (a confirmar) | Gratuito | Aberta | Alta | Características dos imóveis; deduplicação | [F47] |
| ITBI (Secretaria da Fazenda) | Transações com recolhimento de ITBI desde 2019 | Download | Alta | Mensal (Lei 18.161/2024) | Gratuito | Aberta | Alta | Preço praticado; aderência ao teto | [F48] |
| SEHAB — lista de empreendimentos com HIS disponíveis | Empreendimentos com unidades à venda | Página pública | ? | ? | Gratuito | ? | Alta | Cruzamento com o radar | [F16] |
| Diário Oficial da Cidade | Leis, decretos, portarias, despachos | Público | Alta | Diária (dias úteis) | Gratuito | Pública | Alta | Monitor normativo | — |
| Câmara Municipal | Projetos de lei, CPIs, textos legais | Público | Alta | Contínua | Gratuito | Pública | Alta | Monitor normativo | [F17] |
| Plataforma SMUL/SEHAB (Portaria 01/2026) | Dados integrados de licenciamento e fiscalização | **Interna** por ora | ? | ? | ? | ? | Alta | Acompanhar eventual publicação | [F14][F22] |
| Registro de Imóveis (matrículas) | Averbação de enquadramento por unidade | Certidão paga, por unidade | Alta | Por evento | **Pago** | Restrita | Muito alta | Classificação por unidade (amostral) | [H] |
| Receita Federal — dados abertos de CNPJ | Empresas, SPEs, atividade, quadro de sócios | Download | Alta | Mensal (a confirmar) | Gratuito | Aberta | Alta | Resolução de entidades (sócios = dado pessoal: minimizar) | [H] |
| Transporte (SPTrans, Metrô, CPTM — GTFS e estações) | Linhas, paradas, estações | Download (a confirmar) | ? | ? | Gratuito | ? | Alta | Proximidade de transporte | [H] |
| IBGE — Censo 2022 e malhas | Setores censitários, renda, população | Download | Alta | Decenal | Gratuito | Aberta | Alta | Perfil territorial | [H] |

## Fontes de mercado

| Fonte | Conteúdo | Disponibilidade | Termos de uso | Confiabilidade | Uso no BECO | Fonte |
|---|---|---|---|---|---|---|
| Sites e tabelas de incorporadoras | Lançamentos, tipologias, preços, condições | Público | **Verificar por site** | Média (anúncio) | Dados comerciais, com estado "não confirmado" até conciliação | [H] |
| Catálogos e PDFs comerciais | Plantas, metragens, preços | Público ou mediante cadastro | Verificar | Média | Extração com evidência | [H] |
| Órulo / DWV (marketplaces B2B) | Estoque e condições de imóveis novos | Mediante conta ou parceria | Contrato | Média-alta | **Parceria preferível à coleta** | [F37][F39] |
| CRMs de incorporadoras (CV CRM, Anapro, Sienge) | Espelho de vendas, disponibilidade | Integração autorizada | Contrato | Alta | Única via para "disponibilidade confirmada" | [F41] |
| Portais (ZAP, VivaReal, QuintoAndar, Apto) | Anúncios | Público | **Em geral restringem coleta automatizada** | Baixa a média | Não usar como fonte primária; no máximo como sinal, se os termos permitirem | [H] |
| FipeZAP | Índice de preço de anúncios | Público | Verificar | Média (preço pedido) | Indicador de contexto | [F34] |
| Secovi-SP (pesquisa mensal) | Lançamentos e vendas na capital | Público (relatórios) | Verificar reutilização | Alta | Indicadores de mercado | [F27] |
| ABRAINC / Brain / CBIC | Indicadores nacionais | Público (relatórios) | Verificar | Alta | Contexto | [F36] |
| Notícias especializadas | Lançamentos, movimentos de incorporadoras | Público | Citar com link | Média | Sinal para o radar; nunca prova | [H] |

## Lacunas a resolver na Fase 4

1. Baixar e perfilar a camada `HIS_HMP_Habitacao_Popular`: campos, chaves, cobertura, frequência de atualização.
2. Confirmar os campos da base do ITBI e fazer avaliação de LGPD antes de qualquer cruzamento.
3. Testar o custo e o prazo de uma amostra de certidões de matrícula.
4. Levantar termos de uso das 20 principais incorporadoras de HIS da lista do briefing original (quando recebido).
5. Abrir conversas de parceria com pelo menos um marketplace B2B (Órulo ou DWV) e um CRM.
