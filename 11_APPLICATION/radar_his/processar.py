#!/usr/bin/env python3
"""Radar HIS - processamento.

Lê a pasta gerada por coletar.py e escreve os arquivos do site em site/dados:
  empreendimentos.json  um registro por lote com alvará HIS/HMP, com resumo das vendas (ITBI)
  transacoes.json       vendas registradas no ITBI em cada empreendimento
  distritos.json        contornos simplificados dos distritos (mapa)
  indices.json          IPCA e CDI mensais (Banco Central)
  meta.json             datas das fontes e totais

Ligação alvará -> ITBI: mesmo setor e quadra fiscal (6 primeiros dígitos do SQL),
mesmo CEP e mesmo número do imóvel. Unidades em condomínio são separadas do terreno
pela fração ideal e pelo uso no IPTU.

Uso:
  python3 processar.py [--dados PASTA] [--saida site/dados]
"""
import argparse
import collections
import datetime as dt
import json
import pathlib
import re
import statistics
import unicodedata

from python_calamine import CalamineWorkbook
from shapely import STRtree
from shapely.geometry import Point, mapping, shape

# Tetos de preço de venda (art. 6º-A do Decreto 63.130/2024). Lidos no texto oficial em
# legislacao.prefeitura.sp.gov.br em 22/11/2026. Antes de 28/05/2025 não havia teto em decreto.
TETOS = [
    (dt.date(2025, 5, 28), dt.date(2026, 1, 5),
     {"HIS-1": 266000.00, "HIS-2": 369600.00, "HMP": 518000.00}, "Decreto 64.244/2025"),
    (dt.date(2026, 1, 6), None,
     {"HIS-1": 276102.20, "HIS-2": 383636.74, "HMP": 537672.71}, "Decreto 64.895/2026"),
]
CATS_SOCIAIS = {"HIS", "HMP", "HIS1"}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().lower()


def data_iso(s):
    return dt.date.fromisoformat(s[:10]) if s else None


def teto_na_data(d, cat):
    for ini, fim, valores, norma in TETOS:
        if d >= ini and (fim is None or d <= fim):
            return valores[cat], norma
    return None, None


def digitos(v):
    if v is None or v == "":
        return ""
    if isinstance(v, float):
        return str(int(v))
    return re.sub(r"\D", "", str(v))


# ---------------------------------------------------------------- GeoSampa
def tipo_alvara(assunto):
    a = norm(assunto)
    if "modificativo" in a:
        return "Projeto modificativo"
    if "declaratorio" in a:
        return "Aprovação e execução (declaratório)"
    if "aprovacao" in a:
        return "Aprovação e execução"
    if "execucao" in a:
        return "Execução"
    return (assunto or "").strip()[:60]


