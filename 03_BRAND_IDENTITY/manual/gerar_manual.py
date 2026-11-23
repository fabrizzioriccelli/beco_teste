#!/usr/bin/env python3
"""Gera o manual da marca Faro v3 (manual/index.html) com os SVGs oficiais embutidos."""
import pathlib
import re

AQUI = pathlib.Path(__file__).resolve().parent
LOGO = AQUI.parent / "faro"
V2 = AQUI.parent / "arquivo" / "faro-v2"
TOKENS = (AQUI.parents[1] / "04_DESIGN_SYSTEM" / "tokens.css").read_text(encoding="utf-8")


def svg(caminho, altura, largura_auto=True):
    s = caminho.read_text(encoding="utf-8").strip()
    estilo = f"height:{altura}px;width:auto;max-width:100%;display:block" if largura_auto else f"width:100%;height:auto;display:block"
    return re.sub(r' width="[\d.]+" height="[\d.]+"', f' style="{estilo}"', s, count=1)


def logo(nome, altura):
    return svg(LOGO / nome, altura)


CORES = [
    ("Verde Jardim", "--tinta", "#17302A", "23, 48, 42", "52, 0, 13, 81", "11,7:1 no travertino", "Banda de marca, títulos, monograma, botão principal", "#F4EFE6"),
    ("Latão", "--facho", "#B08D57", "176, 141, 87", "0, 20, 51, 31", "decorativo", "Facho do monograma, fios, marcadores", "#17302A"),
    ("Latão claro", "--facho-claro", "#C9A878", "201, 168, 120", "0, 16, 40, 21", "6,3:1 no verde", "Latão sobre o verde: descritor, datas, botões", "#17302A"),
    ("Latão escuro", "--facho-escuro", "#7D5F38", "125, 95, 56", "0, 24, 55, 51", "5,6:1 no papel", "Rótulos, links e numerais romanos", "#FBF9F5"),
    ("Travertino", "--travertino", "#EFEAE1", "239, 234, 225", "0, 2, 6, 6", "fundo", "Fundo da página e do e-mail", "#17302A"),
    ("Papel", "--papel", "#FBF9F5", "251, 249, 245", "0, 1, 2, 2", "fundo", "Corpo do boletim, cartões e fichas", "#17302A"),
    ("Ônix", "--texto", "#1A2622", "26, 38, 34", "32, 0, 11, 85", "13:1 no travertino", "Texto corrido", "#F4EFE6"),
    ("Grafite", "--grafite", "#5B625D", "91, 98, 93", "7, 0, 5, 62", "6,0:1 no papel", "Texto secundário", "#FBF9F5"),
]

REFERENCIAS = [
    ("Brickell", "https://www.behance.net/gallery/252336603/Brickell",
     "Imobiliária boutique brasileira que se posiciona por patrimônio e investimento, não por sonho. Nome em serifa de versais espaçadas, monograma pequeno, embalagem em marrom e cobre.",
     "O posicionamento de inteligência e patrimônio, e o nome em versais espaçadas como peça principal."),
    ("Forte", "https://www.behance.net/gallery/257568569/Forte-Luxury-Architecture-Brand-Identity",
     "Nome em serifa clássica com um monograma F logo acima, aplicado sobre ripado de madeira escura.",
     "O sistema de monograma + logotipo. Nosso F tem o facho do farol, para não ser só uma inicial."),
    ("Orchard Hill", "https://www.behance.net/gallery/237797617/Orchard-Hill-Refined-living-experience",
     "Peças escuras com luz rasante, tipografia pequena e muito espaço vazio.",
     "A contenção: fios finos, textos curtos, nada de enfeite. A luz entra só no facho."),
    ("SOLA", "https://www.behance.net/gallery/254893035/SOLA-Architecture-Studio-Luxury-Real-Estate-Website",
     "Versais finas e largas sobre muito respiro.",
     "O espaçamento generoso entre letras e entre blocos, no site e no e-mail."),
]


