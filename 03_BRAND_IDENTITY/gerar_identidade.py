#!/usr/bin/env python3
"""Gera os arquivos da marca Faro v3 (SVG com texto convertido em curvas).

Conceito "endereço nobre": o F de Faro em Bodoni, como as letras de latão na fachada dos prédios
de alto padrão de São Paulo, com um facho de luz de latão que sai da serifa superior. Paleta dos
materiais desses prédios: verde dos Jardins, latão dos letreiros e travertino do hall.

Uso:
  python3 gerar_identidade.py --fontes PASTA_COM_FONTSOURCE --saida faro/
Requer fonttools. Fontes: Bodoni Moda 500 e Jost 500 (licença OFL), pacotes @fontsource.
"""
import argparse
import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

COR = {"jardim": "#17302A", "latao": "#B08D57", "latao_escuro": "#7D5F38", "latao_claro": "#C9A878",
       "travertino": "#EFEAE1", "papel": "#FBF9F5", "grafite": "#5B625D", "linha": "#DDD5C7"}

# Facho em unidades da fonte (Bodoni Moda, 2000 por eme; versal F de x 57 a 1125, altura 1500).
# O eixo do facho passa no centro da serifa superior do F (y 1090 a 1500, centro 1295).
# Começa 60 unidades depois da serifa, tem 900 de comprimento e abre de 70 para 500 (1 para 7).
FACHO = [(1185, 1260), (2085, 1060), (2085, 1560), (1185, 1330)]
X0, X1, TOPO, VERSAL = 57, 2085, 1560, 1500


class Fonte:
    def __init__(self, caminho):
        self.f = TTFont(caminho)
        self.g = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm

    def glifo(self, ch):
        pen = SVGPathPen(self.g)
        self.g[self.cmap[ord(ch)]].draw(pen)
        return pen.getCommands()

    def texto(self, texto, x, base, corpo, rastreio=0.0):
        esc = corpo / self.upm
        pen = SVGPathPen(self.g)
        cur = 0.0
        for ch in texto:
            nome = self.cmap.get(ord(ch))
            if nome is None:
                continue
            gl = self.g[nome]
            gl.draw(TransformPen(pen, (esc, 0, 0, -esc, x + cur, base)))
            cur += gl.width * esc + rastreio * corpo
        return pen.getCommands(), cur - rastreio * corpo


