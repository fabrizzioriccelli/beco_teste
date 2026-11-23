#!/usr/bin/env python3
"""Gera os arquivos da marca Faro v4 (SVG com texto convertido em curvas).

Conceito "a luz acesa": o logotipo é a palavra faro em Inter Tight Semibold, minimalista, e o miolo
do "o" é uma luz quente, como a lâmpada de um farol ou uma janela acesa à noite. É o único ponto de
cor da marca. O ícone de app é a mesma luz num quadrado escuro, no estilo dos ícones de vidro
do iOS 26.

O texto corrido do site e do e-mail usa a fonte do sistema (SF Pro nos aparelhos Apple). O logo não
usa SF porque a licença da Apple não permite usar a fonte em logotipos nem embuti-la na web.

Uso:
  python3 gerar_identidade.py --fontes PASTA_COM_FONTSOURCE --saida faro/
Requer fonttools. Fonte: Inter Tight 600 (licença OFL), pacote @fontsource/inter-tight.
"""
import argparse
import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

COR = {"tinta": "#1D1D1F", "branco": "#FFFFFF", "noite": "#0A0C10", "noite_2": "#1B2029", "grafite": "#6E6E73", "linha": "#D2D2D7"}
# luz de sódio: do centro claro para a borda âmbar
LUZ = [("0", "#FFFBF4"), ("0.6", "#FFE3BC"), ("1", "#FFC888")]

# miolo do "o" na Inter Tight 600 (unidades da fonte, 2048 por eme): x 316 a 852, y 190 a 920
MIOLO = (584, 555, 292, 386)          # cx, cy, rx, ry (um pouco maior que o miolo: a borda fica sob o anel)
RASTREIO = -0.035


class Fonte:
    def __init__(self, caminho):
        self.f = TTFont(caminho)
        self.g = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm

    def texto(self, texto, x, base, corpo, rastreio=0.0):
        """Devolve o caminho SVG, a largura e a posição x (em px) de cada letra."""
        esc = corpo / self.upm
        pen = SVGPathPen(self.g)
        cur, pos = 0.0, []
        for ch in texto:
            gl = self.g[self.cmap[ord(ch)]]
            pos.append(x + cur)
            gl.draw(TransformPen(pen, (esc, 0, 0, -esc, x + cur, base)))
            cur += gl.width * esc + rastreio * corpo
        return pen.getCommands(), cur - rastreio * corpo, pos


def gradiente(id_):
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in LUZ)
    return f'<radialGradient id="{id_}" cx="0.5" cy="0.42" r="0.62">{stops}</radialGradient>'


