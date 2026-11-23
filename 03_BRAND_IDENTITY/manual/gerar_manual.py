#!/usr/bin/env python3
"""Gera o manual da marca Faro v5 (manual/index.html) com os SVGs oficiais embutidos.

Página de visual único: capa escura com a cidade acesa e corpo branco. As imagens ficam em img/
(cidade.jpg: a cidade acesa sem marcações; email.jpg: prévia do boletim)."""
import pathlib
import re

AQUI = pathlib.Path(__file__).resolve().parent
LOGO = AQUI.parent / "faro"


def svg(nome, estilo="", cor=None, extra=""):
    s = (LOGO / nome).read_text(encoding="utf-8").strip()
    s = re.sub(r' width="[\d.]+" height="[\d.]+"', f' style="{estilo}" {extra}', s, count=1)
    if cor:
        s = s.replace('fill="#0B0B0C"', f'fill="{cor}"')
    return s


def main():
    marca = svg("logotipo.svg", "height:1em;width:auto;display:block", "currentColor")
    marca_aco = svg("logotipo.svg", "height:1em;width:auto;display:block;filter:drop-shadow(5px 9px 6px rgb(0 0 0 / .28)) drop-shadow(1px 1px 0 rgb(255 255 255 / .45))",
                    "url(#aco)").replace("<title>Faro</title>", '<title>Faro</title><defs><linearGradient id="aco" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#48484A"/><stop offset=".55" stop-color="#141416"/><stop offset="1" stop-color="#2C2C2E"/></linearGradient></defs>')
    assinatura = svg("assinatura.svg", "width:min(360px,80%);height:auto;display:block")
    assinatura_neg = svg("assinatura-negativa.svg", "width:min(360px,80%);height:auto;display:block")
    icone = svg("icone-app.svg", "width:96px;height:96px;display:block;border-radius:22px")
    favicon = svg("favicon.svg", "width:32px;height:32px;display:block")
    construcao = svg("construcao.svg", "width:100%;height:auto;display:block")

    html = f"""<title>Marca Faro</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&display=swap">
<style>
/* Layout: capa escura com a cidade acesa e o nome; corpo branco com seções curtas e muito respiro. Visual único (não muda com o tema). */
:root {{ --preto: #0B0B0C; --branco: #FFFFFF; --pedra: #F4F3F1; --fundo: #F5F5F7; --grafite: #3A3A3C; --cinza: #8E8E93; --texto-2: #6E6E73; --linha: #E5E5EA; --noite: #06080B;
  --fonte: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Geist", "Helvetica Neue", Arial, sans-serif;
  --fonte-titulo: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Geist", "Helvetica Neue", Arial, sans-serif;
  --fonte-marca: "Geist", "Helvetica Neue", Arial, sans-serif; color-scheme: light; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--branco); color: var(--preto); font-family: var(--fonte); font-size: 17px; line-height: 1.5; -webkit-font-smoothing: antialiased; }}
.in {{ max-width: 1200px; margin: 0 auto; padding-left: max(20px, env(safe-area-inset-left, 0px)); padding-right: max(20px, env(safe-area-inset-right, 0px)); }}
.capa {{ position: relative; min-height: 640px; background: var(--noite) url(img/cidade.jpg) center / cover; color: var(--branco); display: grid; place-items: center; overflow: hidden; }}
.capa::after {{ content: ""; position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 50%, rgb(6 8 11 / .15), rgb(6 8 11 / .7)); }}
.capa .meio {{ position: relative; z-index: 1; display: grid; gap: 26px; justify-items: center; text-align: center; padding: 80px 20px; }}
.capa .meio svg {{ font-size: clamp(44px, 10vw, 120px); }}
.rot {{ font-family: var(--fonte-marca); font-size: 12px; letter-spacing: .36em; text-transform: uppercase; }}
.capa .rot {{ opacity: .72; }}
.capa .rod {{ position: absolute; z-index: 1; left: 0; right: 0; bottom: 24px; display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; font-size: 13px; color: rgb(255 255 255 / .6); }}
section {{ padding-top: 96px; }}
h2 {{ font-family: var(--fonte-marca); font-weight: 500; font-size: 12px; letter-spacing: .3em; text-transform: uppercase; color: var(--cinza); margin: 0 0 24px; }}
h3 {{ font-family: var(--fonte-titulo); font-weight: 600; font-size: clamp(28px, 4vw, 40px); letter-spacing: -.03em; line-height: 1.08; margin: 0 0 14px; max-width: 22ch; text-wrap: balance; }}
p {{ margin: 0 0 12px; max-width: 62ch; color: var(--grafite); }}
.g3 {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }}
.g2 {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }}
.g21 {{ display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr); gap: 14px; }}
@media (max-width: 820px) {{ .g3, .g2, .g21 {{ grid-template-columns: minmax(0, 1fr); }} }}
.painel {{ min-height: 300px; border-radius: 6px; display: grid; place-items: center; position: relative; padding: 32px; }}
.painel i {{ position: absolute; left: 16px; bottom: 12px; font-style: normal; font-size: 11px; letter-spacing: .2em; text-transform: uppercase; opacity: .5; }}
.painel .so svg {{ font-size: clamp(30px, 5vw, 56px); }}
.parede {{ min-height: 460px; border-radius: 6px; background: linear-gradient(180deg, #E9E6E1, #D9D5CF); position: relative; overflow: hidden; display: grid; place-items: center; }}
.parede::before {{ content: ""; position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgb(0 0 0 / .035) 0 1px, transparent 1px 130px), repeating-linear-gradient(90deg, rgb(0 0 0 / .035) 0 1px, transparent 1px 260px); }}
.parede::after {{ content: ""; position: absolute; inset: 0; background: radial-gradient(ellipse at 20% 0%, rgb(255 255 255 / .55), transparent 60%), linear-gradient(90deg, transparent 70%, rgb(0 0 0 / .08)); }}
.parede .placa {{ position: relative; z-index: 1; font-size: clamp(40px, 7vw, 84px); }}
.mesa {{ min-height: 460px; border-radius: 6px; background: #CFCAC3; position: relative; overflow: hidden; }}
.mesa::before {{ content: ""; position: absolute; inset: 0; background: radial-gradient(rgb(0 0 0 / .06) 1px, transparent 1.3px) 0 0 / 6px 6px, radial-gradient(ellipse at 30% 10%, rgb(255 255 255 / .5), transparent 60%); }}
.cart {{ position: absolute; width: min(280px, 64%); aspect-ratio: 85 / 55; border-radius: 3px; box-shadow: 0 30px 40px -10px rgb(0 0 0 / .35), 0 2px 4px rgb(0 0 0 / .2); display: grid; place-items: center; }}
.cart.a {{ background: var(--preto); color: var(--branco); left: 8%; top: 12%; transform: rotate(-8deg); }} .cart.a svg {{ font-size: 22px; }}
.cart.b {{ background: #FAFAF8; left: 28%; top: 50%; transform: rotate(5deg); place-items: stretch; padding: 20px 22px; }}
.cart.b b {{ font-weight: 600; font-size: 15px; display: block; }} .cart.b span {{ font-size: 11px; color: var(--texto-2); display: block; margin-top: 2px; }} .cart.b .ass {{ align-self: end; font-size: 9px; }}
.tela {{ border-radius: 6px; background: var(--pedra); display: grid; place-items: center; padding: 40px 20px; overflow: hidden; }}
.mac {{ width: 100%; max-width: 760px; border-radius: 18px; background: #1C1C1E; padding: 10px; box-shadow: 0 40px 60px -20px rgb(0 0 0 / .35); }}
.site {{ aspect-ratio: 16 / 10; border-radius: 9px; overflow: hidden; position: relative; background: var(--noite) url(img/cidade.jpg) 50% 40% / cover; color: #fff; }}
.site::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgb(6 8 11 / .8), rgb(6 8 11 / .15) 45%, rgb(6 8 11 / .8)); }}
.site > * {{ position: absolute; z-index: 1; }}
.vidro {{ background: rgb(255 255 255 / .1); -webkit-backdrop-filter: blur(20px) saturate(160%); backdrop-filter: blur(20px) saturate(160%); border: 1px solid rgb(255 255 255 / .18); box-shadow: inset 0 1px 0 rgb(255 255 255 / .25); }}
.nav {{ top: 4%; left: 4%; right: 4%; height: 9%; min-height: 30px; border-radius: 999px; display: flex; align-items: center; justify-content: space-between; padding: 0 6px 0 4%; }}
.nav svg {{ font-size: 10px; }} .nav span {{ font-size: 11px; background: #F5F5F7; color: #000; border-radius: 999px; padding: 5px 11px; }}
.site h4 {{ left: 6%; top: 22%; margin: 0; font-family: var(--fonte-titulo); font-weight: 600; font-size: clamp(20px, 3.6vw, 44px); letter-spacing: -.03em; line-height: 1.02; }}
.tiles {{ left: 6%; right: 6%; bottom: 7%; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }}
.tiles div {{ border-radius: 14px; padding: 10px 12px; }} .tiles b {{ font-family: var(--fonte-titulo); font-weight: 600; font-size: clamp(16px, 2.6vw, 30px); display: block; letter-spacing: -.03em; }} .tiles span {{ font-size: 10px; color: rgb(235 235 245 / .62); }}
.fone {{ width: min(280px, 80%); aspect-ratio: 9 / 19; border-radius: 44px; background: var(--preto); padding: 9px; box-shadow: 0 40px 60px -20px rgb(0 0 0 / .4); }}
.fone .scr {{ height: 100%; border-radius: 36px; overflow: hidden; position: relative; background: var(--noite) url(img/cidade.jpg) 62% 50% / auto 120%; color: #fff; }}
.fone .hora {{ text-align: center; padding-top: 22%; font-family: var(--fonte-titulo); font-size: 58px; font-weight: 600; letter-spacing: -.02em; line-height: 1; }}
.fone .dia {{ text-align: center; font-size: 13px; opacity: .8; margin-top: 6px; }}
.notif {{ position: absolute; left: 8px; right: 8px; bottom: 22%; border-radius: 20px; padding: 11px 12px; display: grid; grid-template-columns: 32px 1fr; gap: 10px; align-items: center; }}
.notif .ico {{ width: 32px; height: 32px; border-radius: 8px; overflow: hidden; }} .notif .ico svg {{ width: 32px; height: 32px; }}
.notif b {{ font-size: 12px; display: block; }} .notif small {{ font-size: 11px; color: rgb(255 255 255 / .85); line-height: 1.3; display: block; }}
.email img {{ width: 100%; height: auto; display: block; border-radius: 6px; border: 1px solid var(--linha); }}
.paleta {{ display: grid; grid-template-columns: 2fr repeat(5, 1fr); min-height: 180px; border-radius: 6px; overflow: hidden; }}
@media (max-width: 820px) {{ .paleta {{ grid-template-columns: repeat(2, 1fr); }} }}
.paleta div {{ padding: 16px; display: flex; flex-direction: column; justify-content: flex-end; font-size: 12px; min-height: 90px; }} .paleta b {{ font-size: 14px; font-weight: 600; }}
.tipo > div {{ background: var(--pedra); border-radius: 6px; padding: 32px; }}
.tipo .t1 {{ font-family: var(--fonte-titulo); font-weight: 600; font-size: clamp(36px, 5vw, 60px); letter-spacing: -.03em; line-height: 1; margin-bottom: 18px; }}
.tipo .t2 {{ font-size: clamp(28px, 4vw, 52px); margin-bottom: 18px; }}
.regras {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }}
@media (max-width: 820px) {{ .regras {{ grid-template-columns: minmax(0, 1fr); }} }}
.regras div {{ background: var(--fundo); border-radius: 6px; padding: 24px; }} .regras b {{ display: block; font-size: 17px; margin-bottom: 6px; }} .regras p {{ font-size: 15px; margin: 0; }}
footer {{ padding: 96px 0 80px; color: var(--cinza); font-size: 13px; }}
</style>

<header class="capa">
  <div class="meio">{marca.replace('style="height:1em', 'style="color:#fff;height:1em')}<div class="rot">Inteligência imobiliária · São Paulo</div></div>
  <div class="rod in"><span>Cada luz é um prédio HIS/HMP com alvará. São 5.250.</span><span>Manual de marca · versão 5 · 23/11/2026</span></div>
</header>

<main class="in">
  <section>
    <h2>Logotipo</h2>
    <h3>Só o nome. Preto e branco.</h3>
    <p>FARO em Geist Light, maiúsculas com espaçamento largo. Não há símbolo nem cor de destaque: a marca é o nome e a imagem da cidade acesa. É o que fazem as marcas imobiliárias de alto padrão, e é o que deixa o Faro distante do clichê do luxo.</p>
    <div class="g3" style="margin-top:28px">
      <div class="painel" style="background:#fff;box-shadow:inset 0 0 0 1px var(--linha)">{assinatura}<i>Principal</i></div>
      <div class="painel" style="background:var(--preto);color:#fff">{assinatura_neg}<i>Negativo</i></div>
      <div class="painel" style="background:var(--pedra)"><div class="so">{marca}</div><i>Só o nome</i></div>
    </div>
    <div class="g2" style="margin-top:14px">
      <div class="painel" style="background:#fff;box-shadow:inset 0 0 0 1px var(--linha);padding:20px">{construcao}</div>
      <div class="painel" style="background:var(--pedra)"><div style="display:flex;gap:22px;align-items:end">{icone}{favicon}</div><i>Ícone de app e favicon: o F em Geist</i></div>
    </div>
  </section>

  <section>
    <h2>Aplicações</h2>
    <h3>A cidade é a fotografia.</h3>
    <p>A imagem da marca é São Paulo à noite vista de cima: cada luz é um prédio HIS/HMP com alvará, desenhado com os dados oficiais. No site ela acende na ordem dos alvarás; no e-mail, marca os imóveis do dia.</p>
    <div class="g21" style="margin-top:28px">
      <div class="parede"><div class="placa">{marca_aco}</div></div>
      <div class="mesa"><div class="cart a">{marca.replace('style="height:1em', 'style="color:#fff;height:1em')}</div><div class="cart b"><div><b>Diogo</b><span>Inteligência imobiliária</span><span>São Paulo</span></div><div class="ass">{marca}</div></div></div>
    </div>
    <div class="g2" style="margin-top:14px">
      <div class="tela"><div class="mac"><div class="site">
        <div class="nav vidro">{marca.replace('style="height:1em', 'style="color:#fff;height:1em')}<span>Perguntar</span></div>
        <h4>O que rolou<br>ontem.</h4>
        <div class="tiles"><div class="vidro"><b>4</b><span>alvarás novos</span></div><div class="vidro"><b>3</b><span>revendas</span></div><div class="vidro"><b>2</b><span>acima do teto</span></div></div>
      </div></div></div>
      <div class="tela"><div class="fone"><div class="scr"><div class="hora">8:00</div><div class="dia">terça-feira, 24 de novembro</div>
        <div class="notif vidro"><div class="ico">{icone.replace('width:96px;height:96px;display:block;border-radius:22px', 'width:32px;height:32px;display:block;border-radius:8px')}</div><div><b>Faro · O que rolou ontem</b><small>4 alvarás novos, 3 revendas e 2 vendas acima do teto. Toque para ver os contatos.</small></div></div></div></div></div>
    </div>
    <div class="g21 email" style="margin-top:14px">
      <img src="img/email.jpg" alt="Boletim diário Faro por e-mail: topo preto com a cidade acesa, números do dia e listas brancas" loading="lazy">
      <div style="padding:8px 4px"><h3 style="font-size:28px">O boletim das 8h</h3><p>Mesmo desenho do site, feito só com HTML para abrir igual no Gmail, no Outlook e no iPhone. A foto da cidade é gerada todo dia com os imóveis do boletim marcados. Com as imagens bloqueadas, o e-mail continua completo.</p></div>
    </div>
  </section>

  <section>
    <h2>Cor</h2>
    <h3>Preto, branco e a luz da cidade.</h3>
    <div class="paleta" style="margin-top:28px">
      <div style="background:var(--preto);color:#fff"><b>Preto</b>#0B0B0C</div><div style="background:#fff;box-shadow:inset 0 0 0 1px var(--linha)"><b>Branco</b>#FFFFFF</div>
      <div style="background:var(--pedra)"><b>Pedra</b>#F4F3F1</div><div style="background:var(--grafite);color:#fff"><b>Grafite</b>#3A3A3C</div>
      <div style="background:var(--cinza);color:#fff"><b>Cinza</b>#8E8E93</div><div style="background:#FFC888"><b>Luz</b>só na imagem</div>
    </div>
    <p style="margin-top:16px">Verde e vermelho aparecem só para dado (ganho acima da inflação, venda acima do teto), nas versões acessíveis das cores de sistema da Apple.</p>
  </section>

  <section>
    <h2>Tipografia</h2>
    <div class="g2 tipo">
      <div><div class="t1">O que rolou ontem.</div><p>SF Pro, a fonte do sistema da Apple, em todo o texto do site e do e-mail. O site chama a fonte do aparelho; nos que não são Apple, entra a Geist. A licença da SF não permite embuti-la nem usá-la no logo.</p></div>
      <div><div class="t2">{marca}</div><p>Geist Light em maiúsculas espaçadas, só no logotipo e em rótulos curtos. Licença OFL, uso livre.</p></div>
    </div>
  </section>

  <section>
    <h2>Interface</h2>
    <h3>Liquid Glass na navegação, nunca no conteúdo.</h3>
    <div class="regras" style="margin-top:28px">
      <div><b>Vidro só flutua</b><p>Barra do topo, controles e a ficha do imóvel são de vidro. Listas, cartões e números ficam em superfície sólida, como pede a Apple.</p></div>
      <div><b>Vidro claro sobre fundo rico</b><p>Os números do dia usam o vidro transparente sobre a cidade, com uma camada de escurecimento por trás para manter a leitura.</p></div>
      <div><b>Cantos concêntricos</b><p>Raio de dentro = raio de fora − margem: ficha com 28 px, blocos internos com 14 px e 14 px de margem.</p></div>
      <div><b>Acessibilidade</b><p>Com "reduzir transparência" ligado no aparelho, o vidro vira superfície sólida. Todo texto passa de 4,5:1 de contraste.</p></div>
    </div>
  </section>

  <section>
    <h2>Não fazer</h2>
    <div class="regras">
      <div><b>Não criar símbolo</b><p>Nada de círculo, casinha, F recortado ou pin. A marca é o nome.</p></div>
      <div><b>Não colorir o nome</b><p>FARO é sempre preto ou branco. A luz quente existe só na imagem da cidade.</p></div>
      <div><b>Não apertar o espaçamento</b><p>O espaço largo entre as letras é parte do desenho. Use os arquivos da pasta faro/.</p></div>
      <div><b>Não usar dourado, serifa de luxo ou foto de banco de imagem</b><p>É o clichê que a marca evita.</p></div>
    </div>
  </section>
</main>
<footer class="in">Faro · manual de marca, versão 5 (proposta aprovada em 23/11/2026). Fonte do logotipo: Geist (OFL). Referências: casos de identidade imobiliária do Behance (Manor, Zenith Nest, Nestus, Realm, Pratum, Livwrk, Landrx, Laken). Versões anteriores em 03_BRAND_IDENTITY/arquivo.</footer>
"""
    (AQUI / "index.html").write_text(html, encoding="utf-8")
    print("manual gerado:", len(html), "bytes")


if __name__ == "__main__":
    main()
