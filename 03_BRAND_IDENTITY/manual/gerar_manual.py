#!/usr/bin/env python3
"""Gera o manual da marca Faro (manual/index.html) com os SVGs oficiais embutidos."""
import pathlib
import re

AQUI = pathlib.Path(__file__).resolve().parent
LOGO = AQUI.parent / "faro"
TOKENS = (AQUI.parents[1] / "04_DESIGN_SYSTEM" / "tokens.css").read_text(encoding="utf-8")


def svg(nome, altura, extra=""):
    s = (LOGO / nome).read_text(encoding="utf-8").strip()
    return re.sub(r' width="[\d.]+" height="[\d.]+"', f' style="height:{altura}px;width:auto;display:block" {extra}', s, count=1)


CORES = [
    ("Tinta", "#0F1E46", "15, 30, 70", "79, 57, 0, 73", "16,2:1 no branco", "Texto, banda de marca, haste do símbolo", "#FFFFFF"),
    ("Facho", "#FF5A1F", "255, 90, 31", "0, 65, 88, 0", "5,2:1 com Tinta", "Assinatura: facho, botão principal, números grandes", "#0F1E46"),
    ("Facho escuro", "#C2410C", "194, 65, 12", "0, 66, 94, 24", "5,2:1 no branco", "Laranja para texto e links", "#FFFFFF"),
    ("Névoa", "#D9E4F5", "217, 228, 245", "11, 7, 0, 4", "12,6:1 com Tinta", "Superfícies de apoio", "#0F1E46"),
    ("Gelo", "#F5F7FB", "245, 247, 251", "2, 2, 0, 2", "15,1:1 com Tinta", "Fundo da página", "#0F1E46"),
    ("Grafite", "#4B5875", "75, 88, 117", "36, 25, 0, 54", "7,1:1 no branco", "Texto secundário", "#FFFFFF"),
    ("Ganho", "#11795A", "17, 121, 90", "86, 0, 26, 53", "5,4:1 no branco", "Valorização acima da inflação", "#FFFFFF"),
    ("Alerta", "#C0262D", "192, 38, 45", "0, 80, 77, 25", "5,9:1 no branco", "Acima do teto, perda real", "#FFFFFF"),
]

REFERENCIAS = [
    ("Astrix Builders", "https://www.behance.net/gallery/226083297/Astrix-Builders-Construction-brand-identity",
     "Laranja vivo com azul-marinho; símbolo geométrico com grade de construção; grotesca sóbria.",
     "A dupla Tinta e Facho, e a folha de construção do símbolo com as medidas à mostra."),
    ("Alliance", "https://www.behance.net/gallery/257399129/Alliance-Brand-Identity",
     "Uma cor forte sobre cinza; números gigantes (94%, 250+, $11.4M) como peça gráfica; frases curtas e diretas.",
     "O herói numérico do boletim e o número grande à direita de cada imóvel."),
    ("Lumen", "https://www.behance.net/gallery/258362035/LUMEN-WEBSITE-BRANDING",
     "Rótulos pequenos com traço (— CHALLENGE), linhas finas, uma grade e uma família tipográfica só.",
     "Os rótulos editoriais em mono ('01 — Alvarás novos') e o sistema com uma família principal."),
    ("Bilge İnşaat", "https://www.behance.net/gallery/231472123/Bilge-nsaat-Modern-Real-Estate-Branding",
     "Símbolo construído sobre grade e círculos; logotipo com área de proteção desenhada.",
     "A regra de área de proteção (8 módulos) e a apresentação técnica da marca."),
]


