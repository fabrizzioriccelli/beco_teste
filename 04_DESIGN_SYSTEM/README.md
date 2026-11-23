# Design system — Faro (v5.0)

Base do site e do boletim por e-mail. Tokens em [tokens.css](tokens.css), marca em [03_BRAND_IDENTITY](../03_BRAND_IDENTITY/).

## Princípios

1. **Preto e branco.** A única cor é a luz quente da cidade, e ela fica na imagem, nunca em texto ou botão.
2. **Estilo Apple.** Fonte do sistema (SF Pro), escala do iOS, listas agrupadas, cápsulas, cantos concêntricos.
3. **Liquid Glass na navegação, nunca no conteúdo** (Apple HIG, Materials). Vidro na barra do topo, nos controles e na ficha do imóvel; listas e cartões em superfície sólida. Sobre a cidade acesa, a variante transparente com camada de escurecimento. O vidro é **nítido**: desfoque baixo (4 px), saturação alta (190%), borda que pega luz (fio branco no alto e à esquerda) e reflexo suave no topo. No Chrome e no Edge, uma lente SVG gerada pelo script curva o fundo nas bordas, como a refração do vidro da Apple; no Safari fica o vidro nítido sem a lente.
4. **A cidade é a fotografia.** O herói do site e o topo do e-mail mostram os prédios HIS/HMP como luzes; os imóveis do dia ganham um anel.

## Cores

| Token | HEX | Uso | Contraste |
|---|---|---|---|
| `--preto` / `--texto` | #0B0B0C | Texto, botão principal, logotipo | 19,8:1 no branco |
| `--branco` / `--superficie` | #FFFFFF | Listas, cartões, fichas | — |
| `--fundo` | #F5F5F7 | Fundo da página e do e-mail | — |
| `--pedra` | #F4F3F1 | Áreas de respiro | — |
| `--texto-2` | #6E6E73 | Texto secundário | 5,1:1 no branco |
| `--noite` | #06080B | Herói (a cidade à noite) | — |
| `--luz` | #FFC888 | Só nos pontos da cidade | — |
| `--ganho` | #1E7A34 | Valorização acima da inflação | 5,4:1 |
| `--atencao` | #B25000 | Avisos | 5,2:1 |
| `--alerta` | #D70015 | Acima do teto, perda real | 5,4:1 |

Tema escuro: cores de sistema da Apple (fundo #000000, superfície #1C1C1E, texto #F5F5F7, ganho #30D158, alerta #FF453A).

## Tipografia

| Papel | Fonte | Observação |
|---|---|---|
| Texto, títulos e números | SF Pro (fonte do sistema) | `-apple-system`; nos aparelhos que não são Apple, Geist |
| Logotipo e rótulos curtos | Geist Light, maiúsculas, espaçamento 0,42 eme | OFL |

A licença da SF não permite embuti-la na web nem usá-la em logotipo; por isso o site chama a fonte do aparelho. Escala do iOS: 34 / 28 / 22 / 20 / 17 / 15 / 13 / 12 px; título do herói até 72 px.

## Componentes

| Componente | Regra |
|---|---|
| **Barra** | Cápsula de vidro flutuante: FARO, data e botão "Perguntar". Variante escura sobre a cidade, clara sobre o conteúdo |
| **Herói** | Texto sempre sobre preto liso (rótulo em versais, título em SF 600, resumo em cinza). A cidade acesa fica numa faixa própria, sangrada de ponta a ponta, embaixo do texto; os três números do dia em vidro escuro sobrepõem o pé da faixa. Nenhum ponto de luz atrás de texto corrido |
| **Pergunte ao Faro** | Barra de vidro fixa no pé da tela ("Pergunte ao Faro"), também aberta pelo botão da barra do topo. Abre um painel de vidro com sugestões, a conversa em balões e os prédios como cartões; leva a pessoa às seções do app (boletim, destaques, mapa, calculadora) |
| **Lista agrupada** | Título da seção em 22 px; grupo branco com raio 22; linhas com título 17 semibold, contexto 15 cinza, valor à direita e seta › |
| **Ficha do imóvel** | Folha de vidro flutuante (raio 28, margem 14, blocos internos com raio 14); no celular, folha que sobe de baixo |
| **Botão** | Cápsula preta (principal) ou cinza-claro; texto com verbo ("Achar quem vende") |
| **Controle segmentado** | Cápsula cinza com a opção ativa em branco |
| **E-mail** | Tabelas com estilos inline, 600 px. Topo preto com FARO em texto, a imagem da cidade do dia, números em painéis; listas brancas; botão cápsula |

Com "reduzir transparência" ligado no aparelho, todo vidro vira superfície sólida.

## Grade

Uma coluna de 920 px no máximo, com margens laterais de 20 px (ou a área segura do aparelho). Barra do topo, herói, números, listas, cartões e rodapé usam as mesmas bordas. Espaçamento em múltiplos de 8; 72 px entre seções.

## Voz

Direta e completa: número, contexto e próximo passo, em frases curtas. Termo técnico só quando ele é o certo (ITBI, alvará, matrícula, teto), sem explicar o óbvio para quem é do ramo.

## Desempenho

- O site carrega primeiro o boletim, os pontos da cidade e os distritos (cerca de 80 KB comprimidos); a base completa chega em segundo plano.
- A cidade acesa é desenhada uma vez, com um sprite de luz; os anéis dos imóveis do dia são animados em CSS (sem redesenhar o canvas).
- O mapa é um canvas único (sem biblioteca e sem 5 mil elementos na página); o clique acha o prédio mais próximo.
- Seções fora da tela não são desenhadas até chegar perto (`content-visibility`); a busca espera 120 ms entre teclas.
- Modo leve: quem pede menos movimento ou menos transparência, ou aparelho muito fraco, recebe vidro sólido e nenhuma animação.

Medição em 23/11/2026 (mesma página, antes → depois): download 3,9 → 1,6 MB (0,45 MB comprimido); tempo de JavaScript 4,15 → 0,03 s; elementos na página 17.584 → 1.465; rolagem 13 → 59 quadros por segundo (58 com o processador 6 vezes mais lento).
