# Catálogo preliminar de skills

Anexo do [Relatório da Fase 0](../01_RESEARCH_BENCHMARK/FASE0_RELATORIO_DIAGNOSTICO.md), §9. Versão 0.1 (21/11/2026). A especificação final é entregável da Fase 6.

**Agentes:** A1 Radar · A2 Normativo HIS/HMP · A3 Analista · A4 Auditor · A5 Orquestrador e Assistente · SVC = serviço determinístico (sem IA).

**Regras comuns a todas as skills:**

- Saída sempre em esquema validado (JSON Schema). Saída inválida = erro, nunca "melhor esforço".
- Todo dado extraído carrega `evidencia` (URL ou arquivo, data e hora, hash, trecho) e `confianca` (alta, média, baixa).
- Falha de fonte (fora do ar, formato alterado) gera alerta de monitoramento e não apaga o dado anterior.
- Custo e duração de cada execução são registrados.

## Skills do briefing (1 a 20)

| # | Skill | Objetivo | Agentes | Entradas → Saídas | Ferramentas | Validações e erros |
|---|---|---|---|---|---|---|
| 1 | Pesquisa web avançada | Encontrar informação pública sobre empreendimentos e incorporadoras | A1, A3, A5 | Consulta → lista de URLs com resumo | Busca web | Domínios bloqueados/permitidos; nunca citar sem abrir a fonte |
| 2 | Pesquisa em sites de incorporadoras | Listar lançamentos de uma incorporadora | A1 | Domínio → páginas de empreendimentos | Fetch, robots.txt | Respeitar termos e robots.txt; sem login |
| 3 | Extração estruturada | Transformar página ou tabela em registro do esquema BECO | A1 | HTML/texto → registro + evidência | LLM com saída estruturada | Campo ausente = `null`, nunca inventado |
| 4 | Leitura de catálogos e PDFs | Extrair plantas, metragens, preços de PDFs | A1 | PDF → registros por tipologia | LLM com entrada de documento | Página e trecho de origem obrigatórios |
| 5 | Identificação de lançamentos | Decidir se um registro é novo, alteração ou duplicata | A1, SVC | Registro → {novo, alteração, duplicata} | Skill 11 | Ambíguo vai para A4 |
| 6 | Classificação HIS/HMP | Enquadrar empreendimento e unidade | SVC (motor de regras), A2 só em caso ambíguo | Registro + data → categoria + regra aplicada | Registro normativo | Sem evidência → "Classificação não confirmada" |
| 7 | Consulta e interpretação de legislação | Responder com base no registro normativo | A2, A5 | Pergunta → resposta com norma citada | Registro normativo, DOC | Nunca dar parecer jurídico; sinalizar validação profissional |
| 8 | Análise geográfica | Entorno, ZEIS, transporte, distâncias | SVC, A3 explica | Coordenada → atributos espaciais | PostGIS | Coordenada fora do município = erro |
| 9 | Cálculo de preço por m² | Valor ÷ área privativa | SVC | Preço, área → R$/m² | — | Área zero ou ausente = não calcular |
| 10 | Comparação de preços | Comparar com vizinhança, categoria e teto | SVC, A3 | Unidade → percentis e distância ao teto | PostGIS, ITBI | Amostra mínima para comparação |
| 11 | Deduplicação | Unificar registros do mesmo empreendimento | SVC, A4 revisa | Registros → entidade única | Chaves fortes (alvará, setor-quadra-lote, CNPJ, coordenadas) | Conflito de chaves vai para A4 |
| 12 | Verificação de fontes | Avaliar confiabilidade da fonte | A4 | URL/fonte → nível de confiança | Lista de fontes | Fonte desconhecida = confiança baixa |
| 13 | Detecção de alterações | Comparar versão atual com a anterior | SVC | Duas versões → diferenças | Histórico | Mudança só com evidência nova |
| 14 | Análise de tendências | Séries de lançamentos, preços e alvarás | A3 | Consulta → série + narrativa | SQL | Narrativa nunca contradiz os números |
| 15 | Geração de relatórios | Boletim diário e relatórios temáticos | A3 | Período + filtros → relatório | Modelos de relatório | Cada item com fonte e confiança |
| 16 | Geração de mapas | Mapas estáticos e camadas | SVC | Filtros → mapa | MapLibre, PMTiles | — |
| 17 | Gestão de CRM | Criar e atualizar oportunidades e atividades | SVC, A5 sugere | Ação → registro | Banco | Ação em nome do usuário exige confirmação |
| 18 | Envio de notificações | Entregar alertas e boletins | SVC | Evento + preferências → entrega | E-mail, aplicativo, WhatsApp (v1.1) | Respeitar consentimento e frequência |
| 19 | Auditoria de dados | Encontrar inconsistências na base | A4 | Base → lista de achados | SQL | Achados críticos bloqueiam publicação |
| 20 | Monitoramento de execução | Saúde de pipelines e agentes | SVC | Logs → alertas | Observabilidade | Falha repetida abre incidente |

