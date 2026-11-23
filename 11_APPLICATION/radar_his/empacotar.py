"""Empacotador: gera os arquivos leves que o site carrega.

A base completa (site/dados/empreendimentos.json, tx_XX.json) continua sendo a fonte dos agentes.
O site recebe só o que mostra, em JSON sem espaços:
  dados/pontos.json  - um ponto por prédio (id, lat, lon, unidades, categoria, data do alvará), em
                       ordem de alvará. É o que o herói e o mapa desenham; chega antes do resto.
  dados/base.json    - os prédios com os campos usados nas listas, na busca e na ficha.
  dados/tx/ABC.json  - vendas por prédio, em pedaços pelos 3 primeiros dígitos do id (~50 KB cada),
                       baixados só quando uma ficha abre.
Uso: python3 empacotar.py   (a rotina diária chama depois do Analista)
"""
import json
import pathlib

AQUI = pathlib.Path(__file__).resolve().parent
DADOS = AQUI / "site" / "dados"
CAMPOS_ITBI = ("n_vendas", "n_revendas", "n_com_revenda", "n_acima_teto", "med_venda", "med_var_real", "terreno")


def categoria(cat):
    if not cat:
        return 0
    if any(x in cat for x in ("R2", "nR", "R1")):
        return 3          # com unidades de mercado
    return 2 if "HMP" in cat else 1


def gravar(caminho, obj):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def main():
    emps = json.loads((DADOS / "empreendimentos.json").read_text(encoding="utf-8"))
    # base em formato de tabela: os nomes dos campos aparecem uma vez; o site remonta os objetos
    linhas, pontos = [], []
    for e in emps:
        it = e["itbi"]
        lat = round(e["lat"], 5) if e.get("lat") is not None else None
        lon = round(e["lon"], 5) if e.get("lon") is not None else None
        alv = e["alv"][-1] if e["alv"] else None
        linhas.append([e["id"], e["end"], e.get("cep"), lat, lon, e.get("cat"), e["his1"], e["his2"], e["hmp"], e.get("def1"),
                       alv and [alv[0], alv[3]], e.get("dist"), e.get("sub"),
                       [it.get(k) if it.get(k) not in (0,) else 0 for k in CAMPOS_ITBI[:4]] +
                       [it.get("med_venda"), round(it["med_var_real"], 4) if it.get("med_var_real") is not None else None, it.get("terreno")]])
        if lat is not None and lon is not None:
            pontos.append([e["id"], round(lat * 1e4), round(lon * 1e4), e["his1"] + e["his2"] + e["hmp"], categoria(e.get("cat")), e.get("def1") or ""])
    pontos.sort(key=lambda q: q[5])
    pontos = [q[:5] for q in pontos]            # a ordem já é a do alvará; a data não precisa ir

    tx = {}
    for f in sorted(DADOS.glob("tx_*.json")):
        tx.update(json.loads(f.read_text(encoding="utf-8")))
    grupos = {}
    for k, v in tx.items():
        grupos.setdefault(k[:3] if k[:3].isdigit() else "xxx", {})[k] = v
    pedacos, divididos = {}, []
    for p3, d in grupos.items():               # pedaço grande demais: divide pelos 4 primeiros dígitos
        if len(json.dumps(d, separators=(",", ":"))) > 160_000 and p3 != "xxx":
            divididos.append(p3)
            for k, v in d.items():
                pedacos.setdefault(k[:4], {})[k] = v
        else:
            pedacos[p3] = d
    gravar(DADOS / "base.json", {"campos": ["id", "end", "cep", "lat", "lon", "cat", "his1", "his2", "hmp", "def1", "alv", "dist", "sub", "itbi"],
                                 "itbi": list(CAMPOS_ITBI), "tx4": sorted(divididos), "d": linhas})
    gravar(DADOS / "pontos.json", pontos)
    pasta = DADOS / "tx"
    for velho in pasta.glob("*.json") if pasta.exists() else []:
        velho.unlink()
    for p, d in pedacos.items():
        gravar(pasta / f"{p}.json", d)
    tamanho = lambda c: c.stat().st_size
    print(f"[Empacotador] base {tamanho(DADOS / 'base.json') // 1000} KB, pontos {tamanho(DADOS / 'pontos.json') // 1000} KB, "
          f"{len(pedacos)} pedaços de vendas (maior {max(tamanho(f) for f in pasta.glob('*.json')) // 1000} KB)")


def arquivos_do_site():
    """Arquivos que o site publica (caminhos relativos a site/)."""
    fixos = ["boletim", "boletins", "destaques", "distritos", "indices", "meta", "base", "pontos"]
    return [f"dados/{n}.json" for n in fixos if (DADOS / f"{n}.json").exists()] + sorted(f"dados/tx/{p.name}" for p in (DADOS / "tx").glob("*.json"))


if __name__ == "__main__":
    main()
