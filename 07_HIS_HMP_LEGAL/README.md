# 07 — HIS/HMP: legislação e regras (Fase 4)

- [REGISTRO_NORMATIVO_HIS_HMP.yaml](REGISTRO_NORMATIVO_HIS_HMP.yaml) — registro versionado de normas e parâmetros (renda, preço, aluguel) por vigência.

Como funciona: cada norma tem fonte, publicação, vigência, abrangência, interpretação operacional, impacto na classificação e data da última verificação. Os parâmetros numéricos ficam em blocos por intervalo de vigência; uma transação é sempre avaliada pela regra vigente na sua data.

Aviso: inteligência de mercado, não parecer jurídico. Itens com `requer_validacao_juridica: true` precisam de revisão por advogado antes de uso em produção.