def carregar_empreendimentos(pasta):
    feats = json.loads((pasta / "habitacao_popular.geojson").read_text(encoding="utf-8"))["features"]
    grupos = collections.defaultdict(list)
    for f in feats:
        p = f["properties"]
        chave = (p.get("cd_sql_incra") or "").strip() or f"id{p['cd_identificador_habitacao_popular']}"
        grupos[chave].append((p, f["geometry"]["coordinates"]))

    emps = []
    for sql, itens in grupos.items():
        itens.sort(key=lambda x: (x[0].get("dt_deferimento_execucao") or "", x[0]["cd_identificador_habitacao_popular"]))
        p, (lon, lat) = itens[-1]  # alvará mais recente define as unidades
        ceps, nums = set(), set()
        for q, _ in itens:
            ceps |= {c for c in (digitos(x).zfill(8) for x in re.split(r"[,;/]", q.get("cd_grupo_cep") or "")) if len(c) == 8 and c != "00000000"}
            nums |= {int(n) for n in re.findall(r"(?<!\d)(\d{1,5})(?!\d)", q.get("tx_grupo_endereco") or "") if 0 < int(n) < 100000}
        tokens = {t.strip() for t in (p.get("cd_subcategoria_uso") or "").split(",") if t.strip()}
        his1, his2, hmp = (p.get("qt_unidade_his_tipo_1") or 0), (p.get("qt_unidade_his_tipo_2") or 0), (p.get("qt_unidade_hmp") or 0)
        if hmp or "HMP" in tokens:
            teto_cat = "HMP"
        elif his2 or not his1:
            teto_cat = "HIS-2"
        else:
            teto_cat = "HIS-1"
        autuacoes = [data_iso(q.get("dt_autuacao_execucao")) for q, _ in itens if q.get("dt_autuacao_execucao")]
        deferimentos = [data_iso(q.get("dt_deferimento_execucao")) for q, _ in itens if q.get("dt_deferimento_execucao")]
        endereco = re.split(r",\s*(?=(?:R|RUA|AV|AVENIDA|AL|ALAMEDA|TV|TRAVESSA|PRACA|ESTR|ESTRADA|R\.)\b)", p.get("tx_grupo_endereco") or "", flags=re.I)[0].strip(" ,")
        emps.append({
            "id": sql,
            "end": re.sub(r"\s+", " ", endereco),
            "cep": sorted(ceps)[0] if ceps else "",
            "lat": round(lat, 6), "lon": round(lon, 6),
            "cat": ", ".join(sorted(tokens)) if tokens else "",
            "puro": bool(tokens) and tokens <= CATS_SOCIAIS,
            "teto_cat": teto_cat,
            "his1": his1, "his2": his2, "hmp": hmp,
            "a_terreno": p.get("qt_area_total_terreno"),
            "a_constr": p.get("qt_area_construida_total"),
            "aut0": min(autuacoes).isoformat() if autuacoes else None,
            "def0": min(deferimentos).isoformat() if deferimentos else None,
            "def1": max(deferimentos).isoformat() if deferimentos else None,
            "alv": [[q.get("cd_numero_documento_execucao"), (q.get("dt_deferimento_execucao") or "")[:10],
                     tipo_alvara(q.get("tx_assunto_alvara")), q.get("cd_numero_processo_execucao")] for q, _ in itens],
            "_ceps": ceps, "_nums": nums, "_sq": sql[:6] if sql[:1].isdigit() else "",
            "_atualizacao": max((q.get("dt_atualizacao") or "")[:10] for q, _ in itens),
        })
    return emps


def marcar_territorio(emps, pasta):
    def camada(nome):
        feats = json.loads((pasta / f"{nome}.geojson").read_text(encoding="utf-8"))["features"]
        geoms = [shape(f["geometry"]) for f in feats]
        chave_nome = next(k for k in feats[0]["properties"] if k.startswith("nm_"))
        return feats, geoms, chave_nome
    dist_feats, dist_geoms, dist_nome = camada("distritos")
    sub_feats, sub_geoms, sub_nome = camada("subprefeituras")
    for feats, geoms, chave, campo in [(dist_feats, dist_geoms, dist_nome, "dist"), (sub_feats, sub_geoms, sub_nome, "sub")]:
        arvore = STRtree(geoms)
        for e in emps:
            pt = Point(e["lon"], e["lat"])
            nome = ""
            for i in arvore.query(pt):
                if geoms[i].covers(pt):
                    nome = feats[i]["properties"][chave]
                    break
            e[campo] = (nome or "").title()
    contornos = []
    for f, g in zip(dist_feats, dist_geoms):
        s = g.simplify(0.0006, preserve_topology=True)
        gj = mapping(s)
        gj = json.loads(json.dumps(gj), parse_float=lambda x: round(float(x), 5))
        contornos.append({"type": "Feature", "properties": {"nome": f["properties"][dist_nome].title()}, "geometry": gj})
    return {"type": "FeatureCollection", "features": contornos}


