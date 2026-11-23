# Design system — Faro (v3.0, alto padrão)

Base visual do site e do boletim por e-mail. Tokens em [tokens.css](tokens.css), logo em [03_BRAND_IDENTITY/faro](../03_BRAND_IDENTITY/faro/) e manual de marca em [03_BRAND_IDENTITY/manual](../03_BRAND_IDENTITY/manual/) (publicado em https://claude.ai/artifact/4GWnbgo3bev3XKnsu2kc6v).

## Direção

Pedido de 23/11/2026: "mais sofisticado, algo alta renda". O Faro serve a quem investe; a marca passa a ter cara de relatório privado e de imobiliária boutique. Referências do [benchmark do Behance](../01_RESEARCH_BENCHMARK/BENCHMARK_VISUAL_BEHANCE.md):

| Referência | O que trouxemos |
|---|---|
| [Brickell](https://www.behance.net/gallery/252336603/Brickell) | Posicionamento por patrimônio e investimento; nome em serifa de versais espaçadas |
| [Forte](https://www.behance.net/gallery/257568569/Forte-Luxury-Architecture-Brand-Identity) | Sistema de monograma + logotipo |
| [Orchard Hill](https://www.behance.net/gallery/237797617/Orchard-Hill-Refined-living-experience) | Contenção: fios finos, pouco texto, muito vazio |
| [SOLA](https://www.behance.net/gallery/254893035/SOLA-Architecture-Studio-Luxury-Real-Estate-Website) | Espaçamento generoso entre letras e entre blocos |

Evitamos: preto com dourado brilhante, degradê e folha metálica, letra cursiva, brasão e foto de mansão de banco de imagem.

## Cores

| Token | Nome | HEX | RGB | CMYK (aprox.) | Uso | Contraste |
|---|---|---|---|---|---|---|
| `--tinta` | Verde Jardim | #17302A | 23, 48, 42 | 52, 0, 13, 81 | Banda, títulos, monograma, botão principal | 11,7:1 no travertino |
| `--facho` | Latão | #B08D57 | 176, 141, 87 | 0, 20, 51, 31 | Facho, fios, marcadores | 2,9:1: só decorativo |
| `--facho-claro` | Latão claro | #C9A878 | 201, 168, 120 | 0, 16, 40, 21 | Latão sobre o verde | 6,3:1 no verde |
| `--facho-escuro` | Latão escuro | #7D5F38 | 125, 95, 56 | 0, 24, 55, 51 | Rótulos, links, numerais romanos | 5,6:1 no papel |
| `--travertino` | Travertino | #EFEAE1 | 239, 234, 225 | 0, 2, 6, 6 | Fundo da página e do e-mail | — |
| `--papel` | Papel | #FBF9F5 | 251, 249, 245 | 0, 1, 2, 2 | Boletim, cartões e fichas | — |
| `--texto` | Ônix | #1A2622 | 26, 38, 34 | 32, 0, 11, 85 | Texto corrido | 13:1 no travertino |
| `--grafite` | Grafite | #5B625D | 91, 98, 93 | 7, 0, 5, 62 | Texto secundário | 6,0:1 no papel |
| `--ganho` | Ganho | #2D6A4F | 45, 106, 79 | 58, 0, 25, 58 | Valorização acima da inflação | 6,1:1 no papel |
| `--atencao` | Atenção | #8A5A12 | 138, 90, 18 | 0, 35, 87, 46 | Ganho abaixo do CDI, avisos | 5,6:1 no papel |
| `--alerta` | Alerta | #9E2B25 | 158, 43, 37 | 0, 73, 77, 38 | Acima do teto, perda real | 7,1:1 no papel |

Todo texto atende WCAG AA (4,5:1). O CMYK é conversão matemática: valide com prova de cor. O tema escuro tem valores próprios em `tokens.css` (fundo verde-noite, texto travertino, latão claro).

## Tipografia

| Papel | Fonte | Pesos | Uso |
|---|---|---|---|
| Nome, títulos e números | **Bodoni Moda** | 400, 500 | Didone de alto contraste com tamanho óptico; números de destaque do boletim |
| Texto e rótulos | **Jost** | 300, 400, 500 | Geométrica (linhagem Futura). Texto em 300/400; rótulos em versais 11 px com espaçamento 0,22 em |

Licença OFL. Escala: herói 64 / 44 / 28 / 20 / 16 / 14 / 11 px. No e-mail, a pilha de fontes cai para Bodoni 72 ou Didot (Apple) e Georgia (demais).

## Componentes

| Componente | Regra |
|---|---|
| **Banda de marca** | Verde Jardim com a assinatura negativa e a data em versais de latão claro; fio de latão de 1 px embaixo |
| **Rótulo editorial** | Jost 500, 11 px, versais, espaçamento 0,22 em, latão escuro |
| **Título do boletim** | Bodoni Moda 500, 42 a 64 px |
| **Herói numérico** | Três números em Bodoni verde, entre fio de latão (cima) e fio claro (baixo) |
| **Seção** | Numeral romano em Bodoni (I, II, III) + título em versais de Jost |
| **Item do boletim** | Losango de latão de 6 px, endereço em Bodoni 18 px (grafia de título, nunca caixa alta), contexto em versais, "Ver contatos e detalhes →" em latão escuro; à direita o número em Bodoni 28 px |
| **Botão** | Principal: fundo verde, texto travertino, versais 12 px espaçadas. Secundário: fio de latão |
| **Chip de estado** | Retângulo de raio 2 com o par cor + fundo do token, sempre com texto |

**Endereços:** a Prefeitura publica em caixa alta; o Redator e o site convertem para grafia de título ("Rua Major Ari Gomes, 29, Vila Mazzei").

**E-mail:** tabelas com estilos inline, 600 px, sem imagens (o logo é texto), para funcionar no Gmail e no Outlook com imagens bloqueadas.

## Voz

Discreta e precisa, como um relatório privado. Número, contexto e próximo passo; sem exclamação e sem promessa que o dado não sustenta. Exemplo: "Três revendas novas em Itaquera. A melhor ganhou 12% acima da inflação."
