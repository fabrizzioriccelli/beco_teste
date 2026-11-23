#!/usr/bin/env python3
"""Gera os arquivos da marca Faro (SVG com texto convertido em curvas e PNGs).

Conceito "facho": o F de Faro é desenhado como a haste de um farol (Tinta) com um facho de luz
(laranja Facho) que sai dela e se abre. "Ter faro" é ter instinto para a oportunidade; o facho é
o que encontra o imóvel certo antes dos outros. Grade de construção 48 x 48.

Uso:
  python3 gerar_identidade.py --fontes PASTA_COM_FONTSOURCE --saida faro/
Requer fonttools. Fontes: Schibsted Grotesk 900 e JetBrains Mono 500 (licença OFL).
"""
import argparse
import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

COR = {"tinta": "#0F1E46", "facho": "#FF5A1F", "nevoa": "#D9E4F5", "gelo": "#F5F7FB", "papel": "#FFFFFF", "grafite": "#4B5875"}

# Geometria do símbolo na grade 48 x 48
HASTE = (6, 6, 11, 36)                         # x, y, largura, altura
FACHO = [(19, 10.5), (46, 1), (46, 20), (19, 15.5)]  # separado da haste por 2: luz que sai do farol, abre de 5 para 19
BRACO = (17, 23, 16, 8)
PROTECAO = 8                                   # área de proteção = altura do braço


def simbolo(cor_haste, cor_facho, x=0.0, y=0.0, s=1.0):
    hx, hy, hw, hh = HASTE
    bx, by, bw, bh = BRACO
    pts = " ".join(f"{x + px * s:.2f},{y + py * s:.2f}" for px, py in FACHO)
    return (f'<rect x="{x + hx * s:.2f}" y="{y + hy * s:.2f}" width="{hw * s:.2f}" height="{hh * s:.2f}" fill="{cor_haste}"/>'
            f'<polygon points="{pts}" fill="{cor_facho}"/>'
            f'<rect x="{x + bx * s:.2f}" y="{y + by * s:.2f}" width="{bw * s:.2f}" height="{bh * s:.2f}" fill="{cor_haste}"/>')


class Texto:
    def __init__(self, caminho):
        self.fonte = TTFont(caminho)
        self.glifos = self.fonte.getGlyphSet()
        self.cmap = self.fonte.getBestCmap()
        self.upm = self.fonte["head"].unitsPerEm

    def caminho(self, texto, x, linha_base, corpo, rastreio=0.0):
        esc = corpo / self.upm
        pen = SVGPathPen(self.glifos)
        cursor = 0.0
        for ch in texto:
            nome = self.cmap.get(ord(ch))
            if nome is None:
                continue
            g = self.glifos[nome]
            g.draw(TransformPen(pen, (esc, 0, 0, -esc, x + cursor, linha_base)))
            cursor += g.width * esc + rastreio * corpo
        return pen.getCommands(), cursor - rastreio * corpo


def svg(w, h, corpo, titulo="Faro"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{titulo}">'
            f"<title>{titulo}</title>{corpo}</svg>\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True)
    ap.add_argument("--saida", default="faro")
    a = ap.parse_args()
    fontes, saida = pathlib.Path(a.fontes), pathlib.Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    marca = Texto(next(fontes.glob("**/schibsted-grotesk-latin-900-normal.woff")))
    apoio = Texto(next(fontes.glob("**/jetbrains-mono-latin-500-normal.woff")))

    arq = {}
    arq["simbolo.svg"] = svg(48, 48, simbolo(COR["tinta"], COR["facho"]))
    arq["simbolo-negativo.svg"] = svg(48, 48, simbolo(COR["papel"], COR["facho"]))
    arq["simbolo-mono.svg"] = svg(48, 48, simbolo(COR["tinta"], COR["tinta"]))
    arq["favicon.svg"] = svg(48, 48, f'<rect width="48" height="48" rx="10" fill="{COR["tinta"]}"/>' + simbolo(COR["papel"], COR["facho"], 4, 4, 0.84))
    arq["icone-app.svg"] = svg(96, 96, f'<rect width="96" height="96" rx="22" fill="{COR["tinta"]}"/>' + simbolo(COR["papel"], COR["facho"], 20, 20, 1.15))

    def horizontal(cor_texto, cor_haste, cor_facho, cor_tag=None):
        d, largura = marca.caminho("faro", 48 + 10, 41, 50, rastreio=-0.035)
        partes = [simbolo(cor_haste, cor_facho), f'<path d="{d}" fill="{cor_texto}"/>']
        total = 48 + 10 + largura
        if cor_tag:
            d2, l2 = apoio.caminho("INTELIGÊNCIA IMOBILIÁRIA", total + 16, 30, 9, rastreio=0.14)
            partes.append(f'<path d="{d2}" fill="{cor_tag}"/>')
            total += 16 + l2
        return svg(total + 2, 48, "".join(partes))

    arq["assinatura.svg"] = horizontal(COR["tinta"], COR["tinta"], COR["facho"])
    arq["assinatura-negativa.svg"] = horizontal(COR["papel"], COR["papel"], COR["facho"])
    arq["assinatura-mono.svg"] = horizontal(COR["tinta"], COR["tinta"], COR["tinta"])
    arq["assinatura-com-descritor.svg"] = horizontal(COR["tinta"], COR["tinta"], COR["facho"], COR["grafite"])

    d, largura = marca.caminho("faro", 0, 0, 44, rastreio=-0.035)
    w = max(largura, 84)
    arq["assinatura-vertical.svg"] = svg(w + 2, 128, simbolo(COR["tinta"], COR["facho"], (w - 72) / 2, 0, 1.5) +
                                         f'<g transform="translate({(w - largura) / 2:.2f} 118)"><path d="{d}" fill="{COR["tinta"]}"/></g>')

    # Folha de construção
    grade = "".join(f'<line x1="{i * 6}" y1="0" x2="{i * 6}" y2="288" stroke="#D5DCE8" stroke-width=".5"/>'
                    f'<line x1="0" y1="{i * 6}" x2="288" y2="{i * 6}" stroke="#D5DCE8" stroke-width=".5"/>' for i in range(49))
    raios = (f'<line x1="{17 * 6}" y1="{12.5 * 6}" x2="288" y2="{-1 * 6}" stroke="{COR["facho"]}" stroke-dasharray="4 4" stroke-width="1"/>'
             f'<line x1="{17 * 6}" y1="{12.5 * 6}" x2="288" y2="{23 * 6}" stroke="{COR["facho"]}" stroke-dasharray="4 4" stroke-width="1"/>'
             f'<circle cx="{17 * 6}" cy="{12.5 * 6}" r="4" fill="none" stroke="{COR["facho"]}"/>')
    nota = lambda x, y, t: f'<text x="{x}" y="{y}" font-family="monospace" font-size="10" fill="{COR["grafite"]}">{t}</text>'
    arq["construcao.svg"] = svg(288, 318, f'<rect width="288" height="318" fill="{COR["papel"]}"/>{grade}' + simbolo(COR["tinta"], COR["facho"], 0, 0, 6) + raios +
                                nota(4, 304, "haste 11 · rua de 2 · facho abre de 5 para 19 · braço 16 x 8") + nota(4, 316, "foco do facho no centro da haste · proteção = 8"))
    for nome, conteudo in arq.items():
        (saida / nome).write_text(conteudo, encoding="utf-8")
        print(nome)


if __name__ == "__main__":
    main()