# ---------------------------------------------------------------- ITBI
COLUNAS = {
    "sql": "n° do cadastro (sql)", "logr": "nome do logradouro", "num": "numero", "compl": "complemento",
    "cep": "cep", "nat": "natureza de transacao", "valor": "valor de transacao", "data": "data de transacao",
    "venal": "valor venal de referencia", "fin_tipo": "tipo de financiamento", "fin_valor": "valor financiado",
    "cartorio": "cartorio de registro", "matricula": "matricula do imovel", "fracao": "fracao ideal",
    "area": "area construida", "uso": "descricao do uso", "acc": "acc",
}


def mapear_colunas(cabecalho):
    cab = [norm(c).replace("n deg", "n°") for c in cabecalho]
    idx = {}
    for chave, alvo in COLUNAS.items():
        alvo_n = norm(alvo)
        for i, c in enumerate(cab):
            if c.startswith(alvo_n) or (chave == "sql" and c.startswith("n") and "sql" in c):
                if chave == "venal" and "proporcional" in c:
                    continue
                idx.setdefault(chave, i)
    return idx


def carregar_itbi(pasta, chaves):
    abas = {}  # nome da aba (MES-ANO) -> arquivo mais recente que a contém
    arquivos = sorted((pasta / "itbi").glob("*.xlsx"), key=lambda p: p.stat().st_mtime)
    for arq in arquivos:
        wb = CalamineWorkbook.from_path(str(arq))
        for aba in wb.sheet_names:
            if re.fullmatch(r"[A-Z]{3}-\d{4}", aba.strip()):
                abas[aba.strip()] = (arq, aba)
    linhas, vistos, total = [], set(), collections.Counter()
    cache = {}
    for aba, (arq, nome_aba) in sorted(abas.items(), key=lambda x: x[0][-4:]):
        wb = cache.get(arq) or CalamineWorkbook.from_path(str(arq))
        cache = {arq: wb}
        rows = wb.get_sheet_by_name(nome_aba).to_python()
        if not rows:
            continue
        idx = mapear_colunas(rows[0])
        total[aba[-4:]] += len(rows) - 1
        g = lambda r, k: r[idx[k]] if k in idx and idx[k] < len(r) else None
        for r in rows[1:]:
            sql = digitos(g(r, "sql")).zfill(11)
            cep = digitos(g(r, "cep")).zfill(8)
            try:
                num = int(float(g(r, "num")))
            except (TypeError, ValueError):
                num = None
            emp_ids = chaves.get((sql[:6], cep, num))
            if not emp_ids:
                continue
            d = g(r, "data")
            if isinstance(d, dt.datetime):
                d = d.date()
            if not isinstance(d, dt.date):
                continue
            try:
                valor = float(g(r, "valor") or 0)
            except (TypeError, ValueError):
                valor = 0.0
            mat = digitos(g(r, "matricula"))
            reg = (sql, d, round(valor, 2), norm(g(r, "nat")), mat)
            if reg in vistos:
                continue
            vistos.add(reg)
            num_f = lambda k: float(g(r, k)) if isinstance(g(r, k), (int, float)) else None
            linhas.append({
                "emp": emp_ids, "sql": sql, "data": d, "valor": valor, "nat": str(g(r, "nat") or "").strip(),
                "compl": str(g(r, "compl") or "").strip(), "fin_tipo": str(g(r, "fin_tipo") or "").strip(),
                "fin_valor": num_f("fin_valor") or 0.0, "cartorio": norm(g(r, "cartorio")), "matricula": mat,
                "fracao": num_f("fracao"), "area": num_f("area"), "uso": str(g(r, "uso") or ""),
                "acc": int(num_f("acc") or 0), "aba": aba,
            })
    return linhas, total, sorted(abas, key=lambda a: (a[-4:], "JAN FEV MAR ABR MAI JUN JUL AGO SET OUT NOV DEZ".split().index(a[:3])))


