"""Agente Redator: escreve o boletim diário ("o que mapeamos ontem") a partir da comparação
com o snapshot da execução anterior. Gera HTML de e-mail (estilos inline) e texto puro."""
import datetime as dt
import html
import json
import pathlib

COR = {"placa": "#1F3F8B", "faixa": "#F2B705", "asfalto": "#171C1B", "grafite": "#59625F", "meio_fio": "#D6D9D3",
       "calcada": "#E5E7E2", "concreto": "#EFF0EC", "papel": "#FFFFFF", "ganho": "#1C6B45", "alerta": "#B42318",
       "alerta_fundo": "#FBE4E1", "ganho_fundo": "#E2F1E7"}
FONTE_MARCA = "Archivo, 'Helvetica Neue', Arial, sans-serif"
FONTE_TEXTO = "'IBM Plex Sans', 'Segoe UI', Arial, sans-serif"
FONTE_DADO = "'IBM Plex Mono', Menlo, Consolas, monospace"
MES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def brl(v):
    return "R$ " + f"{v:,.0f}".replace(",", ".")


def pct(x):
    return ("+" if x >= 0 else "−") + f"{abs(x) * 100:.0f}%"


def vs_inflacao(x):
    return f"{abs(x) * 100:.0f}% {'acima' if x >= 0 else 'abaixo'} da inflação"


def plural(n, um, varios):
    return f"{n} {um if n == 1 else varios}"


def oportunidade_plausivel(r):
    """Para o boletim, só pares de compra e revenda com cara de negócio real de apartamento."""
    return r["v0"] >= 100_000 and 0.6 <= r["v1"] / r["v0"] <= 1.8


def data_br(iso):
    return "-".join(reversed(iso[:10].split("-"))).replace("-", "/") if iso else "—"


def mes_ano(iso):
    return f"{MES[int(iso[5:7]) - 1]}/{iso[2:4]}" if iso else "—"


def snapshot(emps, meta):
    """O que a próxima execução usa para saber o que é novo."""
    return {
        "gerado_em": meta["gerado_em"], "geosampa_atualizacao": meta["geosampa_atualizacao"],
        "itbi_ultimo_mes": meta["itbi_ultimo_mes"], "itbi_guias_lidas": meta["itbi_guias_lidas"],
        "itbi_ligadas": meta["itbi_ligadas"], "ipca_ultimo": meta["ipca_ultimo"], "totais": meta["totais"],
        "emps": {e["id"]: [e["itbi"]["n_vendas"], e["itbi"]["n_revendas"], e["itbi"]["n_acima_teto"]] for e in emps},
    }


def comparar(emps, dest, meta, ant):
    por_id = {e["id"]: e for e in emps}
    if not ant:
        return {"primeiro": True}
    velhos = ant.get("emps", {})
    novos_alv = sorted((e for e in emps if e["id"] not in velhos), key=lambda e: e["def1"] or "", reverse=True)
    dv = {e["id"]: e["itbi"]["n_vendas"] - velhos[e["id"]][0] for e in emps if e["id"] in velhos}
    dr = {e["id"]: e["itbi"]["n_revendas"] - velhos[e["id"]][1] for e in emps if e["id"] in velhos}
    da = {e["id"]: e["itbi"]["n_acima_teto"] - velhos[e["id"]][2] for e in emps if e["id"] in velhos}
    com_venda = sorted((i for i, d in dv.items() if d > 0), key=lambda i: -dv[i])
    return {
        "primeiro": False,
        "novos_alvaras": novos_alv,
        "vendas_novas": sum(d for d in dv.values() if d > 0),
        "revendas_novas": sum(d for d in dr.values() if d > 0),
        "acima_novas": sum(d for d in da.values() if d > 0),
        "predios_com_venda": [por_id[i] for i in com_venda[:5]],
        "revendas": _primeiros_por_predio(dest["revendas"], dr)[:5],
        "acima": _agrupar_acima(_primeiros_por_predio(dest["acima_teto"], da))[:5],
        "fonte_alvaras_mudou": meta["geosampa_atualizacao"] != ant.get("geosampa_atualizacao"),
        "fonte_itbi_mudou": meta["itbi_ultimo_mes"] != ant.get("itbi_ultimo_mes"),
        "desde": ant.get("gerado_em", "")[:10],
    }