## Skills adicionais identificadas na Fase 0 (21 a 30)

| # | Skill | Objetivo | Agentes | Entradas → Saídas | Ferramentas | Validações e erros |
|---|---|---|---|---|---|---|
| 21 | Geocodificação e normalização | Endereço → coordenada, CEP e setor-quadra-lote | SVC | Endereço → endereço normalizado + geometria | IPTU, lotes do GeoSampa | Baixa precisão marcada como tal |
| 22 | Monitor do Diário Oficial | Detectar publicações relevantes | SVC filtra, A2 analisa | Edição do dia → itens relevantes | DOC, palavras-chave | Todo item com link para a publicação |
| 23 | Consulta a camadas do GeoSampa | Baixar e atualizar camadas oficiais | SVC | Camada → tabela versionada | Download, PostGIS | Mudança de esquema = alerta |
| 24 | Cruzamento ITBI × teto | Aderência do preço praticado ao teto vigente na data | SVC, A3 | Empreendimento → indicador | ITBI, registro normativo | Só agregados; avaliação de LGPD antes de ativar |
| 25 | Resolução de entidades | Ligar marca, incorporadora, SPE e CNPJ | A1, SVC | Nome/CNPJ → grupo econômico | CNPJ aberto | Dados de sócios minimizados |
| 26 | Leitura de memorial e matrícula | Extrair enquadramento por unidade | A1 | Documento → unidades + categoria | LLM com documento | Documento pago só com autorização de custo |
| 27 | Enquadramento por data | Aplicar a regra vigente na data do evento | SVC | Data + valores → categoria | Registro normativo | Data fora de qualquer vigência = erro |
| 28 | Registro de evidências | Capturar e preservar a prova de cada dado | SVC | URL/arquivo → evidência imutável | Armazenamento, hash | Evidência ausente bloqueia "confirmado" |
| 29 | Controle de custo de IA | Orçamento por execução, por dia, por agente | A5, SVC | Execução → autorização ou bloqueio | Contadores de tokens | Estouro pausa a execução e avisa |
| 30 | Minimização de dados pessoais (LGPD) | Remover ou mascarar dados pessoais antes de armazenar | A4, SVC | Registro → registro minimizado | Regras de LGPD | Dado sensível sem base legal = descartar |

## Exemplo de uso — skill 6 (classificação HIS/HMP)

```yaml
entrada:
  unidade: { area_privativa_m2: 32.4, preco_anunciado: 279000.00 }
  empreendimento: { alvara: "a extrair da camada HIS_HMP", categoria_alvara: "HIS-1 e HIS-2" }
  data_referencia: "2026-11-21"
saida:
  categoria_unidade: "Classificação não confirmada"
  motivo: "Alvará indica HIS-1 e HIS-2, mas não identifica a unidade; preço anunciado acima do teto de HIS-1 (R$ 276.102,20) e abaixo do teto de HIS-2 (R$ 383.636,74)."
  hipotese: "HIS-2"
  regra_aplicada: "NORMA-010 / parâmetros 2026"
  alertas: ["Conferir tabela oficial da incorporadora ou matrícula"]
  confianca: media
```

O exemplo é ilustrativo e usa dados fictícios.