# ---------------------------------------------------------------- índices
def carregar_indice(pasta, nome):
    d = json.loads((pasta / f"bcb_{nome}.json").read_text())
    out = {}
    for r in d:
        dd, mm, aa = r["data"].split("/")
        out[f"{aa}-{mm}"] = float(r["valor"])
    return out


def fator(indice, d0, d1):
    """Fator acumulado dos meses após d0 até d1 (inclusive)."""
    f = 1.0
    y, m = d0.year, d0.month
    while (y, m) < (d1.year, d1.month):
        m += 1
        if m > 12:
            y, m = y + 1, 1
        v = indice.get(f"{y}-{m:02d}")
        if v is None:
            break
        f *= 1 + v / 100
    return f


# ---------------------------------------------------------------- análise
INICIO_UNIDADES = dt.date(2017, 1, 1)  # a camada HIS começa em ago/2019; folga para vendas na planta


def tipo_transacao(t):
    """terreno | unidade | vaga | outro, a partir do complemento, da fração ideal e do uso no IPTU."""
    compl, uso = norm(t["compl"]), norm(t["uso"])
    if re.search(r"\b(vg|vaga|vagas|garagem|box|estac)\b", compl) or "garagem" in uso:
        return "vaga"
    if re.search(r"\b(loja|sala|conj|nr)\b", compl):
        return "outro"
    if (re.search(r"\b(matricula|matr|mat|lote|lotes|lt|gleba|terreno|area|parte|pt|qd|quadra)\b", compl)
            or re.search(r"\bl\.?\s*\d+.*\bq\.?\s*\d+", compl) or re.fullmatch(r"e\s*\d+[a-z]?", compl)):
        return "terreno"
    if t["valor"] > 2_000_000:  # acima de qualquer teto HIS/HMP com folga: negócio do lote, não da unidade
        return "terreno"
    if compl and (re.search(r"\b(ap|apto|apt|apart|apartamento|unid|un|casa|torre|bl|bloco|t)\b", compl) or re.search(r"\d", compl)):
        return "unidade"
    if t["fracao"] is not None and t["fracao"] < 0.999 and ("apartamento" in uso or "condominio" in uso):
        return "unidade"
    return "terreno"


def chave_unidade(t, numeros_endereco):
    """Mesma unidade antes e depois da individualização da matrícula (apartamento + torre).

    Devolve None quando o complemento só repete números do endereço (ex.: "438 E 444"):
    nesse caso a guia é do lote, não de uma unidade.
    """
    c = norm(t["compl"]).upper()
    c = re.sub(r"\b(APARTAMENTO|APART|APTO|APT|AP|UNIDADE|UNID|UN)\b\.?", " AP ", c)
    c = re.sub(r"\b(TORRE|TR|BLOCO|BL|EDIFICIO|ED|T)\b\.?", " T ", c)
    tem_ap = re.search(r"AP\s*N?[º°O]?\s*(\d+)", c)
    numeros = [int(n) for n in re.findall(r"\d+", c)]
    if not tem_ap and numeros and all(n in numeros_endereco for n in numeros):
        return None
    ap = tem_ap or re.search(r"(\d{2,4})(?!.*\d{2,4})", c)
    torre = re.search(r"\bT\s*([A-Z0-9]{1,3})\b", c)
    if ap:
        return f"{torre.group(1) if torre else ''}|{ap.group(1).lstrip('0')}"
    return re.sub(r"[^A-Z0-9]", "", c) or f"sql{t['sql']}"


FAIXA_PLAUSIVEL = (0.5, 2.5)  # revenda/compra fora disso costuma ser guia parcial ou erro de cadastro
JANELA_MESMO_NEGOCIO = 90  # guias da mesma unidade em até 90 dias = um único negócio


def eh_compra_venda(t):
    return "compra e venda" in norm(t["nat"])


def eh_permuta(t):
    n = norm(t["nat"])
    return "dacao" in n or "permuta" in n or "integralizacao" in n


def numero_cartorio(nome):
    m = re.search(r"(\d+)", nome or "")
    return int(m.group(1)) if m else 0


