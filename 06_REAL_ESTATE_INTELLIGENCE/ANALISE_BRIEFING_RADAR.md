# Tarefa 3 — Análise do briefing original do Radar Imobiliário

Anexo do [Relatório da Fase 0](../01_RESEARCH_BENCHMARK/FASE0_RELATORIO_DIAGNOSTICO.md). Data: 21/11/2026.

## 1. Situação: o anexo não foi encontrado

O briefing mestre (seção 11) pede que o Radar use "integralmente o briefing original de prospecção imobiliária fornecido como anexo deste projeto", com lista de incorporadoras, lista de bairros, critérios de preço, tipologias, fontes, dados comerciais, regras de deduplicação, monitoramento diário, estrutura do relatório, critérios de qualidade e notificações.

**Esse anexo não está no repositório nem na mensagem recebida.** A análise completa (inconsistências e itens desatualizados em cada lista) só pode ser feita depois do envio. Esta é a decisão pendente **D5**.

Enquanto isso, o que é possível adiantar:

## 2. Pontos do briefing que certamente precisarão de atualização

Com base no que o briefing mestre descreve sobre o conteúdo do anexo e na pesquisa da Fase 0:

| Item do briefing original | Por que precisa de revisão | Proposta |
|---|---|---|
| Critérios de preço | Os tetos de HIS/HMP mudam todo ano (INCC) e os limites de renda mudam com o salário mínimo. Em 2026: HIS-1 R$ 276.102,20; HIS-2 R$ 383.636,74; HMP R$ 537.672,71 [F01] | Substituir valores fixos por referência ao registro normativo versionado |
| Classificação HIS/HMP | O Decreto 64.244/2025 mudou a comprovação (certidão municipal, averbação na matrícula) [F05] | Evidência mínima por nível (empreendimento e unidade) e estado "não confirmado" |
| Tipologias (studios) | Mercado de compactos em que HIS, R2V e NR coexistem no mesmo prédio [F25][F29] | Classificação separada por unidade; studios de livre comercialização em segmento próprio |
| Fontes de pesquisa | Fontes oficiais abertas não citadas no briefing mestre: camada HIS/HMP do GeoSampa, ITBI, IPTU [F15][F47][F48] | Inverter a ordem: fonte oficial primeiro, site da incorporadora depois |
| Monitoramento diário às 8h | Fontes têm cadências diferentes (DOC diário em dias úteis; ITBI mensal; GeoSampa a confirmar; sites de incorporadoras irregulares) | Coleta em cadências por fonte; boletim às 8h todos os dias consolidando o que mudou |
| Regras de deduplicação | Chaves como nome do empreendimento ou endereço livre são frágeis | Chaves fortes: número do alvará, código setor-quadra-lote, CNPJ da SPE, endereço normalizado + coordenadas |
| Disponibilidade | O briefing exige não comunicar disponibilidade sem confirmação | Só CRM ou espelho de vendas autorizado confirma; caso contrário, "disponibilidade não confirmada" |
| Notificações | Custos de WhatsApp mudaram (cobrança por mensagem; utilitários cobrados com janela aberta a partir de 01/10/2026) [F50] | E-mail e aplicativo no MVP; WhatsApp na v1.1 |
| Lista de bairros | Precisa ser cruzada com onde os alvarás HIS realmente estão | Ranking de bairros por alvarás HIS/HMP licenciados (Fase 4) |
| Lista de incorporadoras | Incorporadoras operam por SPEs e podem ter sido notificadas ou multadas | Ficha por grupo econômico, com CNPJs das SPEs |

## 3. Inconsistências e riscos no próprio briefing mestre

| # | Ponto | Observação | Proposta |
|---|---|---|---|
| 1 | Radar de "oportunidades" HIS | Se o usuário for investidor sem renda compatível, o produto facilita uma compra irregular | Salvaguardas de elegibilidade e posicionamento correto (decisão D3) |
| 2 | 10 agentes com papéis sobrepostos | Radar e Monitor de incorporadoras se sobrepõem; CRM e Notificações não precisam de IA | 5 agentes + serviços determinísticos (relatório, §9) |
| 3 | Data Quality e Compliance como agentes paralelos | Não impedem, por si, a publicação de dado não verificado | Portões obrigatórios no fluxo |
| 4 | Gmail como canal | Limites de envio e verificação de OAuth para uso em produção | Provedor transacional para produção; Gmail só para piloto |
| 5 | "Fotos, quando licenciadas" | Fotos de incorporadoras em geral têm direitos reservados | Usar só com autorização expressa; padrão sem foto ou com mapa e planta |
| 6 | "Exportar informações autorizadas" | Falta definir o que é "autorizado" | Matriz de permissões por tipo de dado e de perfil (Fase 5) |
| 7 | Classificação por unidade | Exige matrícula ou tabela oficial; não há fonte aberta por unidade | Classificação por unidade como "não confirmada" por padrão, salvo evidência |
| 8 | Sequência rígida de fases | A pesquisa de dados (Fase 4) não depende da marca e está no caminho crítico | Permitir trilha paralela (decisão D6) |

## 4. Oportunidades de melhoria do Radar

1. **Radar em dois estágios:** "licenciado" (alvará HIS/HMP no GeoSampa) e "lançado" (comercialização identificada). O intervalo entre os dois é informação valiosa para incorporadoras e corretores.
2. **Boletim por relevância e por confiança**, como o briefing pede, com selo de procedência em cada item.
3. **Histórico de alterações** com o que mudou, quando, de que valor para que valor e qual fonte.
4. **Alerta de aderência ao teto:** preço anunciado acima do teto vigente da categoria é sinal de erro de classificação ou de irregularidade, a ser revisado antes de publicar.
