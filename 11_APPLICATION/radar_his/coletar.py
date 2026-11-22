#!/usr/bin/env python3
"""Radar HIS - coleta das fontes oficiais.

Baixa para uma pasta local (padrão: ./_dados):
  1. GeoSampa (WFS): camada "HIS e HMP - Alvará de Execução" (geoportal:habitacao_popular),
     distritos e subprefeituras.
  2. Secretaria Municipal da Fazenda: planilhas "Guias de ITBI pagas" (2006 em diante).
  3. Banco Central (SGS): IPCA mensal (série 433) e CDI mensal (série 4391).

Uso:
  python3 coletar.py [--dados PASTA] [--sem-itbi]

Os arquivos de ITBI só são baixados de novo quando o tamanho publicado muda.
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
WFS = "https://wms.geosampa.prefeitura.sp.gov.br/geoserver/ows"
CAMADAS = {
    "habitacao_popular": "geoportal:habitacao_popular",
    "distritos": "geoportal:distrito_municipal",
    "subprefeituras": "geoportal:subprefeitura",
}
PAGINA_ITBI = "https://prefeitura.sp.gov.br/web/fazenda/w/acesso_a_informacao/31501"
SGS = {"ipca": 433, "cdi": 4391}


def baixar(url, destino=None, timeout=900):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        dados = r.read()
    if destino:
        pathlib.Path(destino).write_bytes(dados)
    return dados


def tamanho_remoto(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return int(r.headers.get("Content-Length") or 0)
    except Exception:
        return 0


def coletar_geosampa(pasta):
    for nome, camada in CAMADAS.items():
        q = urllib.parse.urlencode({
            "service": "WFS", "version": "2.0.0", "request": "GetFeature",
            "typeNames": camada, "outputFormat": "application/json", "srsName": "EPSG:4326",
        })
        destino = pasta / f"{nome}.geojson"
        baixar(f"{WFS}?{q}", destino)
        n = len(json.loads(destino.read_text(encoding="utf-8"))["features"])
        print(f"GeoSampa {camada}: {n} registros")


def coletar_itbi(pasta):
    pasta_itbi = pasta / "itbi"
    pasta_itbi.mkdir(exist_ok=True)
    html = baixar(PAGINA_ITBI, timeout=120).decode("utf-8", "ignore")
    links = sorted(set(re.findall(r'href="([^"]*(?:ITBI|itbi)[^"]*\.xlsx)"', html)))
    if not links:
        raise RuntimeError("Nenhuma planilha de ITBI encontrada na página da Fazenda (o layout pode ter mudado).")
    for link in links:
        url = link.replace(" ", "%20")
        nome = urllib.parse.unquote(url.rsplit("/", 1)[1]).replace(" ", "_")
        destino = pasta_itbi / nome
        remoto = tamanho_remoto(url)
        if destino.exists() and remoto and destino.stat().st_size == remoto:
            print(f"ITBI {nome}: sem mudança")
            continue
        baixar(url, destino)
        print(f"ITBI {nome}: {destino.stat().st_size / 1e6:.1f} MB")


def coletar_bcb(pasta):
    hoje = dt.date.today().strftime("%d/%m/%Y")
    for nome, serie in SGS.items():
        url = (f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados"
               f"?formato=json&dataInicial=01/01/2006&dataFinal={hoje}")
        destino = pasta / f"bcb_{nome}.json"
        baixar(url, destino, timeout=120)
        d = json.loads(destino.read_text())
        print(f"Banco Central {nome} (SGS {serie}): {len(d)} meses, último {d[-1]['data']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dados", default="_dados")
    ap.add_argument("--sem-itbi", action="store_true", help="não baixa as planilhas de ITBI")
    a = ap.parse_args()
    pasta = pathlib.Path(a.dados)
    pasta.mkdir(parents=True, exist_ok=True)
    coletar_geosampa(pasta)
    coletar_bcb(pasta)
    if not a.sem_itbi:
        coletar_itbi(pasta)
    (pasta / "coleta.json").write_text(json.dumps({"coletado_em": dt.datetime.now().isoformat(timespec="seconds")}))
    print("Coleta concluída em", pasta.resolve())


if __name__ == "__main__":
    sys.exit(main())