def destaques(emps, transacoes, ipca, limite=40):
    """Itens do boletim: alvarás novos, revendas recentes e vendas acima do teto."""
    por_id = {e["id"]: e for e in emps}
    base = lambda e: {"id": e["id"], "end": e["end"], "dist": e["dist"]}
    novos = [dict(base(e), data=e["def1"], his1=e["his1"], his2=e["his2"], hmp=e["hmp"], cat=e["cat"])
             for e in sorted(emps, key=lambda e: e["def1"] or "", reverse=True)[:limite]]
    revendas, acima = [], []
    for eid, lista in transacoes.items():
        e = por_id[eid]
        unidades = collections.defaultdict(list)
        for t in lista:
            if t[2] in ("venda", "revenda"):
                unidades[t[8]].append(t)
            if t[6]:
                teto, norma = teto_na_data(dt.date.fromisoformat(t[0]), e["teto_cat"])
                acima.append(dict(base(e), un=t[3], data=t[0], valor=t[1], teto=teto, categoria=e["teto_cat"], norma=norma))
        for l in unidades.values():
            if len(l) > 1 and l[-1][2] == "revenda":
                a, b = l[0], l[-1]
                d0, d1 = dt.date.fromisoformat(a[0]), dt.date.fromisoformat(b[0])
                nom = b[1] / a[1]
                if not FAIXA_PLAUSIVEL[0] <= nom <= FAIXA_PLAUSIVEL[1]:
                    continue
                revendas.append(dict(base(e), un=b[3] or a[3], d0=a[0], v0=a[1], d1=b[0], v1=b[1],
                                     nominal=round(nom - 1, 4), real=round(nom / fator(ipca, d0, d1) - 1, 4)))
    revendas.sort(key=lambda r: r["d1"], reverse=True)
    acima.sort(key=lambda r: r["data"], reverse=True)
    ganhos = sorted((r for r in revendas if (dt.date.fromisoformat(r["d1"]) - dt.date.fromisoformat(r["d0"])).days >= 365),
                    key=lambda r: r["real"], reverse=True)
    return {"novos": novos, "revendas": revendas[:limite], "acima_teto": acima[:limite], "maiores_ganhos": ganhos[:limite]}