def main():
    tokens = re.sub(r"^/\*.*?\*/\n", "", TOKENS, count=1, flags=re.S)
    cores = "".join(f"""
      <div class="cor">
        <div class="amostra" style="background:{h};color:{txt}"><b>{n}</b><span>{h}</span></div>
        <dl><dt>Token</dt><dd>{tok}</dd><dt>RGB</dt><dd>{r}</dd><dt>CMYK</dt><dd>{c}</dd><dt>Contraste</dt><dd>{k}</dd></dl>
        <p>{uso}</p>
      </div>""" for n, tok, h, r, c, k, uso, txt in CORES)
    refs = "".join(f"""
      <article class="ref">
        <h4><a href="{link}" target="_blank" rel="noopener">{nome} ↗</a></h4>
        <p class="rot">O que vimos</p><p>{vimos}</p>
        <p class="rot">O que trouxemos</p><p>{trouxemos}</p>
      </article>""" for nome, link, vimos, trouxemos in REFERENCIAS)
    simb = (LOGO / "simbolo.svg").read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', simb).group(1)
    corpo = re.search(r"<title>Faro</title>(.*)</svg>", simb, re.S).group(1)
    def circulo():
        w, h = (float(x) for x in vb.split()[2:])
        r = max(w, h) / 2 + 6
        cx, cy = w / 2, h / 2
        caixa = f"{cx - r - 3:.1f} {cy - r - 3:.1f} {2 * r + 6:.1f} {2 * r + 6:.1f}"
        return f'<svg viewBox="{caixa}" style="height:84px"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#B08D57" stroke-width="1.5"/>{corpo}</svg>'
    erros = [
        ("Não distorcer nem condensar", f'<svg viewBox="{vb}" style="height:60px;width:120px" preserveAspectRatio="none">{corpo}</svg>'),
        ("Não usar dourado brilhante, degradê ou efeito de folha metálica",
         f'<svg viewBox="{vb}" style="height:60px"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#FFE08A"/><stop offset=".5" stop-color="#C8962E"/><stop offset="1" stop-color="#FFF3C4"/></linearGradient></defs>'
         + corpo.replace("#17302A", "url(#g)").replace("#B08D57", "url(#g)") + "</svg>"),
        ("Não trocar o latão por outra cor", f'<svg viewBox="{vb}" style="height:60px">{corpo.replace("#B08D57", "#FF5A1F")}</svg>'),
        ("Não pôr o monograma em círculo, brasão ou moldura ornamental", circulo()),
    ]
    erros_html = "".join(f'<div class="erro"><div class="erro-img">{s}<i aria-hidden="true">×</i></div><p>{t}</p></div>' for t, s in erros)

    html = f"""<title>Marca Faro</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..700;1,6..96,400..500&family=Jost:wght@300..600&display=swap">
<style>
/* Layout: livro de marca de boutique. Capa na banda verde; capítulos com numeral romano e fio de latão; muito respiro. */
{tokens.strip()}
* {{ box-sizing: border-box; }}
body {{ background: var(--travertino); color: var(--texto); font-family: var(--fonte-texto); font-size: 16px; font-weight: 400; line-height: 1.65; margin: 0; }}
.in {{ max-width: 1120px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
.capa {{ background: var(--banda); color: var(--banda-texto); margin-top: calc(-1 * env(safe-area-inset-top, 0px)); padding-top: calc(env(safe-area-inset-top, 0px) + 64px); padding-bottom: 80px; border-bottom: 1px solid var(--facho); }}
.capa .in {{ display: grid; gap: 40px; }}
.capa .rot {{ color: var(--facho-claro); }}
.capa h1 {{ font-family: var(--fonte-marca); font-weight: 400; font-size: clamp(40px, 7.4vw, 92px); line-height: 1.02; letter-spacing: -.015em; margin: 0; max-width: 15ch; text-wrap: balance; }}
.capa h1 em {{ color: var(--facho-claro); }}
.capa p.lead {{ max-width: 54ch; font-size: 18px; font-weight: 300; margin: 0; opacity: .92; }}
.capa .marca svg {{ height: clamp(56px, 9vw, 92px) !important; }}
.rot {{ font-family: var(--fonte-dado); font-size: 11.5px; font-weight: 500; letter-spacing: .24em; text-transform: uppercase; color: var(--facho-escuro); margin: 0; }}
section.cap {{ padding-block: 88px 8px; }}
.cap-h {{ display: grid; gap: 14px; margin-bottom: 36px; }}
.cap-h .num {{ font-family: var(--fonte-marca); font-size: 22px; color: var(--facho-escuro); line-height: 1; display: flex; align-items: center; gap: 14px; }}
.cap-h .num::after {{ content: ""; height: 1px; width: 56px; background: var(--facho); }}
h2 {{ font-family: var(--fonte-marca); font-weight: 400; font-size: clamp(32px, 5vw, 56px); letter-spacing: -.01em; line-height: 1.05; margin: 0; max-width: 22ch; text-wrap: balance; color: var(--tinta); }}
h3 {{ font-family: var(--fonte-marca); font-weight: 500; font-size: 22px; margin: 0 0 8px; color: var(--tinta); }}
h4 {{ font-family: var(--fonte-marca); font-weight: 500; font-size: 21px; margin: 0 0 10px; }}
h4 a {{ color: var(--tinta); text-decoration: none; }}
h4 a:hover {{ color: var(--facho-escuro); }}
p {{ margin: 0 0 12px; max-width: 66ch; }}
a {{ color: var(--facho-escuro); text-underline-offset: 3px; text-decoration-thickness: 1px; }}
:focus-visible {{ outline: 1px solid var(--facho-escuro); outline-offset: 3px; }}
.grid2 {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }}
.grid3 {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; }}
.grid4 {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; }}
@media (max-width: 900px) {{ .grid4 {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
@media (max-width: 640px) {{ .grid2, .grid3, .grid4 {{ grid-template-columns: minmax(0, 1fr); }} }}
.bloco {{ background: var(--papel); border: 1px solid var(--linha); padding: 26px; min-width: 0; }}
.antes-agora {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.4fr); gap: 20px; align-items: stretch; }}
@media (max-width: 760px) {{ .antes-agora {{ grid-template-columns: minmax(0, 1fr); }} }}
.antes-agora .palco {{ min-height: 200px; }}
.ref {{ border-top: 1px solid var(--facho); padding-top: 18px; }}
.ref .rot {{ margin-top: 14px; font-size: 10.5px; }}
.ref p:not(.rot) {{ font-size: 15px; }}
.lista {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }}
.lista li {{ display: grid; grid-template-columns: 16px minmax(0, 1fr); gap: 8px; }}
.lista li::before {{ content: ""; width: 6px; height: 6px; background: var(--facho); transform: rotate(45deg); margin-top: 10px; }}
.materiais {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0; border: 1px solid var(--linha); }}
@media (max-width: 640px) {{ .materiais {{ grid-template-columns: minmax(0, 1fr); }} }}
.material {{ padding: 28px; min-height: 260px; display: grid; align-content: end; gap: 6px; }}
.material b {{ font-family: var(--fonte-marca); font-weight: 400; font-size: 30px; line-height: 1.1; }}
.material span {{ font-size: 14.5px; max-width: 30ch; }}
.palco {{ display: grid; place-items: center; min-height: 240px; padding: 32px; border: 1px solid var(--linha); }}
.palco.escuro {{ background: #17302A; border-color: #17302A; }}
.palco.claro {{ background: #FBF9F5; }}
.palco.pedra {{ background: #E7E0D3; border-color: #E7E0D3; }}
.legenda {{ font-family: var(--fonte-dado); font-size: 11px; font-weight: 500; letter-spacing: .16em; text-transform: uppercase; color: var(--grafite); margin-top: 10px; }}
.icones {{ display: flex; flex-wrap: wrap; gap: 28px; align-items: end; }}
.cor .amostra {{ aspect-ratio: 4 / 3; max-width: 100%; display: flex; flex-direction: column; justify-content: flex-end; padding: 16px; gap: 2px; border: 1px solid var(--linha); }}
.cor .amostra b {{ font-family: var(--fonte-marca); font-weight: 500; font-size: 22px; }}
.cor .amostra span {{ font-size: 13px; letter-spacing: .08em; }}
.cor dl {{ display: grid; grid-template-columns: auto 1fr; gap: 3px 14px; margin: 12px 0 6px; font-size: 13px; }}
.cor dt {{ color: var(--grafite); font-size: 11px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; padding-top: 2px; }}
.cor dd {{ margin: 0; font-variant-numeric: tabular-nums; font-variant-ligatures: none; }}
.cor p {{ font-size: 14px; color: var(--grafite); }}
.tipo-display {{ font-family: var(--fonte-marca); font-weight: 400; font-size: clamp(48px, 7vw, 84px); line-height: .98; letter-spacing: -.015em; margin: 10px 0 18px; color: var(--tinta); }}
.pesos {{ display: flex; flex-wrap: wrap; gap: 8px 24px; font-size: 26px; }}
.serif {{ font-family: var(--fonte-marca); }}
.numerais {{ font-family: var(--fonte-marca); font-size: clamp(36px, 5vw, 56px); line-height: 1.1; color: var(--tinta); margin: 8px 0 12px; font-variant-numeric: lining-nums; }}
.escala div {{ display: grid; grid-template-columns: 64px minmax(0, 1fr); gap: 12px; align-items: baseline; padding: 8px 0; border-top: 1px solid var(--linha); overflow-wrap: anywhere; }}
.comp-num {{ font-family: var(--fonte-marca); font-size: 64px; line-height: 1; color: var(--tinta); }}
.btn {{ display: inline-block; padding: 15px 24px; font-size: 12px; font-weight: 500; letter-spacing: .2em; text-transform: uppercase; text-decoration: none; }}
.btn.prim {{ background: #17302A; color: #F4EFE6; }}
.btn.sec {{ border: 1px solid var(--facho); color: var(--tinta); }}
.acoes {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; }}
.chip {{ display: inline-block; font-size: 12.5px; padding: 3px 10px; border-radius: 2px; margin: 0 6px 6px 0; }}
.item {{ display: grid; grid-template-columns: 16px minmax(0, 1fr) auto; gap: 4px 12px; padding: 16px 0; border-bottom: 1px solid var(--linha); }}
.item i {{ width: 6px; height: 6px; background: var(--facho); transform: rotate(45deg); margin: 10px 0 0 3px; }}
.item .t {{ font-family: var(--fonte-marca); font-weight: 500; font-size: 18px; color: var(--tinta); }}
.item .c {{ font-size: 10.5px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: var(--grafite); }}
.item .a {{ font-size: 11px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: var(--facho-escuro); text-decoration: none; }}
.item .d {{ text-align: right; }}
.item .d b {{ font-family: var(--fonte-marca); font-weight: 500; font-size: 28px; color: var(--ganho); }}
.item .d span {{ display: block; font-size: 11.5px; color: var(--grafite); }}
.secao-rot {{ border-bottom: 1px solid var(--linha); padding-bottom: 8px; }}
.secao-rot b {{ font-family: var(--fonte-marca); font-weight: 500; font-size: 15px; letter-spacing: 0; margin-right: 4px; }}
.aplic {{ display: grid; grid-template-columns: minmax(0, 1.3fr) minmax(0, 1fr); gap: 28px; align-items: start; }}
@media (max-width: 860px) {{ .aplic {{ grid-template-columns: minmax(0, 1fr); }} }}
.aplic img {{ width: 100%; height: auto; display: block; border: 1px solid var(--linha); }}
.telefone {{ max-width: 340px; margin: 0 auto; border: 9px solid #17302A; border-radius: 38px; overflow: hidden; outline: 1px solid #B08D57; outline-offset: -1px; }}
.telefone img {{ border: 0; }}
.erro-img {{ position: relative; display: grid; place-items: center; height: 130px; background: var(--papel); border: 1px solid var(--linha); }}
.erro-img i {{ position: absolute; top: 8px; right: 12px; font-style: normal; font-size: 20px; color: var(--alerta); }}
.erro p {{ font-size: 14px; margin-top: 10px; }}
footer {{ padding-block: 72px 72px; color: var(--grafite); font-size: 13px; }}
footer .in {{ border-top: 1px solid var(--facho); padding-top: 18px; }}
</style>

<header class="capa"><div class="in">
  <p class="rot">Manual de marca · versão 3 · 23 de novembro de 2026</p>
  <div class="marca">{logo("assinatura-negativa.svg", 92)}</div>
  <h1>Cada endereço, lido como <em>patrimônio</em>.</h1>
  <p class="lead">O Faro acompanha os prédios HIS e HMP de São Paulo e entrega, todo dia às 8h, o que mudou e onde está a oportunidade, com a discrição de um relatório privado.</p>
</div></header>

<main class="in">
  <section class="cap">
    <div class="cap-h"><p class="num">I</p><h2>Mais sofisticado, com cara de alto padrão</h2></div>
    <p>Esse foi o pedido em 23/11/2026. O Faro serve a quem investe, e a marca precisa ter o peso de quem cuida de patrimônio. Saem a grotesca pesada e o laranja de sinalização. Entram a serifa de alto contraste, o latão e o espaço vazio.</p>
    <div class="antes-agora">
      <div><div class="palco claro">{svg(V2 / "assinatura.svg", 52)}</div><p class="legenda">Antes · v2, grotesca e laranja</p></div>
      <div><div class="palco claro">{logo("assinatura.svg", 76)}</div><p class="legenda">Agora · v3, Bodoni, latão e verde</p></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="num">II</p><h2>O que o Behance mostrou no alto padrão</h2></div>
    <p>Dos 24 projetos da busca "real estate" (23/11/2026), 11 são sites de imóvel de luxo e boa parte das identidades usa serifa, versais espaçadas e cores de material. Estes quatro guiaram a nova versão:</p>
    <div class="grid4">{refs}</div>
    <div class="grid2" style="margin-top:28px">
      <div class="bloco"><h3>O que trouxemos</h3><ul class="lista"><li>Serifa de alto contraste no nome e nos números</li><li>Versais espaçadas, como letreiro de fachada</li><li>Cores de material, foscas</li><li>Fios finos e muito respiro</li></ul></div>
      <div class="bloco"><h3>O que evitamos</h3><ul class="lista"><li>Preto com dourado brilhante, o clichê do luxo</li><li>Degradê, folha metálica e brilho</li><li>Letra cursiva e brasão</li><li>Foto de mansão de banco de imagem</li></ul></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="num">III</p><h2>Endereço nobre: as cores vêm dos prédios de São Paulo</h2></div>
    <div class="materiais">
      <div class="material" style="background:#17302A;color:#F4EFE6"><b>Verde Jardim</b><span>O verde das copas dos Jardins, Jardim Europa e Jardim América.</span></div>
      <div class="material" style="background:#B08D57;color:#17302A"><b>Latão</b><span>As letras de metal na fachada e as ferragens dos prédios de alto padrão.</span></div>
      <div class="material" style="background:#EFEAE1;color:#17302A"><b>Travertino</b><span>A pedra dos halls de entrada, quente e clara.</span></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="num">IV</p><h2>O monograma: um F que acende</h2></div>
    <div class="grid2">
      <div class="palco claro" style="padding:20px">{svg(LOGO / "construcao.svg", 0, largura_auto=False)}</div>
      <div><h3>Construção</h3>
        <p>O F vem da Bodoni Moda, a mesma letra do nome. Da serifa superior sai um facho de latão, como a luz de um farol. O eixo do facho passa exatamente no centro dessa serifa, e as bordas do facho se encontram na serifa: a luz nasce da letra.</p>
        <p>O facho começa a 4% da altura da versal depois da serifa, mede 60% dessa altura e abre de 70 para 500 unidades, na proporção de 1 para 7.</p>
        <p>Área de proteção: um terço da altura da versal em volta de qualquer assinatura. Tamanho mínimo: 16 px para o favicon, 32 px de altura para a assinatura horizontal.</p></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="num">V</p><h2>Assinaturas</h2></div>
    <div class="grid2">
      <div><div class="palco claro">{logo("assinatura.svg", 70)}</div><p class="legenda">Principal · fundo claro</p></div>
      <div><div class="palco escuro">{logo("assinatura-negativa.svg", 70)}</div><p class="legenda">Negativa · verde Jardim</p></div>
      <div><div class="palco pedra">{logo("logotipo.svg", 34)}</div><p class="legenda">Logotipo · cabeçalho do e-mail e espaços estreitos</p></div>
      <div><div class="palco claro">{logo("assinatura-vertical.svg", 160)}</div><p class="legenda">Vertical · capas e telas quadradas</p></div>
    </div>
    <div class="bloco" style="margin-top:20px"><div class="icones">{logo("icone-app.svg", 128)}{logo("icone-app.svg", 64)}{logo("favicon.svg", 32)}{logo("favicon.svg", 16)}{logo("simbolo.svg", 70)}{logo("simbolo-mono.svg", 70)}</div>
      <p class="legenda">Ícone de app em selo com fio de latão · favicon · monograma · monograma em uma cor</p></div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="num">VI</p><h2>Paleta</h2></div>
    <p>Verde e latão fazem a marca; travertino e papel dão o fundo. O latão é fosco e aparece pouco: no facho, nos fios, nos marcadores e nos rótulos. Em texto pequeno, use o latão escuro.</p>
    <div class="grid4">{cores}</div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="num">VII</p><h2>Bodoni Moda e Jost</h2></div>
    <div class="grid2">
      <div class="bloco"><p class="rot">Nome, títulos e números · Bodoni Moda</p><p class="tipo-display">O que rolou ontem</p>
        <p class="numerais">R$ 383.636,74</p>
        <p>Didone de alto contraste, a letra das revistas e das marcas de luxo. Tem tamanho óptico: fica mais delicada nos títulos grandes e mais firme nos pequenos. Os números são o ponto forte, por isso ela vale também para os destaques do boletim. Acima, o teto de preço da HIS-2 em 2026.</p></div>
      <div class="bloco"><p class="rot">Texto e rótulos · Jost</p><p style="font-size:22px;font-weight:300;margin:10px 0 6px">Comprou por R$ 297.050 e revendeu por R$ 385.000.</p>
        <p class="rot" style="color:var(--grafite);margin-bottom:16px">Bela Vista · AP 304 · Matrícula 543.554</p>
        <p>Geométrica no espírito da Futura, clássica do mercado imobiliário. No texto, peso leve; nos rótulos, versais pequenas com espaçamento largo.</p>
        <div class="escala"><div><span class="rot">64</span><span class="serif" style="font-size:44px;line-height:1">Herói</span></div><div><span class="rot">44</span><span class="serif" style="font-size:32px">Título</span></div><div><span class="rot">28</span><span class="serif" style="font-size:24px">Seção</span></div><div><span class="rot">16</span><span style="font-weight:300">Texto corrido do boletim</span></div><div><span class="rot">11</span><span class="rot" style="color:var(--grafite)">Rótulo editorial</span></div></div></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="num">VIII</p><h2>As peças do boletim</h2></div>
    <div class="grid3">
      <div class="bloco"><p class="rot">Herói numérico</p><p class="comp-num" style="margin:14px 0 10px">5.250</p><p class="rot" style="color:var(--grafite)">prédios HIS/HMP</p></div>
      <div class="bloco"><p class="rot secao-rot"><b>II</b> · Oportunidades do dia</p><div class="item"><i></i><span><span class="t">Rua Frei Caneca, 651</span><br><span class="c">Bela Vista · AP 304</span><br><a class="a" href="#">Ver contatos →</a></span><span class="d"><b>+20%</b><span>acima da inflação</span></span></div></div>
      <div class="bloco"><p class="rot">Ações e estados</p><div class="acoes" style="margin-top:14px"><a class="btn prim" href="#">Abrir o Faro →</a><a class="btn sec" href="#">Achar quem vende</a></div>
        <span class="chip" style="background:var(--ganho-fundo);color:var(--ganho)">+8% acima da inflação</span><span class="chip" style="background:var(--alerta-fundo);color:var(--alerta)">acima do teto</span><span class="chip" style="background:var(--pedra)">142 unidades</span></div>
    </div>
    <p style="margin-top:18px">As seções do boletim usam numeral romano (I, II, III) em Bodoni e o título em versais de Jost. O marcador de cada item é um losango de latão.</p>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="num">IX</p><h2>O boletim das 8h e o site</h2></div>
    <div class="aplic">
      <div><img src="img/app_email.jpg" alt="E-mail do boletim diário Faro na versão 3"><p class="legenda">E-mail diário · só HTML e texto, abre igual com imagens bloqueadas</p></div>
      <div><div class="telefone"><img src="img/app_site.jpg" alt="Site Faro no celular, versão 3"></div><p class="legenda" style="text-align:center">Site no celular · boletim, mapa e fichas com contatos</p></div>
    </div>
  </section>

  <section class="cap">
    <div class="cap-h"><p class="num">X</p><h2>O que não fazer</h2></div>
    <div class="grid4">{erros_html}</div>
  </section>
</main>
<footer><div class="in">Faro · manual de marca, versão 3. Fontes Bodoni Moda e Jost (licença OFL, uso comercial livre). As referências são projetos públicos do Behance, citados com link para os autores; nenhuma imagem deles foi reproduzida. A versão 2 está guardada em 03_BRAND_IDENTITY/arquivo/faro-v2. O nome ainda depende de busca no INPI.</div></footer>
"""
    (AQUI / "index.html").write_text(html, encoding="utf-8")
    print("manual gerado:", len(html), "bytes")


if __name__ == "__main__":
    main()