def _primeiros_por_predio(lista, deltas):
    """Só os itens novos: para cada prédio, os `delta` itens mais recentes."""
    usados, saida = {}, []
    for x in lista:
        if usados.get(x["id"], 0) < deltas.get(x["id"], 0):
            usados[x["id"]] = usados.get(x["id"], 0) + 1
            saida.append(x)
    return saida


def _agrupar_acima(lista):
    grupos = {}
    for a in lista:
        g = grupos.setdefault(a["id"], dict(a, n=0, maior=0.0, unidades=[]))
        g["n"] += 1
        g["maior"] = max(g["maior"], a["valor"] - a["teto"])
        g["unidades"].append(a["un"])
    return list(grupos.values())


def rotativos(lista, n, hoje, excluir):
    """Escolhe n itens diferentes a cada dia, para o boletim nunca vir vazio."""
    lista = [x for x in lista if x["id"] not in excluir]
    if not lista:
        return []
    k = hoje.toordinal() % len(lista)
    return (lista[k:] + lista[:k])[:n]


# ---------------------------------------------------------------- HTML
def _e(s):
    return html.escape(str(s or ""))


def item_html(link, titulo, linha1, linha2="", destaque=None):
    cor = {"ganho": COR["ganho"], "alerta": COR["alerta"]}.get(destaque, COR["asfalto"])
    return f"""
<tr><td style="padding:0 0 12px">
 <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:{COR['papel']};border:1px solid {COR['meio_fio']};border-radius:12px">
  <tr><td style="padding:14px 16px">
   <div style="font-family:{FONTE_MARCA};font-weight:700;font-size:16px;color:{COR['asfalto']};line-height:1.3">{_e(titulo)}</div>
   <div style="font-family:{FONTE_TEXTO};font-size:13px;color:{COR['grafite']};padding-top:2px">{linha1}</div>
   {f'<div style="font-family:{FONTE_TEXTO};font-size:14px;color:{cor};padding-top:6px">{linha2}</div>' if linha2 else ''}
   <div style="padding-top:10px"><a href="{link}" style="display:inline-block;background:{COR['placa']};color:#FFFFFF;font-family:{FONTE_TEXTO};font-size:14px;font-weight:600;text-decoration:none;padding:8px 14px;border-radius:8px">Ver contatos e detalhes</a></div>
  </td></tr>
 </table>
</td></tr>"""


def secao(titulo, itens_html, nota=""):
    if not itens_html:
        return ""
    return f"""
<tr><td style="padding:22px 0 10px">
 <table role="presentation" cellspacing="0" cellpadding="0"><tr>
  <td style="width:11px;height:11px;background:{COR['faixa']}"></td>
  <td style="padding-left:10px;font-family:{FONTE_MARCA};font-weight:700;font-size:19px;color:{COR['asfalto']}">{_e(titulo)}</td>
 </tr></table>
 {f'<div style="font-family:{FONTE_TEXTO};font-size:13px;color:{COR["grafite"]};padding-top:4px">{nota}</div>' if nota else ''}
</td></tr>{''.join(itens_html)}"""


def numeros_html(pares):
    cel = "".join(f"""<td width="{100 // len(pares)}%" style="padding:4px">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:{COR['papel']};border:1px solid {COR['meio_fio']};border-radius:10px"><tr><td style="padding:10px 12px">
   <div style="font-family:{FONTE_MARCA};font-weight:800;font-size:24px;color:{COR['placa']}">{v}</div>
   <div style="font-family:{FONTE_TEXTO};font-size:12.5px;color:{COR['grafite']}">{_e(r)}</div></td></tr></table></td>""" for v, r in pares)
    return f'<tr><td><table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr>{cel}</tr></table></td></tr>'