def analisar(emps, linhas, ipca, cdi):
    por_emp = collections.defaultdict(list)
    for t in linhas:
        for eid in t["emp"]:
            por_emp[eid].append(t)
    transacoes = {}
    for e in emps:
        ts = sorted(por_emp.get(e["id"], []), key=lambda t: t["data"])
        unidades = collections.defaultdict(list)
        for t in ts:
            if t["valor"] <= 0:
                continue
            tipo = tipo_transacao(t)
            if tipo == "unidade" and t["data"] < INICIO_UNIDADES:
                tipo = None  # unidade de prédio anterior no mesmo endereço: fora do recorte
            elif tipo == "unidade":
                uid = chave_unidade(t, e["_nums"])
                if uid is None:
                    tipo = "terreno"
                else:
                    unidades[uid].append(t)
            t["_tipo"] = tipo
        # Guias complementares (valor muito abaixo do típico do prédio) não são negócios.
        valores_cv = [t["valor"] for l in unidades.values() for t in l if eh_compra_venda(t)]
        mediana = statistics.median(valores_cv) if valores_cv else 0
        piso, teto_unidade = 0.3 * mediana, max(5 * mediana, 3_000_000)
        for uid in list(unidades):
            grandes = [t for t in unidades[uid] if t["valor"] > teto_unidade]
            for t in grandes:  # valor de lote inteiro, não de apartamento
                t["_tipo"] = "terreno"
                unidades[uid].remove(t)
            if not unidades[uid]:
                del unidades[uid]
        n_un = 0
        variacoes, primeiras, revendas, m2 = [], [], [], []
        acima = 0
        for uid, lista in unidades.items():
            lista.sort(key=lambda t: t["data"])
            negocios = []  # cada negócio = guias da mesma unidade dentro da janela
            for t in lista:
                if t["valor"] < piso:
                    t["_tipo"] = "complemento"
                    continue
                if negocios and (t["data"] - negocios[-1][-1]["data"]).days <= JANELA_MESMO_NEGOCIO:
                    negocios[-1].append(t)
                else:
                    negocios.append([t])
            if not negocios:
                continue
            n_un += 1
            eventos = []
            for grupo in negocios:
                principal = max(grupo, key=lambda t: (eh_compra_venda(t), t["valor"]))
                for t in grupo:
                    t["_tipo"] = "duplicada"
                    t["_un"] = n_un
                eventos.append(principal)
            for i, t in enumerate(eventos):
                if eh_permuta(t):
                    t["_tipo"] = "permuta"
                elif i == 0 or all(eh_permuta(x) for x in eventos[:i]):
                    t["_tipo"] = "venda"
                else:
                    t["_tipo"] = "revenda"
                t["_acima"] = None
                if eh_compra_venda(t) and e["puro"]:
                    teto, _ = teto_na_data(t["data"], e["teto_cat"])
                    if teto:
                        t["_acima"] = t["valor"] > teto + 0.5
                        acima += t["_acima"]
                if t["_tipo"] == "venda":
                    primeiras.append(t["valor"])
                    if t["area"] and t["area"] < 400:
                        m2.append(t["valor"] / t["area"])
                elif t["_tipo"] == "revenda":
                    revendas.append(t["valor"])
            precos = [t for t in eventos if t["_tipo"] in ("venda", "revenda") and eh_compra_venda(t)]
            if len(precos) >= 2 and FAIXA_PLAUSIVEL[0] <= precos[-1]["valor"] / precos[0]["valor"] <= FAIXA_PLAUSIVEL[1]:
                a, b = precos[0], precos[-1]
                nom = b["valor"] / a["valor"]
                variacoes.append((nom, nom / fator(ipca, a["data"], b["data"]), fator(cdi, a["data"], b["data"])))
        med = lambda xs: round(statistics.median(xs), 2) if xs else None
        terrenos = [t for t in ts if t.get("_tipo") == "terreno"]
        e["itbi"] = {
            "n_unidades": n_un,
            "n_vendas": len(primeiras),
            "n_revendas": len(revendas),
            "med_venda": med(primeiras),
            "med_m2": med(m2),
            "med_revenda": med(revendas),
            "n_acima_teto": acima,
            "n_com_revenda": len(variacoes),
            "med_var_nominal": med([v[0] - 1 for v in variacoes]),
            "med_var_real": med([v[1] - 1 for v in variacoes]),
            "terreno": [terrenos[-1]["data"].isoformat(), round(terrenos[-1]["valor"], 2)] if terrenos else None,
            "ultima": max((t["data"] for t in ts if t.get("_tipo") in ("venda", "revenda")), default=None),
        }
        if e["itbi"]["ultima"]:
            e["itbi"]["ultima"] = e["itbi"]["ultima"].isoformat()
        visiveis = ("terreno", "venda", "revenda", "permuta", "vaga", "outro")
        saida = [[t["data"].isoformat(), round(t["valor"], 2), t["_tipo"], t["compl"][:24], round(t["area"] or 0, 1),
                  1 if t["fin_valor"] else 0, t.get("_acima"), t["nat"].split(".", 1)[-1][:28], t.get("_un", 0),
                  numero_cartorio(t["cartorio"]), t["matricula"]]
                 for t in ts if t.get("_tipo") in visiveis]
        if saida:
            transacoes[e["id"]] = saida
    return transacoes


