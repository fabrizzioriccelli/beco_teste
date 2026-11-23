#!/usr/bin/env python3
"""Gera os arquivos da marca Faro v5 (SVG com o texto convertido em curvas).

Proposta 5, aprovada em 23/11/2026: só o nome. FARO em Geist Light, maiúsculas com espaçamento
largo, preto e branco. Sem símbolo e sem cor de destaque: a marca é o nome e a imagem da cidade
acesa (os 5.250 prédios HIS/HMP de São Paulo como pontos de luz, desenhada pelo ilustrador.py).

O texto do site e do e-mail usa a fonte do sistema (SF Pro nos aparelhos Apple) com Geist nos
demais. O logo não usa SF porque a licença da Apple não permite usá-la em logotipos.

Uso:
  python3 gerar_identidade.py --fontes PASTA_COM_FONTSOURCE --saida faro/
Requer fonttools. Fonte: Geist 300 e 400 (licença OFL), pacote @fontsource/geist-sans.
"""
import argparse
import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

PRETO, BRANCO, PEDRA, CINZA = "#0B0B0C", "#FFFFFF", "#F4F3F1", "#8E8E93"
RASTREIO = 0.42            # espaço entre letras do logotipo, em eme
RASTREIO_DESC = 0.38
VERSAL = 710               # altura das maiúsculas na Geist (1000 por eme)


class Fonte:
    def __init__(self, caminho):
        self.f = TTFont(caminho)
        self.g = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm

    def texto(self, texto, x, base, corpo, rastreio=0.0):
        """Caminho SVG e largura ótica (sem o espaço depois da última letra)."""
        esc = corpo / self.upm
        pen = SVGPathPen(self.g)
        cur = 0.0
        for ch in texto:
            gl = self.g[self.cmap[ord(ch)]]
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
    leve = Fonte(next(fontes.glob("**/geist-sans-latin-300-normal.woff")))
    regular = Fonte(next(fontes.glob("**/geist-sans-latin-400-normal.woff")))

    corpo = 100
    versal = VERSAL * corpo / 1000          # 71 px
    margem = versal / 3                      # área de proteção: um terço da versal

    def logotipo(cor):
        d, w = leve.texto("FARO", margem, margem + versal, corpo, RASTREIO)
        return svg(w + 2 * margem, versal + 2 * margem, f'<path d="{d}" fill="{cor}"/>')

    def assinatura(cor, cor_desc):
        d1, w1 = leve.texto("FARO", 0, 0, corpo, RASTREIO)
        c2 = corpo * 0.15
        d2, w2 = regular.texto("INTELIGÊNCIA IMOBILIÁRIA", 0, 0, c2, RASTREIO_DESC)
        W = max(w1, w2) + 2 * margem
        y1 = margem + versal
        y2 = y1 + versal * 0.62
        H = y2 + margem
        return svg(W, H, f'<path d="{d1}" fill="{cor}" transform="translate({(W - w1) / 2:.2f} {y1:.2f})"/>'
                         f'<path d="{d2}" fill="{cor_desc}" transform="translate({(W - w2) / 2:.2f} {y2:.2f})"/>')

    def icone(t, rx, peso, fundo=PRETO, cor=BRANCO):
        fonte = leve if peso == 300 else regular
        c = t * 0.62
        gl = fonte.g[fonte.cmap[ord("F")]]
        esc = c / 1000
        larg = (531 - 93) * esc                       # caixa do F na Geist
        x = (t - larg) / 2 - 93 * esc
        base = (t + VERSAL * esc) / 2
        d, _ = fonte.texto("F", x, base, c)
        return svg(t, t, f'<rect width="{t}" height="{t}" rx="{rx}" fill="{fundo}"/><path d="{d}" fill="{cor}"/>')

    arq = {
        "logotipo.svg": logotipo(PRETO),
        "logotipo-negativo.svg": logotipo(BRANCO),
        "assinatura.svg": assinatura(PRETO, CINZA),
        "assinatura-negativa.svg": assinatura(BRANCO, "#A1A1A6"),
        "icone-app.svg": icone(1024, 229, 300),       # raio ~22% como os ícones do iOS
        "favicon.svg": icone(64, 14, 400),
    }

    # Folha de construção: espaçamento, versal e área de proteção
    d, w = leve.texto("FARO", 60, 60 + versal * 2, corpo * 2, RASTREIO)
    W, H = w + 120, versal * 2 + 170
    v2 = versal * 2
    guias = (f'<rect x="{60 - v2 / 3:.1f}" y="{60 - v2 / 3:.1f}" width="{w + 2 * v2 / 3:.1f}" height="{v2 + 2 * v2 / 3:.1f}" fill="none" stroke="{CINZA}" stroke-dasharray="4 4" stroke-width="1"/>'
             f'<line x1="0" y1="{60 + v2:.1f}" x2="{W:.1f}" y2="{60 + v2:.1f}" stroke="{CINZA}" stroke-width=".8"/>'
             f'<line x1="0" y1="60" x2="{W:.1f}" y2="60" stroke="{CINZA}" stroke-width=".8"/>')
    nota = (f'<text x="20" y="{H - 34:.1f}" font-family="sans-serif" font-size="13" fill="{CINZA}">Geist Light, maiúsculas, espaçamento de 0,42 eme entre letras.</text>'
            f'<text x="20" y="{H - 14:.1f}" font-family="sans-serif" font-size="13" fill="{CINZA}">Área de proteção (tracejado): um terço da altura das maiúsculas. Mínimo: 14 px de altura.</text>')
    arq["construcao.svg"] = svg(W, H, f'<rect width="{W:.1f}" height="{H:.1f}" fill="{BRANCO}"/>' + guias + f'<path d="{d}" fill="{PRETO}"/>' + nota)

    for nome, conteudo in arq.items():
        (saida / nome).write_text(conteudo, encoding="utf-8")
        print(nome)


if __name__ == "__main__":
    main()