def redigir(pasta_dados, snapshot_anterior, auditoria, config, hoje=None):
    hoje = hoje or dt.date.today()
    pasta = pathlib.Path(pasta_dados)
    emps = json.loads((pasta / "empreendimentos.json").read_text(encoding="utf-8"))
    dest = json.loads((pasta / "destaques.json").read_text(encoding="utf-8"))
    meta = json.loads((pasta / "meta.json").read_text(encoding="utf-8"))
    link = config["link_radar"]
    ficha = lambda i: f"{link}#imovel-{i}"
    c = comparar(emps, dest, meta, snapshot_anterior)
    dia = data_br(hoje.isoformat())[:5]

    blocos, texto = [], []
    vistos = set()
    if c["primeiro"]:
        titulo = "Panorama do Radar HIS"
        resumo = (f"Primeiro boletim. Estamos acompanhando {meta['totais']['empreendimentos']:,} prédios com alvará HIS/HMP na capital, "
                  f"{meta['totais']['vendas']:,} primeiras vendas e {meta['totais']['revendas']:,} revendas registradas.").replace(",", ".")
        numeros = [(f"{meta['totais']['empreendimentos']:,}".replace(",", "."), "prédios HIS/HMP"),
                   (f"{meta['totais']['revendas']:,}".replace(",", "."), "revendas registradas"),
                   (f"{meta['totais']['acima_teto']}", "vendas acima do teto")]
        novos = dest["novos"][:3]
        blocos.append(secao("Alvarás mais recentes", [item_html(ficha(n["id"]), n["end"], f"{_e(n['dist'])} · alvará de {data_br(n['data'])}",
                                                                 f"{n['his1'] + n['his2'] + n['hmp']} unidades HIS/HMP") for n in novos]))
        vistos |= {n["id"] for n in novos}
        assunto = f"Radar HIS · {dia} · panorama de {meta['totais']['empreendimentos']:,} prédios HIS/HMP".replace(",", ".")
    else:
        n_alv, vn, rn, an = len(c["novos_alvaras"]), c["vendas_novas"], c["revendas_novas"], c["acima_novas"]
        titulo = "O que mapeamos ontem"
        partes = []
        if n_alv: partes.append(plural(n_alv, "alvará HIS/HMP novo", "alvarás HIS/HMP novos"))
        if vn: partes.append(plural(vn, "venda nova", "vendas novas"))
        if rn: partes.append(plural(rn, "revenda", "revendas"))
        if an: partes.append(plural(an, "venda acima do teto", "vendas acima do teto"))
        if partes:
            resumo = "Desde o último boletim: " + ", ".join(partes) + "."
        else:
            resumo = (f"A Prefeitura não publicou dados novos desde o último boletim. Alvarás atualizados em "
                      f"{data_br(meta['geosampa_atualizacao'])}; vendas do ITBI até {meta['itbi_ultimo_mes'].lower()}. "
                      "Abaixo, oportunidades da base que valem um contato hoje.")
        numeros = [(str(n_alv), "alvarás novos"), (str(vn), "vendas novas"), (str(rn), "revendas novas")]
        blocos.append(secao("Alvarás novos", [item_html(ficha(e["id"]), e["end"], f"{_e(e['dist'])} · alvará de {data_br(e['def1'])}",
                                                         f"{e['his1'] + e['his2'] + e['hmp']} unidades HIS/HMP") for e in c["novos_alvaras"][:5]]))
        blocos.append(secao("Revendas registradas", [item_html(ficha(r["id"]), r["end"], f"{_e(r['dist'])} · {_e(r['un'])}",
                                                                f"Comprou por {brl(r['v0'])} ({mes_ano(r['d0'])}) e revendeu por {brl(r['v1'])} ({mes_ano(r['d1'])}) · <b>{vs_inflacao(r['real'])}</b>",
                                                                "ganho" if r["real"] >= 0 else "alerta") for r in c["revendas"]]))
        blocos.append(secao("Alertas: venda acima do teto", [item_html(ficha(a["id"]), a["end"], f"{_e(a['dist'])} · {_e(', '.join(a['unidades'][:3]))}{' e outras' if a['n'] > 3 else ''}",
                                                                        f"{plural(a['n'], 'venda nova', 'vendas novas')} acima do teto {a['categoria']} de {brl(a['teto'])} · <b>até {brl(a['maior'])} acima</b>", "alerta") for a in c["acima"]],
                            "Pode ser erro de cadastro. Confira antes de agir."))
        vistos |= {e["id"] for e in c["novos_alvaras"][:5]} | {r["id"] for r in c["revendas"]} | {a["id"] for a in c["acima"]}
        assunto = f"Radar HIS · {dia} · " + (", ".join(partes) if partes else "sem dados novos ontem · 3 oportunidades do dia")

    opp = rotativos([r for r in dest["revendas"] + dest["maiores_ganhos"] if oportunidade_plausivel(r)], 3, hoje, vistos)
    blocos.append(secao("Oportunidades do dia", [item_html(ficha(r["id"]), r["end"], f"{_e(r['dist'])} · {_e(r['un'])}",
                                                          f"{brl(r['v0'])} ({mes_ano(r['d0'])}) → {brl(r['v1'])} ({mes_ano(r['d1'])}) · <b>{vs_inflacao(r['real'])}</b>",
                                                          "ganho" if r["real"] >= 0 else "alerta") for r in opp],
                         "Unidades que já mostraram valorização. Toque para achar quem vende, ver a fachada ou pedir a certidão."))

    aviso = ""
    if auditoria["status"] == "alerta":
        itens = "; ".join(v["verificacao"] for v in auditoria["verificacoes"] if not v["ok"])
        aviso = f'<tr><td style="padding:12px 14px;background:{COR["alerta_fundo"]};color:{COR["alerta"]};font-family:{FONTE_TEXTO};font-size:13px;border-radius:8px">Aviso do Auditor: {_e(itens)}.</td></tr>'

    html_mail = f"""<!doctype html><html><body style="margin:0;padding:0;background:{COR['concreto']}">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:{COR['concreto']}"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width:600px;width:100%">
 <tr><td style="padding:0 0 14px;border-bottom:2px solid {COR['asfalto']}">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr>
   <td><img src="cid:att0" alt="Radar HIS" width="189" height="36" style="display:block;border:0"></td>
   <td align="right" style="font-family:{FONTE_DADO};font-size:12px;color:{COR['grafite']}">{data_br(hoje.isoformat())}</td>
  </tr></table>
 </td></tr>
 <tr><td style="padding:22px 0 6px;font-family:{FONTE_MARCA};font-weight:800;font-size:28px;line-height:1.15;color:{COR['asfalto']}">{_e(titulo)}</td></tr>
 <tr><td style="padding:0 0 14px;font-family:{FONTE_TEXTO};font-size:16px;line-height:1.5;color:{COR['asfalto']}">{_e(resumo)}</td></tr>
 {aviso}
 {numeros_html(numeros)}
 {''.join(blocos)}
 <tr><td align="center" style="padding:26px 0 10px"><a href="{link}" style="display:inline-block;background:{COR['asfalto']};color:#FFFFFF;font-family:{FONTE_TEXTO};font-weight:600;font-size:15px;text-decoration:none;padding:12px 22px;border-radius:10px">Abrir o Radar e perguntar</a></td></tr>
 <tr><td style="padding:18px 0 0;border-top:1px solid {COR['meio_fio']};font-family:{FONTE_DADO};font-size:11.5px;line-height:1.6;color:{COR['grafite']}">
  Fontes: alvarás HIS/HMP do GeoSampa (atualizado em {data_br(meta['geosampa_atualizacao'])}), guias de ITBI da Secretaria da Fazenda (até {meta['itbi_ultimo_mes'].lower()}), IPCA e CDI do Banco Central (até {meta['cdi_ultimo']}). Teto de preço: Decreto 64.895/2026.<br>
  Os dados públicos não trazem nome nem telefone de proprietários. Inteligência de mercado; não substitui consulta jurídica nem certidão de matrícula.
 </td></tr>
</table></td></tr></table></body></html>"""

    texto.append(f"{titulo} — {data_br(hoje.isoformat())}\n\n{resumo}\n")
    for nome, lista in ([("Oportunidades do dia", opp)] if c["primeiro"] else
                        [("Revendas registradas", c["revendas"]), ("Oportunidades do dia", opp)]):
        if lista:
            texto.append(nome.upper())
            texto += [f"- {r['end']} ({r['dist']}), {r['un']}: {brl(r['v0'])} → {brl(r['v1'])}, {vs_inflacao(r['real'])}. {ficha(r['id'])}" for r in lista]
            texto.append("")
    texto.append(f"Abrir o Radar: {link}")
    return {"assunto": assunto, "titulo": titulo, "resumo": resumo, "html": html_mail, "texto": "\n".join(texto),
            "comparacao": {k: (len(v) if isinstance(v, list) else v) for k, v in c.items()},
            "snapshot_novo": snapshot(emps, meta)}
