# 03 — Identidade visual

**Faro v3.0 (23/11/2026), direção alto padrão.** Conceito "endereço nobre": o F de Faro em Bodoni, como as letras de latão na fachada dos prédios de alto padrão de São Paulo, com um facho de luz de latão que sai da serifa superior. Paleta dos materiais desses prédios: verde Jardim, latão e travertino.

Manual completo (direção, referências do Behance, materiais, monograma, assinaturas, paleta, tipografia, componentes, aplicações e usos incorretos): `manual/index.html`, publicado em https://claude.ai/artifact/4GWnbgo3bev3XKnsu2kc6v.

## Arquivos

| Arquivo | Uso |
|---|---|
| `faro/assinatura.svg` | Principal: monograma, fio de latão, FARO e descritor. Fundo claro |
| `faro/assinatura-negativa.svg` | Sobre verde Jardim (banda do site) |
| `faro/assinatura-mono.svg` | Uma cor |
| `faro/assinatura-sem-descritor*.svg` | Espaços menores |
| `faro/logotipo.svg`, `faro/logotipo-negativo.svg` | Só FARO em versais espaçadas |
| `faro/assinatura-vertical.svg` | Capas e telas quadradas |
| `faro/simbolo*.svg` | Monograma (cor, negativo, uma cor) |
| `faro/icone-app.svg`, `faro/favicon.svg` | Selo verde com fio de latão; aba do navegador |
| `faro/construcao.svg` | Folha de construção do monograma |
| `faro/png/` | Ícone 512/192/180, favicon 32/48/64, monograma 256, assinaturas a 120 px |
| `manual/` | Manual de marca (`gerar_manual.py` gera o `index.html`) |
| `arquivo/faro-v2/` | Versão 2 (grotesca e laranja), substituída em 23/11/2026 |
| `arquivo/radar-his-v1/` | Versão 1 ("Radar HIS") |

O texto do logo está em curvas e não depende de fonte instalada. Para regerar:

```
python3 03_BRAND_IDENTITY/gerar_identidade.py --fontes <pasta com @fontsource/bodoni-moda e @fontsource/jost> --saida 03_BRAND_IDENTITY/faro
python3 03_BRAND_IDENTITY/manual/gerar_manual.py
```

## Construção do monograma

- F da Bodoni Moda 500. O facho começa 60 unidades (4% da versal) depois da serifa superior, mede 900 (60% da versal) e abre de 70 para 500 unidades.
- O eixo do facho passa no centro da serifa superior; as bordas do facho se encontram na serifa.
- Área de proteção: um terço da altura da versal. Mínimo: 16 px (favicon) e 32 px de altura (assinatura horizontal).

Cores, tipografia e componentes: [04_DESIGN_SYSTEM/README.md](../04_DESIGN_SYSTEM/README.md).

Pendente antes de registrar: busca no INPI (classes 9, 35, 36 e 42) e disponibilidade de domínio.