def lote_tx(eid):
    """Arquivo de transações de um empreendimento: tx_<2 primeiros dígitos do setor>.json."""
    return eid[:2] if eid[:2].isdigit() else "xx"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dados", default="_dados")
    ap.add_argument("--saida", default="site/dados")
    a = ap.parse_args()
    pasta, saida = pathlib.Path(a.dados), pathlib.Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)

    emps = carregar_empreendimentos(pasta)
    distritos = marcar_territorio(emps, pasta)
    chaves = collections.defaultdict(list)
    for e in emps:
        if e["_sq"]:
            for c in e["_ceps"]:
                for n in e["_nums"]:
                    chaves[(e["_sq"], c, n)].append(e["id"])
    print(f"Empreendimentos (lotes): {len(emps)}; chaves de ligação: {len(chaves)}")

    linhas, total_itbi, abas = carregar_itbi(pasta, chaves)
    print(f"ITBI: {sum(total_itbi.values())} guias lidas ({abas[0]} a {abas[-1]}); {len(linhas)} ligadas a empreendimentos HIS/HMP")

    ipca, cdi = carregar_indice(pasta, "ipca"), carregar_indice(pasta, "cdi")
    transacoes = analisar(emps, linhas, ipca, cdi)

    atualizacao = max(e.pop("_atualizacao") for e in emps)
    for e in emps:
        for k in ("_ceps", "_nums", "_sq"):
            e.pop(k)
    emps.sort(key=lambda e: e["def1"] or "", reverse=True)
    coleta = json.loads((pasta / "coleta.json").read_text()) if (pasta / "coleta.json").exists() else {}
    meta = {
        "gerado_em": dt.datetime.now().isoformat(timespec="seconds"),
        "coletado_em": coleta.get("coletado_em"),
        "geosampa_atualizacao": atualizacao,
        "ultimo_deferimento": emps[0]["def1"],
        "itbi_primeiro_mes": abas[0], "itbi_ultimo_mes": abas[-1],
        "itbi_guias_lidas": sum(total_itbi.values()),
        "itbi_ligadas": sum(len(v) for v in transacoes.values()),
        "ipca_ultimo": max(ipca), "cdi_ultimo": max(cdi),
        "tetos": [{"inicio": i.isoformat(), "fim": f.isoformat() if f else None, "valores": v, "norma": n} for i, f, v, n in TETOS],
        "totais": {
            "empreendimentos": len(emps),
            "alvaras": sum(len(e["alv"]) for e in emps),
            "his1": sum(e["his1"] for e in emps), "his2": sum(e["his2"] for e in emps), "hmp": sum(e["hmp"] for e in emps),
            "com_vendas": sum(1 for e in emps if e["itbi"]["n_vendas"]),
            "vendas": sum(e["itbi"]["n_vendas"] for e in emps),
            "revendas": sum(e["itbi"]["n_revendas"] for e in emps),
            "acima_teto": sum(e["itbi"]["n_acima_teto"] for e in emps),
        },
    }
    escrever = lambda nome, obj: (saida / nome).write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    escrever("empreendimentos.json", emps)
    escrever("destaques.json", destaques(emps, transacoes, ipca))
    for velho in saida.glob("tx_*.json"):
        velho.unlink()
    lotes = collections.defaultdict(dict)
    for eid, lista in transacoes.items():
        lotes[lote_tx(eid)][eid] = lista
    for lote, conteudo in lotes.items():
        escrever(f"tx_{lote}.json", conteudo)
    escrever("distritos.json", distritos)
    escrever("indices.json", {"ipca": ipca, "cdi": cdi})
    escrever("meta.json", meta)
    print(json.dumps(meta["totais"], ensure_ascii=False))
    tam = {f.name: f.stat().st_size for f in saida.iterdir()}
    tx = [v for k, v in tam.items() if k.startswith("tx_")]
    for k, v in sorted(tam.items()):
        if not k.startswith("tx_"):
            print(f"  {k}: {v / 1e3:.0f} KB")
    print(f"  tx_*.json: {len(tx)} arquivos, {sum(tx) / 1e6:.1f} MB no total, maior {max(tx) / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