def main():
    tokens = re.sub(r"/\*.*?\*/\n", "", TOKENS, count=1, flags=re.S)
    cores = "".join(f"""
      <div class="cor">
        <div class="amostra" style="background:{h};color:{txt}"><b>{n}</b><span>{h}</span></div>
        <dl><dt>RGB</dt><dd>{r}</dd><dt>CMYK</dt><dd>{c}</dd><dt>Contraste</dt><dd>{k}</dd></dl>
        <p>{uso}</p>
      </div>""" for n, h, r, c, k, uso, txt in CORES)
    refs = "".join(f"""
      <article class="ref">
        <h4><a href="{link}" target="_blank" rel="noopener">{nome} ↗</a></h4>
        <p class="rot">O que vimos</p><p>{vimos}</p>
        <p class="rot">O que trouxemos</p><p>{trouxemos}</p>
      </article>""" for nome, link, vimos, trouxemos in REFERENCIAS)
    simb = (LOGO / "simbolo.svg").read_text(encoding="utf-8")
    corpo_simb = re.search(r"<title>Faro</title>(.*)</svg>", simb, re.S).group(1)
    erros = [
        ("Não distorcer", f'<svg viewBox="0 0 48 48" style="height:64px;width:110px"><g transform="scale(2.2,1)">{corpo_simb}</g></svg>'),
        ("Não trocar as cores", f'<svg viewBox="0 0 48 48" style="height:64px">{corpo_simb.replace("#0F1E46", "#XXXXXX").replace("#FF5A1F", "#0F1E46").replace("#XXXXXX", "#FF5A1F")}</svg>'),
        ("Não colar o facho na haste", '<svg viewBox="0 0 48 48" style="height:64px"><rect x="6" y="6" width="11" height="36" fill="#0F1E46"/><polygon points="17,10.5 46,1 46,20 17,15.5" fill="#FF5A1F"/><rect x="17" y="23" width="16" height="8" fill="#0F1E46"/></svg>'),
        ("Não pôr dentro de pin, casa ou círculo", f'<svg viewBox="0 0 64 64" style="height:64px"><circle cx="32" cy="32" r="30" fill="#D9E4F5"/><g transform="translate(8 8)">{corpo_simb}</g></svg>'),
    ]
    erros_html = "".join(f'<div class="erro"><div class="erro-img">{s}<i aria-hidden="true">×</i></div><p>{t}</p></div>' for t, s in erros)

    html = f"""<title>Marca Faro</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
/* Layout: case de identidade em blocos largos; capa na banda de marca; cada capítulo numerado como no boletim. */
{tokens.strip()}
* {{ box-sizing: border-box; }}
body {{ background: var(--gelo); color: var(--texto); font-family: var(--fonte-texto); font-size: 16px; line-height: 1.55; margin: 0; }}
.in {{ max-width: 1120px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
.capa {{ background: var(--banda); color: var(--banda-texto); margin-top: calc(-1 * env(safe-area-inset-top, 0px)); padding-top: calc(env(safe-area-inset-top, 0px) + 56px); padding-bottom: 64px; border-bottom: 8px solid var(--facho); }}
.capa .in {{ display: grid; gap: 28px; }}
.capa .rot {{ color: var(--banda-texto); opacity: .7; }}
.capa h1 {{ font-size: clamp(44px, 9vw, 104px); font-weight: 900; letter-spacing: -.045em; line-height: .95; margin: 0; max-width: 11ch; text-wrap: balance; }}
.capa h1 em {{ font-style: normal; color: var(--facho); }}
.capa p {{ max-width: 56ch; font-size: 18px; margin: 0; opacity: .9; }}
.capa .marca svg {{ height: clamp(56px, 10vw, 96px) !important; }}
.rot {{ font-family: var(--fonte-dado); font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: var(--grafite); margin: 0; }}
section.cap {{ padding-block: 64px 8px; }}
.cap-h {{ display: grid; gap: 10px; border-top: 2px solid var(--texto); padding-top: 14px; margin-bottom: 28px; }}
.cap-h .rot b {{ color: var(--facho-escuro); font-weight: 500; }}
h2 {{ font-size: clamp(30px, 5vw, 52px); font-weight: 900; letter-spacing: -.035em; line-height: 1.02; margin: 0; max-width: 20ch; text-wrap: balance; }}
h3 {{ font-size: 21px; font-weight: 800; letter-spacing: -.015em; margin: 0 0 6px; }}
h4 {{ font-size: 18px; font-weight: 800; margin: 0 0 8px; }}
p {{ margin: 0 0 10px; max-width: 68ch; }}
a {{ color: var(--facho-escuro); }}
.grid2 {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }}
.grid3 {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
.grid4 {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }}
@media (max-width: 860px) {{ .grid2, .grid3, .grid4 {{ grid-template-columns: minmax(0, 1fr); }} }}
.bloco {{ background: var(--papel); border: 1px solid var(--linha); padding: 22px; min-width: 0; }}
.numeros {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); border-top: 2px solid var(--texto); border-bottom: 1px solid var(--linha); margin-bottom: 24px; }}
.numeros div {{ padding: 16px 12px 16px 0; }}
.numeros div + div {{ border-left: 1px solid var(--linha); padding-left: 16px; }}
.numeros b {{ display: block; font-size: clamp(36px, 7vw, 64px); font-weight: 900; letter-spacing: -.04em; line-height: 1; color: var(--facho); }}
.numeros span {{ font-size: 14px; color: var(--grafite); }}
.ref .rot {{ margin-top: 12px; }}
.ref p:not(.rot) {{ font-size: 15px; }}
.evitar {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }}
.evitar li {{ border-left: 3px solid var(--alerta); padding: 4px 0 4px 12px; }}
.nome-grande {{ font-size: clamp(80px, 18vw, 220px); font-weight: 900; letter-spacing: -.06em; line-height: .85; margin: 0 0 18px; color: var(--texto); }}
.nome-grande span {{ color: var(--facho); }}
.descartes {{ display: grid; gap: 8px; margin-top: 8px; }}
.descartes div {{ display: grid; grid-template-columns: 110px minmax(0, 1fr); gap: 12px; padding: 10px 0; border-top: 1px solid var(--linha); }}
.descartes b {{ text-decoration: line-through; text-decoration-color: var(--alerta); }}
.palco {{ display: grid; place-items: center; min-height: 220px; padding: 28px; border: 1px solid var(--linha); }}
.palco.escuro {{ background: #0F1E46; border-color: #0F1E46; }}
.palco.laranja {{ background: #FF5A1F; border-color: #FF5A1F; }}
.palco.claro {{ background: #FFFFFF; }}
.legenda {{ font-family: var(--fonte-dado); font-size: 12px; color: var(--grafite); margin-top: 8px; }}
.icones {{ display: flex; flex-wrap: wrap; gap: 24px; align-items: end; }}
.cor .amostra {{ aspect-ratio: 4 / 3; max-width: 100%; display: flex; flex-direction: column; justify-content: flex-end; padding: 14px; gap: 2px; border: 1px solid var(--linha); }}
.cor .amostra b {{ font-size: 20px; font-weight: 800; }}
.cor .amostra span {{ font-family: var(--fonte-dado); font-size: 13px; }}
.cor dl {{ display: grid; grid-template-columns: auto 1fr; gap: 2px 12px; margin: 10px 0 6px; font-size: 13px; }}
.cor dt {{ font-family: var(--fonte-dado); color: var(--grafite); }}
.cor dd {{ margin: 0; font-variant-numeric: tabular-nums; }}
.cor p {{ font-size: 14px; color: var(--grafite); }}
.tipo-display {{ font-size: clamp(44px, 6.4vw, 78px); font-weight: 900; letter-spacing: -.05em; line-height: .9; margin: 6px 0 14px; }}
.pesos {{ display: flex; flex-wrap: wrap; gap: 8px 22px; font-size: 26px; }}
.mono {{ font-family: var(--fonte-dado); }}
.escala div {{ display: grid; grid-template-columns: 70px minmax(0, 1fr); gap: 12px; align-items: baseline; padding: 6px 0; border-top: 1px solid var(--calcada); overflow-wrap: anywhere; }}
.comp-num {{ font-size: 56px; font-weight: 900; letter-spacing: -.04em; line-height: 1; color: var(--facho); }}
.acoes {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }}
.btn {{ display: inline-block; padding: 13px 20px; font-weight: 700; text-decoration: none; }}
.btn.prim {{ background: #FF5A1F; color: #0F1E46; }}
.btn.sec {{ background: #0F1E46; color: #FFFFFF; }}
.chip {{ display: inline-block; font-size: 13px; padding: 3px 10px; border-radius: 999px; margin: 0 6px 6px 0; }}
.item {{ display: grid; grid-template-columns: 14px minmax(0, 1fr) auto; gap: 4px 10px; padding: 14px 0; border-bottom: 1px solid var(--linha); }}
.item i {{ width: 9px; height: 9px; background: var(--facho); margin-top: 7px; }}
.item b.t {{ font-weight: 800; }}
.item .d {{ text-align: right; }}
.item .d b {{ font-size: 26px; font-weight: 900; color: var(--ganho); letter-spacing: -.02em; }}
.aplic {{ display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 20px; align-items: start; }}
@media (max-width: 860px) {{ .aplic {{ grid-template-columns: minmax(0, 1fr); }} }}
.aplic img {{ width: 100%; height: auto; display: block; border: 1px solid var(--linha); }}
.telefone {{ max-width: 340px; margin: 0 auto; border: 10px solid #0F1E46; border-radius: 34px; overflow: hidden; }}
.telefone img {{ border: 0; }}
.erro {{ text-align: left; }}
.erro-img {{ position: relative; display: grid; place-items: center; height: 120px; background: var(--papel); border: 1px solid var(--linha); }}
.erro-img i {{ position: absolute; top: 6px; right: 10px; font-style: normal; font-weight: 900; font-size: 22px; color: var(--alerta); }}
.erro p {{ font-size: 14px; margin-top: 8px; }}
footer {{ padding-block: 56px 64px; color: var(--grafite); font-size: 13px; }}
</style>

<header class="capa"><div class="in">
  <p class="rot">Manual de marca · v2.0 · 23/11/2026</p>
  <div class="marca">{svg("assinatura-negativa.svg", 96)}</div>
  <h1>O faro do mercado HIS. <em>Todo dia às 8h.</em></h1>
  <p>Faro é a inteligência imobiliária que acompanha os prédios HIS e HMP de São Paulo e avisa, toda manhã, o que mudou e onde está a oportunidade.</p>
</div></header>

<main class="in">
  <section class="cap">
    <div class="cap-h"><p class="rot"><b>01</b> — Pesquisa</p><h2>O que os projetos do Behance mostraram</h2></div>
    <p>Analisamos os 24 projetos que o Behance mostra na busca "real estate" (ordem "Recommended", 23/11/2026) e abrimos seis identidades inteiras.</p>
    <div class="numeros"><div><b>11</b><span>sites de imóvel de luxo</span></div><div><b>11</b><span>identidades de construtora e imobiliária</span></div><div><b>~15</b><span>usam preto, creme e dourado</span></div></div>
    <div class="grid4">{refs}</div>
    <div class="grid2" style="margin-top:16px">
      <div class="bloco"><h3>O padrão que dominava</h3><p>Preto com creme e dourado, serifas finas, foto de mansão em tela cheia. É o visual de alto padrão: bonito, mas repetido e errado para quem trabalha com habitação social.</p></div>
      <div class="bloco"><h3>O que deixamos de fora</h3><ul class="evitar"><li>Dourado, preto e serifa de luxo</li><li>Foto de banco de imagem no lugar do imóvel real</li><li>Casinha, telhado, pin de mapa</li><li>Gradientes e mockups 3D</li></ul></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="rot"><b>02</b> — Nome</p><h2>Faro: o instinto de achar a oportunidade antes</h2></div>
    <div class="grid2">
      <div><p class="nome-grande">far<span>o</span></p>
        <p>"Ter faro para negócio" é a expressão que todo corretor conhece: o instinto de farejar a oportunidade antes dos outros. É exatamente o que o produto faz toda manhã. O nome também lembra o farol, que ilumina o caminho.</p>
        <p>Quatro letras, fácil de falar e de buscar, vira verbo ("o Faro achou três revendas") e funciona por voz ("Faro, o que saiu hoje?").</p></div>
      <div class="bloco"><h3>Nomes descartados</h3><div class="descartes">
        <div><b>BECO</b><span>Remete a lugar escuro e a "beco sem saída".</span></div>
        <div><b>Radar HIS</b><span>Genérico e técnico; "radar" é clichê de monitoramento.</span></div>
        <div><b>Lastro</b><span>Já é uma proptech grande no Brasil (a da assistente Lais).</span></div>
        <div><b>Prumo</b><span>Associado à Prumo Logística.</span></div>
      </div><p class="legenda">Pendente antes de registrar: busca no INPI (classes 9, 35, 36 e 42) e domínio.</p></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="rot"><b>03</b> — Símbolo</p><h2>Um F que é farol</h2></div>
    <div class="grid2">
      <div class="palco claro">{svg("construcao.svg", 300)}</div>
      <div><h3>Construção</h3>
        <p><b>Haste</b>: o prédio e o farol. <b>Facho</b>: a luz que sai da haste e se abre até encontrar o alvo. <b>Braço</b>: fecha a leitura do F.</p>
        <p>Grade de 48 módulos. Haste de 11 × 36. O facho começa a 2 módulos da haste (a "rua" que separa a luz da torre), com 5 módulos de altura, e abre até 19. O braço tem 16 × 8. A área de proteção em volta de qualquer assinatura é de 8 módulos, a altura do braço.</p>
        <p>Tamanho mínimo: 16 px de altura para o favicon e 24 px para a assinatura horizontal.</p></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="rot"><b>04</b> — Assinaturas</p><h2>Variações para cada fundo</h2></div>
    <div class="grid2">
      <div><div class="palco claro">{svg("assinatura.svg", 72)}</div><p class="legenda">Principal · fundo claro</p></div>
      <div><div class="palco escuro">{svg("assinatura-negativa.svg", 72)}</div><p class="legenda">Negativa · fundo Tinta ou foto escura</p></div>
      <div><div class="palco laranja">{svg("assinatura-mono.svg", 72)}</div><p class="legenda">Monocromática · sobre Facho, carimbo, impressão em uma cor</p></div>
      <div><div class="palco claro">{svg("assinatura-vertical.svg", 140)}</div><p class="legenda">Vertical · capas e telas quadradas</p></div>
    </div>
    <div class="bloco" style="margin-top:16px"><div class="icones">{svg("icone-app.svg", 120)}{svg("icone-app.svg", 64)}{svg("favicon.svg", 32)}{svg("favicon.svg", 16)}{svg("simbolo.svg", 64)}{svg("simbolo-mono.svg", 64)}</div>
      <p class="legenda">Ícone de app (120 e 64 px), favicon (32 e 16 px), símbolo e símbolo monocromático</p></div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="rot"><b>05</b> — Cor</p><h2>Tinta e Facho</h2></div>
    <p>Azul-noite para a confiança e laranja para o que importa hoje. Uma cor forte sobre base neutra, como nas melhores identidades do benchmark, sem cair no preto e dourado do luxo. O laranja é para preenchimento e números grandes; em texto pequeno, use o Facho escuro.</p>
    <div class="grid4">{cores}</div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="rot"><b>06</b> — Tipografia</p><h2>Schibsted Grotesk e JetBrains Mono</h2></div>
    <div class="grid2">
      <div class="bloco"><p class="rot">Marca e texto · Schibsted Grotesk</p><p class="tipo-display">O que rolou ontem</p>
        <div class="pesos"><span style="font-weight:400">Regular</span><span style="font-weight:500">Medium</span><span style="font-weight:700">Bold</span><span style="font-weight:900">Black</span></div>
        <p style="margin-top:14px">Grotesca desenhada para o jornal norueguês Schibsted: firme nos títulos, muito legível no celular e com números fortes. É uma família só para marca e texto, como no Lumen. Licença OFL, uso comercial livre.</p></div>
      <div class="bloco"><p class="rot">Dados · JetBrains Mono</p><p class="mono" style="font-size:22px;margin:6px 0 14px">01 — ALVARÁS NOVOS<br>SQL 117.141.0015-5<br>Matrícula 543.554 · 11º RI</p>
        <p>Rótulos, datas, códigos e fontes. Lembra documento de registro e alinha os números.</p>
        <div class="escala"><div><span class="rot">56</span><span style="font-size:40px;font-weight:900;letter-spacing:-.04em">Herói 5.250</span></div><div><span class="rot">40</span><span style="font-size:30px;font-weight:900">Título</span></div><div><span class="rot">26</span><span style="font-size:22px;font-weight:800">Seção</span></div><div><span class="rot">16</span><span>Texto corrido do boletim</span></div><div><span class="rot">12</span><span class="mono" style="font-size:12px;letter-spacing:.14em">RÓTULO EDITORIAL</span></div></div></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="rot"><b>07</b> — Componentes</p><h2>As peças do boletim</h2></div>
    <div class="grid3">
      <div class="bloco"><p class="rot">Herói numérico</p><p class="comp-num">4</p><p class="legenda" style="margin:0">alvarás novos</p></div>
      <div class="bloco"><p class="rot">Item do boletim</p><div class="item"><i></i><span><b class="t">Rua Frei Caneca, 651</b><br><span class="legenda" style="margin:0">Bela Vista · AP 304</span><br><a href="#">Ver contatos e detalhes →</a></span><span class="d"><b>+20%</b><br><span class="legenda" style="margin:0">acima da inflação</span></span></div></div>
      <div class="bloco"><p class="rot">Ações e estados</p><p class="acoes"><a class="btn prim" href="#">Abrir o Faro →</a><a class="btn sec" href="#">Achar quem vende</a></p>
        <span class="chip" style="background:var(--ganho-fundo);color:var(--ganho)">+8% acima da inflação</span><span class="chip" style="background:var(--alerta-fundo);color:var(--alerta)">acima do teto</span><span class="chip" style="background:var(--calcada)">142 unidades</span></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="rot"><b>08</b> — Aplicações</p><h2>O boletim das 8h e o site</h2></div>
    <div class="aplic">
      <div><img src="img/app_email.jpg" alt="E-mail do boletim diário Faro"><p class="legenda">E-mail diário: banda Tinta com o logo, título, três números do dia e seções numeradas. Feito só com HTML: aparece mesmo com imagens bloqueadas.</p></div>
      <div><div class="telefone"><img src="img/app_site.jpg" alt="Site Faro no celular"></div><p class="legenda" style="text-align:center">Site no celular: o mesmo boletim, mais as fichas com contatos de cada prédio.</p></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="rot"><b>09</b> — Usos incorretos</p><h2>O que não fazer</h2></div>
    <div class="grid4">{erros_html}</div>
  </section>
</main>
<footer class="in">Faro · manual de marca v2.0. Fontes Schibsted Grotesk e JetBrains Mono (OFL). Referências: projetos públicos do Behance citados no capítulo 01, com links para os autores; nenhuma imagem deles foi reproduzida. O nome ainda depende de busca no INPI.</footer>
"""
    (AQUI / "index.html").write_text(html, encoding="utf-8")
    print("manual gerado:", len(html), "bytes")


if __name__ == "__main__":
    main()
