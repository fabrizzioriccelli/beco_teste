"""Agente Ilustrador: desenha "a cidade acesa", a imagem de abertura do boletim.

São Paulo vista de cima, à noite. Cada prédio HIS/HMP com alvará é um ponto de luz quente; os
imóveis citados no boletim do dia aparecem mais fortes, com um halo. Só dados oficiais: nada de
foto de banco de imagem. A imagem vai no topo do e-mail (servida pelo repositório público) e
repete o fundo animado do site.

Uso: gerar(emps, distritos_geojson, ids_destaque, caminho_png)
"""
import math

from PIL import Image, ImageChops, ImageDraw, ImageFilter

LARGURA, ALTURA = 1200, 640          # 2x de 600 x 320 no e-mail
LON0, LON1 = -46.83, -46.37          # recorte leste-oeste da mancha urbana
LAT_CENTRO = -23.585
FUNDO_CENTRO, FUNDO_BORDA = (22, 27, 36), (6, 8, 11)
LUZ = (255, 205, 150)                # luz de sódio, quente
LUZ_FORTE = (255, 238, 214)


def _projecao():
    esc = LARGURA / ((LON1 - LON0) * math.cos(math.radians(LAT_CENTRO)))
    def xy(lon, lat):
        x = (lon - LON0) * math.cos(math.radians(LAT_CENTRO)) * esc
        y = ALTURA / 2 - (lat - LAT_CENTRO) * esc
        return x, y
    return xy


def _fundo():
    img = Image.new("RGB", (LARGURA, ALTURA), FUNDO_BORDA)
    px = img.load()
    cx, cy, r = LARGURA * 0.55, ALTURA * 0.5, math.hypot(LARGURA, ALTURA) * 0.55
    for y in range(ALTURA):
        for x in range(0, LARGURA):
            t = min(1.0, math.hypot(x - cx, y - cy) / r)
            t = t * t
            px[x, y] = tuple(int(FUNDO_CENTRO[i] * (1 - t) + FUNDO_BORDA[i] * t) for i in range(3))
    return img


def gerar(emps, distritos, ids_destaque, caminho):
    xy = _projecao()
    base = _fundo()

    # contornos dos distritos, quase invisíveis
    linhas = Image.new("RGB", (LARGURA, ALTURA), (0, 0, 0))
    d = ImageDraw.Draw(linhas)
    for f in distritos.get("features", []):
        g = f["geometry"]
        poligonos = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for pol in poligonos:
            for anel in pol:
                d.line([xy(lon, lat) for lon, lat in anel], fill=(20, 24, 30), width=1)
    base = ImageChops.add(base, linhas)

    # pontos de luz
    luz = Image.new("RGB", (LARGURA, ALTURA), (0, 0, 0))
    d = ImageDraw.Draw(luz)
    destaque = set(ids_destaque or [])
    fortes = []
    for e in emps:
        if e.get("lat") is None or e.get("lon") is None:
            continue
        x, y = xy(e["lon"], e["lat"])
        if not (-10 <= x <= LARGURA + 10 and -10 <= y <= ALTURA + 10):
            continue
        if e["id"] in destaque:
            fortes.append((x, y))
            continue
        un = (e.get("his1") or 0) + (e.get("his2") or 0) + (e.get("hmp") or 0)
        r = 0.7 + min(1.6, math.sqrt(max(un, 1)) / 8)
        k = 0.32 + min(0.5, un / 500)
        cor = tuple(int(c * k) for c in LUZ)
        d.ellipse([x - r, y - r, x + r, y + r], fill=cor)
    brilho = luz.filter(ImageFilter.GaussianBlur(3))
    brilho = Image.eval(brilho, lambda v: min(255, int(v * 1.1)))
    halo = luz.filter(ImageFilter.GaussianBlur(20))
    halo = Image.eval(halo, lambda v: min(255, int(v * 0.9)))
    img = ImageChops.add(ImageChops.add(ImageChops.add(base, halo), brilho), luz)

    # imóveis do boletim: núcleo branco, halo largo e anel fino
    if fortes:
        camada = Image.new("RGB", (LARGURA, ALTURA), (0, 0, 0))
        d = ImageDraw.Draw(camada)
        for x, y in fortes:
            d.ellipse([x - 3.5, y - 3.5, x + 3.5, y + 3.5], fill=LUZ_FORTE)
        glow = camada.filter(ImageFilter.GaussianBlur(10))
        glow = Image.eval(glow, lambda v: min(255, int(v * 2.6)))
        img = ImageChops.add(img, glow)
        img = ImageChops.add(img, camada)
        anel = Image.new("RGB", (LARGURA, ALTURA), (0, 0, 0))
        d = ImageDraw.Draw(anel)
        for x, y in fortes:
            d.ellipse([x - 16, y - 16, x + 16, y + 16], outline=(190, 190, 190), width=2)
        img = ImageChops.add(img, anel)

    # vinheta suave nas bordas de cima e de baixo, para o texto respirar
    mascara = Image.new("L", (1, ALTURA))
    for y in range(ALTURA):
        t = min(y, ALTURA - 1 - y) / (ALTURA * 0.22)
        mascara.putpixel((0, y), int(255 * min(1.0, t)))
    mascara = mascara.resize((LARGURA, ALTURA))
    img = Image.composite(img, Image.new("RGB", (LARGURA, ALTURA), FUNDO_BORDA), mascara)
    img.save(caminho, optimize=True)
    return caminho