def svg(w, h, corpo, titulo="Faro", defs=""):
    d = f"<defs>{defs}</defs>" if defs else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{titulo}">'
            f"<title>{titulo}</title>{d}{corpo}</svg>\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True)
    ap.add_argument("--saida", default="faro")
    a = ap.parse_args()
    fontes, saida = pathlib.Path(a.fontes), pathlib.Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    inter = Fonte(next(fontes.glob("**/inter-tight-latin-600-normal.woff")))

    def logotipo(cor, luz=True, corpo=56, margem=4, gid="luz"):
        esc = corpo / inter.upm
        base = margem + 1560 * esc           # altura do f
        d, w, pos = inter.texto("faro", margem, base, corpo, RASTREIO)
        cx, cy, rx, ry = MIOLO
        luz_svg = ""
        if luz:
            luz_svg = (f'<ellipse cx="{pos[3] + cx * esc:.2f}" cy="{base - cy * esc:.2f}" rx="{rx * esc:.2f}" ry="{ry * esc:.2f}" fill="url(#{gid})"/>')
        return svg(w + 2 * margem, base + 22 * esc + margem, luz_svg + f'<path d="{d}" fill="{cor}"/>', defs=gradiente(gid) if luz else "")

    arq = {
        "logotipo.svg": logotipo(COR["tinta"]),
        "logotipo-negativo.svg": logotipo(COR["branco"]),
        "logotipo-mono.svg": logotipo(COR["tinta"], luz=False),
        "logotipo-mono-negativo.svg": logotipo(COR["branco"], luz=False),
    }

    # Símbolo: o "o" aceso
    def simbolo(cor, tamanho=48, fundo=None, raio=0, gid="luz"):
        corpo = tamanho * 0.86 * inter.upm / 1154      # altura do "o" ocupa ~86% do quadro
        esc = corpo / inter.upm
        larg_o = (1120 - 49) * esc
        alt_o = (1132 + 22) * esc
        x0 = (tamanho - larg_o) / 2 - 49 * esc
        base = (tamanho + alt_o) / 2 - 22 * esc
        d, _, _ = inter.texto("o", x0, base, corpo)
        cx, cy, rx, ry = MIOLO
        partes = ""
        if fundo:
            partes += fundo
        partes += f'<ellipse cx="{x0 + cx * esc:.2f}" cy="{base - cy * esc:.2f}" rx="{rx * esc:.2f}" ry="{ry * esc:.2f}" fill="url(#{gid})"/>'
        partes += f'<path d="{d}" fill="{cor}"/>'
        return partes

    arq["simbolo.svg"] = svg(48, 48, simbolo(COR["tinta"]), defs=gradiente("luz"))
    arq["simbolo-negativo.svg"] = svg(48, 48, simbolo(COR["branco"]), defs=gradiente("luz"))

    # Ícone de app: quadrado escuro com o "o" de vidro e a luz dentro (estilo iOS 26)
    def icone(t, rx):
        defs = (gradiente("luz") +
                f'<linearGradient id="fundo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{COR["noite_2"]}"/><stop offset="1" stop-color="{COR["noite"]}"/></linearGradient>'
                '<linearGradient id="vidro" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".98"/><stop offset=".5" stop-color="#E6E8EE" stop-opacity=".92"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".75"/></linearGradient>'
                '<radialGradient id="brilho" cx=".5" cy=".55" r=".5"><stop offset="0" stop-color="#FFC888" stop-opacity=".35"/><stop offset="1" stop-color="#FFC888" stop-opacity="0"/></radialGradient>')
        fundo = (f'<rect width="{t}" height="{t}" rx="{rx}" fill="url(#fundo)"/>'
                 f'<circle cx="{t / 2}" cy="{t / 2}" r="{t * .42}" fill="url(#brilho)"/>'
                 f'<rect x=".5" y=".5" width="{t - 1}" height="{t - 1}" rx="{rx - .5}" fill="none" stroke="#FFFFFF" stroke-opacity=".14"/>')
        marca = f'<g transform="translate({t * .19:.2f} {t * .19:.2f})">' + simbolo("url(#vidro)", t * 0.62, gid="luz") + "</g>"
        return svg(t, t, fundo + marca, defs=defs)

    arq["icone-app.svg"] = icone(96, 21.5)
    arq["favicon.svg"] = icone(48, 11)

    # Folha de construção: logotipo grande com a altura-x, o miolo e a luz
    corpo = 160
    esc = corpo / inter.upm
    m = 24
    base = m + 1560 * esc
    d, w, pos = inter.texto("faro", m, base, corpo, RASTREIO)
    cx, cy, rx, ry = MIOLO
    W, H = max(w + 2 * m, 700), base + 70
    guias = []
    for y, rot in ((0, "linha de base"), (1118, "altura-x"), (1560, "ascendente do f")):
        yy = base - y * esc
        guias.append(f'<line x1="0" y1="{yy:.1f}" x2="{W:.1f}" y2="{yy:.1f}" stroke="#86868B" stroke-width=".6" stroke-dasharray="3 3"/>'
                     f'<text x="{W - 6:.1f}" y="{yy - 5:.1f}" text-anchor="end" font-family="sans-serif" font-size="9" fill="{COR["grafite"]}">{rot}</text>')
    ox, oy = pos[3] + cx * esc, base - cy * esc
    guias.append(f'<line x1="{ox:.1f}" y1="{oy - ry * esc - 16:.1f}" x2="{ox:.1f}" y2="{oy + ry * esc + 16:.1f}" stroke="#F08A2C" stroke-width=".6"/>'
                 f'<line x1="{ox - rx * esc - 16:.1f}" y1="{oy:.1f}" x2="{ox + rx * esc + 16:.1f}" y2="{oy:.1f}" stroke="#F08A2C" stroke-width=".6"/>')
    nota = f'<text x="{m}" y="{H - 24:.1f}" font-family="sans-serif" font-size="10" fill="{COR["grafite"]}">Inter Tight Semibold, rastreio −3,5%. A luz ocupa o miolo do "o" e passa 5% por baixo do anel.</text>'
    nota += f'<text x="{m}" y="{H - 10:.1f}" font-family="sans-serif" font-size="10" fill="{COR["grafite"]}">Área de proteção: a altura-x em volta do logotipo. Mínimo: 18 px de altura.</text>'
    arq["construcao.svg"] = svg(W, H, f'<rect width="{W:.1f}" height="{H:.1f}" fill="#FFFFFF"/>' + "".join(guias) +
                                f'<ellipse cx="{ox:.2f}" cy="{oy:.2f}" rx="{rx * esc:.2f}" ry="{ry * esc:.2f}" fill="url(#luz)"/><path d="{d}" fill="{COR["tinta"]}"/>' + nota,
                                defs=gradiente("luz"))
    for nome, conteudo in arq.items():
        (saida / nome).write_text(conteudo, encoding="utf-8")
        print(nome)


if __name__ == "__main__":
    main()