def svg(w, h, corpo, titulo="Faro"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{titulo}">'
            f"<title>{titulo}</title>{corpo}</svg>\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True)
    ap.add_argument("--saida", default="faro")
    a = ap.parse_args()
    fontes, saida = pathlib.Path(a.fontes), pathlib.Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    bodoni = Fonte(next(fontes.glob("**/bodoni-moda-latin-500-normal.woff")))
    jost = Fonte(next(fontes.glob("**/jost-latin-500-normal.woff")))
    F = bodoni.glifo("F")
    facho = " ".join(f"{x},{y}" for x, y in FACHO)

    def mono(x, base, versal, cor_f, cor_l):
        """Monograma com a versal de altura `versal` px, canto esquerdo em x e linha de base em `base`."""
        s = versal / VERSAL
        return (f'<g transform="translate({x - X0 * s:.2f} {base:.2f}) scale({s:.5f} {-s:.5f})">'
                f'<path d="{F}" fill="{cor_f}"/><polygon points="{facho}" fill="{cor_l}"/></g>')

    def largura(versal):
        return (X1 - X0) * versal / VERSAL

    def altura(versal):
        return TOPO * versal / VERSAL

    arq = {}
    # Símbolo (monograma)
    v = 40
    for nome, f_, l_ in (("simbolo.svg", COR["jardim"], COR["latao"]), ("simbolo-negativo.svg", COR["travertino"], COR["latao_claro"]),
                         ("simbolo-mono.svg", COR["jardim"], COR["jardim"])):
        arq[nome] = svg(largura(v) + 8, altura(v) + 8, mono(4, 4 + altura(v), v, f_, l_))

    # Ícone de app: selo verde com fio de latão e o monograma
    v = 40
    arq["icone-app.svg"] = svg(96, 96, f'<rect width="96" height="96" rx="20" fill="{COR["jardim"]}"/>'
                               f'<rect x="8.5" y="8.5" width="79" height="79" rx="13" fill="none" stroke="{COR["latao_claro"]}" stroke-width="1"/>'
                               + mono((96 - largura(v)) / 2, (96 + altura(v)) / 2, v, COR["travertino"], COR["latao_claro"]))
    v = 22
    arq["favicon.svg"] = svg(48, 48, f'<rect width="48" height="48" rx="10" fill="{COR["jardim"]}"/>'
                             + mono((48 - largura(v)) / 2, (48 + altura(v)) / 2, v, COR["travertino"], COR["latao_claro"]))

    # Logotipo: FARO em versais espaçadas, como letreiro de fachada
    d, w = bodoni.texto("FARO", 2, 32, 40, rastreio=0.24)
    arq["logotipo.svg"] = svg(w + 4, 36, f'<path d="{d}" fill="{COR["jardim"]}"/>')
    arq["logotipo-negativo.svg"] = svg(w + 4, 36, f'<path d="{d}" fill="{COR["travertino"]}"/>')

    # Assinatura horizontal: monograma | fio de latão | FARO + descritor
    def horizontal(cor_f, cor_l, cor_fio, cor_desc, descritor=True):
        v = 40
        h = altura(v) + 12
        mx = largura(v)
        x_fio = mx + 17
        x_txt = x_fio + 17
        if descritor:
            d1, w1 = bodoni.texto("FARO", x_txt, 30, 32, rastreio=0.24)
            d2, w2 = jost.texto("INTELIGÊNCIA IMOBILIÁRIA", x_txt + 1, 45.5, 7.4, rastreio=0.42)
            partes = f'<path d="{d1}" fill="{cor_f}"/><path d="{d2}" fill="{cor_desc}"/>'
            w = max(w1, w2 + 1)
        else:
            d1, w = bodoni.texto("FARO", x_txt, 38, 32, rastreio=0.24)
            partes = f'<path d="{d1}" fill="{cor_f}"/>'
        corpo = (mono(0, 6 + altura(v), v, cor_f, cor_l) + f'<rect x="{x_fio:.2f}" y="6" width="0.8" height="{altura(v):.2f}" fill="{cor_fio}"/>' + partes)
        return svg(x_txt + w + 2, h, corpo)

    arq["assinatura.svg"] = horizontal(COR["jardim"], COR["latao"], COR["latao"], COR["latao_escuro"])
    arq["assinatura-negativa.svg"] = horizontal(COR["travertino"], COR["latao_claro"], COR["latao_claro"], COR["latao_claro"])
    arq["assinatura-mono.svg"] = horizontal(COR["jardim"], COR["jardim"], COR["jardim"], COR["jardim"])
    arq["assinatura-sem-descritor.svg"] = horizontal(COR["jardim"], COR["latao"], COR["latao"], COR["latao_escuro"], descritor=False)
    arq["assinatura-sem-descritor-negativa.svg"] = horizontal(COR["travertino"], COR["latao_claro"], COR["latao_claro"], COR["latao_claro"], descritor=False)

    # Assinatura vertical (capas, telas quadradas)
    v = 64
    d1, w1 = bodoni.texto("FARO", 0, 0, 40, rastreio=0.24)
    d2, w2 = jost.texto("INTELIGÊNCIA IMOBILIÁRIA", 0, 0, 8.4, rastreio=0.42)
    W = max(w1, w2, largura(v)) + 8
    arq["assinatura-vertical.svg"] = svg(W, altura(v) + 84,
                                         mono((W - largura(v)) / 2, 4 + altura(v), v, COR["jardim"], COR["latao"]) +
                                         f'<g transform="translate({(W - w1) / 2:.2f} {altura(v) + 58:.2f})"><path d="{d1}" fill="{COR["jardim"]}"/></g>'
                                         f'<g transform="translate({(W - w2) / 2:.2f} {altura(v) + 78:.2f})"><path d="{d2}" fill="{COR["latao_escuro"]}"/></g>')

    # Folha de construção (unidades da fonte / 6,25 = px)
    k = 1 / 6.25
    W = 520
    def px(x, y):
        return 24 + (x - X0) * k, 300 - y * k
    guias = []
    for y, rot in ((0, "linha de base"), (VERSAL, "altura das versais"), (1295, "eixo do facho: centro da serifa")):
        _, yy = px(0, y)
        guias.append(f'<line x1="0" y1="{yy:.1f}" x2="{W}" y2="{yy:.1f}" stroke="{COR["latao"]}" stroke-width=".6" stroke-dasharray="3 3"/>'
                     f'<text x="362" y="{yy - 5:.1f}" font-family="sans-serif" font-size="9" fill="{COR["grafite"]}">{rot}</text>')
    for x in (1125, 1185, 2085):
        xx, _ = px(x, 0)
        guias.append(f'<line x1="{xx:.1f}" y1="20" x2="{xx:.1f}" y2="312" stroke="{COR["linha"]}" stroke-width=".6"/>')
    # as bordas do facho convergem num ponto dentro da serifa do F: a luz nasce da letra
    ax, ay = 1038.5, 1292.6
    for (x1, y1) in ((2085, 1560), (2085, 1060)):
        a1, b1 = px(ax, ay); a2, b2 = px(x1, y1)
        guias.append(f'<line x1="{a1:.1f}" y1="{b1:.1f}" x2="{a2:.1f}" y2="{b2:.1f}" stroke="{COR["latao_escuro"]}" stroke-width=".7" stroke-dasharray="2 2"/>')
    a1, b1 = px(ax, ay)
    guias.append(f'<circle cx="{a1:.1f}" cy="{b1:.1f}" r="3" fill="none" stroke="{COR["latao_escuro"]}" stroke-width=".8"/>')
    nota = lambda y, t: f'<text x="24" y="{y}" font-family="sans-serif" font-size="9" fill="{COR["grafite"]}">{t}</text>'
    corpo = (f'<rect width="{W}" height="352" fill="{COR["papel"]}"/>' + mono(24, 300, VERSAL * k, COR["jardim"], COR["latao"]) + "".join(guias) +
             nota(330, "Facho: começa a 4% da versal depois da serifa, mede 60% da versal e abre de 70 para 500 unidades (1 para 7).") +
             nota(344, "As bordas do facho se encontram na serifa do F. Área de proteção: um terço da altura da versal."))
    arq["construcao.svg"] = svg(W, 352, corpo)
    for nome, conteudo in arq.items():
        (saida / nome).write_text(conteudo, encoding="utf-8")
        print(nome)


if __name__ == "__main__":
    main()
