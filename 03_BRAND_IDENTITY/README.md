# 03 — Identidade visual

**Faro v5 (23/11/2026), proposta aprovada.** Só o nome: FARO em Geist Light, maiúsculas com espaçamento largo, preto e branco. Sem símbolo e sem cor de destaque. A imagem da marca é a cidade acesa: São Paulo à noite, cada luz é um dos 5.250 prédios HIS/HMP com alvará, desenhada com os dados oficiais (`11_APPLICATION/radar_his/ilustrador.py`).

Manual: `manual/index.html` (gerado por `manual/gerar_manual.py`), publicado em https://claude.ai/artifact/4GWnbgo3bev3XKnsu2kc6v.

## Arquivos

| Arquivo | Uso |
|---|---|
| `faro/logotipo.svg`, `faro/logotipo-negativo.svg` | FARO sozinho, preto ou branco |
| `faro/assinatura.svg`, `faro/assinatura-negativa.svg` | FARO com "INTELIGÊNCIA IMOBILIÁRIA" |
| `faro/icone-app.svg`, `faro/favicon.svg` | O F em Geist num quadrado preto |
| `faro/construcao.svg` | Espaçamento (0,42 eme) e área de proteção (um terço da versal) |
| `faro/png/` | Ícone 1024/512/180, favicon 32/64, logotipo e assinaturas |
| `arquivo/` | Versões anteriores: Radar HIS (v1), Faro v2 (grotesca e laranja), v3 (Bodoni, verde e latão), v4 recusada ("o" aceso) |

Para regerar: `python3 03_BRAND_IDENTITY/gerar_identidade.py --fontes <pasta com @fontsource/geist-sans> --saida 03_BRAND_IDENTITY/faro`.

## Como a proposta foi escolhida

1. Pesquisa dos casos de identidade imobiliária mais bem avaliados do Behance (Manor, Zenith Nest, Nestus, Realm, Pratum, Livwrk, Landrx, Laken).
2. Três direções de símbolo (Torre, Facho, Lente) e a fusão das três, recusada por não ser moderna nem minimalista.
3. Proposta 5: só o nome, preto e branco, como as marcas imobiliárias de alto padrão (Compass, Aman, Related, JHSF), com a cidade acesa como fotografia. Aprovada.

Pendente: fotos de arquitetura para as aplicações (banco de imagens liberado, fotos próprias ou geração no Canva) e busca do nome no INPI.
