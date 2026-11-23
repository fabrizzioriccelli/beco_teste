# 03 — Identidade visual

**Faro v2.0 (23/11/2026).** O F de Faro desenhado como farol: a haste (o prédio, a torre) em Tinta e um facho de luz laranja que sai dela e se abre até achar o alvo. "Ter faro" é ter instinto para a oportunidade; o produto é isso toda manhã.

Manual completo, com a pesquisa do Behance, nome, símbolo, cores, tipografia, componentes, aplicações e usos incorretos: `manual/index.html` (publicado em https://claude.ai/artifact/4GWnbgo3bev3XKnsu2kc6v).

## Arquivos

| Pasta / arquivo | Conteúdo |
|---|---|
| `faro/assinatura.svg` | Assinatura principal, fundo claro |
| `faro/assinatura-negativa.svg` | Fundo Tinta ou foto escura |
| `faro/assinatura-mono.svg` | Uma cor: sobre Facho, carimbo, impressão |
| `faro/assinatura-com-descritor.svg` | Com "INTELIGÊNCIA IMOBILIÁRIA" |
| `faro/assinatura-vertical.svg` | Capas e telas quadradas |
| `faro/simbolo*.svg` | Símbolo sozinho (cor, negativo, mono) |
| `faro/icone-app.svg`, `faro/favicon.svg` | Ícone de app e aba do navegador |
| `faro/construcao.svg` | Folha de construção com a grade 48 × 48 |
| `faro/png/` | Ícone de app 512/192/180, favicon 32/48/64, símbolo 256, assinaturas a 96 px |
| `manual/` | Manual de marca (`gerar_manual.py` gera o `index.html` com os SVGs embutidos) |
| `arquivo/radar-his-v1/` | Identidade anterior ("Radar HIS", H de quadra), substituída em 23/11/2026 |

O texto do logo está em curvas e não depende de fonte instalada. Para regerar:

```
python3 03_BRAND_IDENTITY/gerar_identidade.py --fontes <pasta com fontsource schibsted-grotesk e jetbrains-mono> --saida 03_BRAND_IDENTITY/faro
python3 03_BRAND_IDENTITY/manual/gerar_manual.py
```

## Construção

- Grade 48 × 48. Haste 11 × 36. Facho separado da haste por 2 módulos, abre de 5 para 19. Braço 16 × 8.
- Área de proteção: 8 módulos (a altura do braço) em volta de qualquer assinatura.
- Tamanho mínimo: 16 px de altura para o favicon e 24 px para a assinatura horizontal.

Regras de cor, tipografia e componentes: [04_DESIGN_SYSTEM/README.md](../04_DESIGN_SYSTEM/README.md).

Pendente antes de registrar: busca no INPI (classes 9, 35, 36 e 42) e disponibilidade de domínio.
