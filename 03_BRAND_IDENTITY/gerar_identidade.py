#!/usr/bin/env python3
"""Gera os arquivos do logo do Radar HIS (SVG com texto convertido em curvas).

Conceito "H de quadra": duas quadras (azul placa) e, entre elas, o lote encontrado
(amarelo faixa). Juntas formam um H, de HIS e de habitação. Grade de construção 48 x 48.

Uso:
  python3 gerar_identidade.py --fontes PASTA_COM_FONTSOURCE --saida logo/
Requer: fonttools. As fontes são Archivo (800) e IBM Plex Mono (500), licença OFL.
"""
import argparse
import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

COR = {
    "placa": "#1F3F8B", "faixa": "#F2B705", "asfalto": "#171C1B",
    "concreto": "#EFF0EC", "papel": "#FFFFFF", "placa_clara": "#9DB8F2",
}
GRADE = 48
QUADRA_ESQ = (0, 0, 15, 48)    # x, y, largura, altura
QUADRA_DIR = (33, 0, 15, 48)
LOTE = (17, 17, 14, 14)        # área de proteção do logo = 1 lote (14 unidades)


def simbolo(cor_quadra, cor_lote, x=0.0, y=0.0, escala=1.0, solido=False):
    s = escala
    rects = []
    for (rx, ry, rw, rh), cor in [(QUADRA_ESQ, cor_quadra), (QUADRA_DIR, cor_quadra), (LOTE, cor_lote)]:
        if solido and cor == cor_lote:  # versão favicon: sem ruas em volta do lote
            rx, rw = 15, 18
        rects.append(f'<rect x="{x + rx * s:.2f}" y="{y + ry * s:.2f}" width="{rw * s:.2f}" height="{rh * s:.2f}" fill="{cor}"/>')
    return "".join(rects)


class Texto:
    def __init__(self, caminho):
        self.fonte = TTFont(caminho)
        self.glifos = self.fonte.getGlyphSet()
        self.cmap = self.fonte.getBestCmap()
        self.upm = self.fonte["head"].unitsPerEm
        self.cap = getattr(self.fonte["OS/2"], "sCapHeight", 0) or int(self.upm * 0.7)

    def caminho(self, texto, x, linha_base, altura_cap, rastreio=0.0):
        """Path SVG do texto, com a altura das maiúsculas = altura_cap. Retorna (d, largura)."""
        esc = altura_cap / self.cap
        pen = SVGPathPen(self.glifos)
        cursor = 0.0
        for ch in texto:
            nome = self.cmap.get(ord(ch))
            if nome is None:
                continue
            g = self.glifos[nome]
            tp = TransformPen(pen, (esc, 0, 0, -esc, x + cursor, linha_base))
            g.draw(tp)
            cursor += g.width * esc + rastreio * altura_cap
        return pen.getCommands(), cursor - rastreio * altura_cap


def svg(w, h, corpo, titulo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{titulo}">'
            f"<title>{titulo}</title>{corpo}</svg>\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", required=True)
    ap.add_argument("--saida", default="logo")
    a = ap.parse_args()
    fontes, saida = pathlib.Path(a.fontes), pathlib.Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    marca = Texto(next(fontes.glob("**/archivo-latin-800-normal.woff")))
    apoio = Texto(next(fontes.glob("**/ibm-plex-mono-latin-500-normal.woff")))

    arquivos = {}
    # Símbolo (versão reduzida)
    arquivos["simbolo.svg"] = svg(48, 48, simbolo(COR["placa"], COR["faixa"]), "Radar HIS")
    arquivos["simbolo-negativo.svg"] = svg(48, 48, simbolo(COR["papel"], COR["faixa"]), "Radar HIS")
    arquivos["simbolo-mono.svg"] = svg(48, 48, simbolo(COR["asfalto"], COR["asfalto"]), "Radar HIS")
    arquivos["favicon.svg"] = svg(48, 48, simbolo(COR["placa"], COR["faixa"], solido=True), "Radar HIS")
    # Ícone de aplicativo: símbolo sobre placa, margem de 1 lote
    icone = f'<rect width="96" height="96" rx="20" fill="{COR["placa"]}"/>' + simbolo(COR["papel"], COR["faixa"], 24, 24, 1.0)
    arquivos["icone-app.svg"] = svg(96, 96, icone, "Radar HIS")

    # Assinatura horizontal: símbolo 48 de altura; maiúsculas com 26; tagline em mono
    def horizontal(cor_texto, cor_quadra, cor_lote, cor_apoio, tagline=True):
        d, largura = marca.caminho("Radar HIS", 48 + 14, 30, 26, rastreio=-0.01)
        partes = [simbolo(cor_quadra, cor_lote), f'<path d="{d}" fill="{cor_texto}"/>']
        larg_total = 48 + 14 + largura
        if tagline:
            d2, l2 = apoio.caminho("INTELIGÊNCIA HIS · SÃO PAULO", 48 + 14, 47, 8.2, rastreio=0.12)
            partes.append(f'<path d="{d2}" fill="{cor_apoio}"/>')
            larg_total = max(larg_total, 48 + 14 + l2)
        return svg(larg_total + 2, 48, "".join(partes), "Radar HIS")

    arquivos["assinatura-horizontal.svg"] = horizontal(COR["asfalto"], COR["placa"], COR["faixa"], "#59625F")
    arquivos["assinatura-horizontal-negativa.svg"] = horizontal(COR["papel"], COR["papel"], COR["faixa"], "#C9CEC8")
    arquivos["assinatura-horizontal-mono.svg"] = horizontal(COR["asfalto"], COR["asfalto"], COR["asfalto"], COR["asfalto"])
    arquivos["assinatura-horizontal-sem-tagline.svg"] = horizontal(COR["asfalto"], COR["placa"], COR["faixa"], "", tagline=False)

    # Assinatura vertical
    d, largura = marca.caminho("Radar HIS", 0, 0, 22, rastreio=-0.01)
    w = max(largura, 96)
    vert = simbolo(COR["placa"], COR["faixa"], (w - 72) / 2, 0, 1.5) + \
        f'<g transform="translate({(w - largura) / 2:.2f} 112)"><path d="{d}" fill="{COR["asfalto"]}"/></g>'
    arquivos["assinatura-vertical.svg"] = svg(w + 2, 118, vert, "Radar HIS")

    # Folha de construção: grade 48, ruas de 2, lote 14 = área de proteção
    linhas = "".join(f'<line x1="{i * 6}" y1="0" x2="{i * 6}" y2="288" stroke="#D6D9D3" stroke-width=".5"/>'
                     f'<line x1="0" y1="{i * 6}" x2="288" y2="{i * 6}" stroke="#D6D9D3" stroke-width=".5"/>' for i in range(49))
    cota = lambda x1, y1, x2, y2, t, tx, ty: (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#B42318" stroke-width="1"/>'
                                               f'<text x="{tx}" y="{ty}" font-family="monospace" font-size="9" fill="#B42318">{t}</text>')
    construcao = (f'<rect width="288" height="288" fill="{COR["papel"]}"/>{linhas}' + simbolo(COR["placa"], COR["faixa"], 0, 0, 6) +
                  cota(0, 294, 90, 294, "15", 40, 306) + cota(90, 294, 102, 294, "2", 92, 306) +
                  cota(102, 294, 186, 294, "14 = lote = área de proteção", 104, 306))
    arquivos["construcao.svg"] = svg(288, 312, construcao, "Construção do símbolo Radar HIS")

    for nome, conteudo in arquivos.items():
        (saida / nome).write_text(conteudo, encoding="utf-8")
        print(nome)


if __name__ == "__main__":
    main()
