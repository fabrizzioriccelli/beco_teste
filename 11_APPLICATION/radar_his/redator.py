"""Agente Redator: escreve o boletim diário ("O que rolou ontem").

Compara os dados de hoje com o snapshot da execução anterior e gera um CONTEÚDO único
(título, resumo, números e seções). O mesmo conteúdo vira:
  - o e-mail (HTML com estilos inline, sem imagens) e a versão em texto;
  - a seção "Boletim" do site (site/dados/boletim.json).
"""
import datetime as dt
import html
import json
import pathlib
import re

# Paleta e tipografia da marca Faro v3 (04_DESIGN_SYSTEM/tokens.css)
COR = {"tinta": "#17302A", "tinta_texto": "#F4EFE6", "facho": "#B08D57", "facho_claro": "#C9A878", "facho_escuro": "#7D5F38",
       "texto": "#1A2622", "grafite": "#5B625D", "linha": "#DDD5C7", "pedra": "#E7E0D3", "travertino": "#EFEAE1", "papel": "#FBF9F5",
       "ganho": "#2D6A4F", "alerta": "#9E2B25", "alerta_fundo": "#F5E3DF"}
FONTE_MARCA = "'Bodoni Moda', 'Bodoni 72', Didot, 'Bodoni MT', Georgia, 'Times New Roman', serif"
FONTE_TEXTO = "Jost, Futura, 'Century Gothic', 'Helvetica Neue', Arial, sans-serif"
FONTE_DADO = FONTE_TEXTO
ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
MES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]


# ---------------------------------------------------------------- formatação
def brl(v):
    return "R$ " + f"{v:,.0f}".replace(",", ".")


def milhar(n):
    return f"{n:,}".replace(",", ".")


def plural(n, um, varios):
    return f"{n} {um if n == 1 else varios}"


def pct_curto(x):
    return ("+" if x >= 0 else "−") + f"{abs(x) * 100:.0f}%"


def data_br(iso):
    return "/".join(reversed(iso[:10].split("-"))) if iso else "—"


def mes_ano(iso):
    return f"{MES[int(iso[5:7]) - 1]}/{iso[2:4]}" if iso else "—"


def mes_extenso(aba_ou_ym):
    """'SET-2026' ou '2026-11' -> 'set/2026'."""
    if aba_ou_ym[:3].isalpha():
        return f"{aba_ou_ym[:3].lower()}/{aba_ou_ym[-4:]}"
    return f"{MES[int(aba_ou_ym[5:7]) - 1]}/{aba_ou_ym[:4]}"


PEQUENAS = {"da", "de", "do", "das", "dos", "e", "em", "na", "no", "nas", "nos"}
SIGLAS = {"HIS", "HMP", "SP", "BL", "AP", "APTO", "CJ", "CEP", "SQL"}
ROMANO = re.compile(r"^(X{0,3})(IX|IV|V?I{0,3})$")


def endereco(s):
    """Endereço da Prefeitura (muitas vezes em caixa alta) em grafia de título: 'Rua Major Ari Gomes, 29, Vila Mazzei'."""
    def palavra(m):
        w, k = m.group(0), m.start()
        u = w.upper()
        if u in SIGLAS or (len(u) > 1 and ROMANO.match(u)):
            return u
        if k > 0 and w.lower() in PEQUENAS:
            return w.lower()
        return w[:1].upper() + w[1:].lower()
    s = re.sub(r"\b0+(\d)", r"\1", s or "")
    s = re.sub(r"[A-Za-zÀ-ÿ]+", palavra, s)
    return s.replace("S/Nº", "s/nº").replace("S/N", "s/n")


def _e(s):
    return html.escape(str(s or ""))


# ---------------------------------------------------------------- comparação com o dia anterior
def snapshot(emps, meta):
    return {
        "gerado_em": meta["gerado_em"], "geosampa_atualizacao": meta["geosampa_atualizacao"],
        "itbi_ultimo_mes": meta["itbi_ultimo_mes"], "itbi_guias_lidas": meta["itbi_guias_lidas"],
        "itbi_ligadas": meta["itbi_ligadas"], "ipca_ultimo": meta["ipca_ultimo"], "totais": meta["totais"],
        "emps": {e["id"]: [e["itbi"]["n_vendas"], e["itbi"]["n_revendas"], e["itbi"]["n_acima_teto"]] for e in emps},
    }


def _novos_por_predio(lista, deltas):
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


def comparar(emps, dest, ant):
    if not ant:
        return {"primeiro": True}
    velhos = ant.get("emps", {})
    campos = ("n_vendas", "n_revendas", "n_acima_teto")
    delta = [{e["id"]: e["itbi"][campos[i]] - velhos[e["id"]][i] for e in emps if e["id"] in velhos} for i in range(3)]
    dv, dr, da = delta
    return {
        "primeiro": False,
        "novos_alvaras": sorted((e for e in emps if e["id"] not in velhos), key=lambda e: e["def1"] or "", reverse=True),
        "vendas_novas": sum(x for x in dv.values() if x > 0),
        "revendas_novas": sum(x for x in dr.values() if x > 0),
        "acima_novas": sum(x for x in da.values() if x > 0),
        "revendas": _novos_por_predio(dest["revendas"], dr)[:5],
        "acima": _agrupar_acima(_novos_por_predio(dest["acima_teto"], da))[:5],
    }


def oportunidade_plausivel(r):
    """Só pares de compra e revenda com cara de negócio real de apartamento e ganho acima da inflação."""
    return r["v0"] >= 100_000 and 0.6 <= r["v1"] / r["v0"] <= 1.8 and r["real"] >= 0.03


def rotativos(lista, n, hoje, excluir):
    """Escolhe n itens diferentes a cada dia, para o boletim nunca vir vazio."""
    lista = [x for x in lista if x["id"] not in excluir]
    if not lista:
        return []
    k = hoje.toordinal() % len(lista)
    return (lista[k:] + lista[:k])[:n]


# ---------------------------------------------------------------- conteúdo
def _item_revenda(r):
    return {"id": r["id"], "titulo": endereco(r["end"]), "contexto": f"{r['dist']} · {r['un']}",
            "detalhe": f"Comprou por {brl(r['v0'])} ({mes_ano(r['d0'])}) e revendeu por {brl(r['v1'])} ({mes_ano(r['d1'])}).",
            "destaque": pct_curto(r["real"]), "destaque_rotulo": "acima da inflação" if r["real"] >= 0 else "abaixo da inflação",
            "tom": "ganho" if r["real"] >= 0 else "alerta"}


def _item_alvara(e):
    u = e["his1"] + e["his2"] + e["hmp"]
    partes = [f"{e['his1']} HIS-1" if e["his1"] else "", f"{e['his2']} HIS-2" if e["his2"] else "", f"{e['hmp']} HMP" if e["hmp"] else ""]
    return {"id": e["id"], "titulo": endereco(e["end"]), "contexto": f"{e['dist']} · alvará de {data_br(e['def1'])}",
            "detalhe": " · ".join(p for p in partes if p) or "Unidades não informadas no alvará.",
            "destaque": milhar(u), "destaque_rotulo": "unidades", "tom": "neutro"}


def _item_acima(a):
    return {"id": a["id"], "titulo": endereco(a["end"]), "contexto": f"{a['dist']} · {', '.join(a['unidades'][:3])}{' e outras' if a['n'] > 3 else ''}",
            "detalhe": f"{plural(a['n'], 'venda nova', 'vendas novas')} acima do teto {a['categoria']} de {brl(a['teto'])}.",
            "destaque": "+" + brl(a["maior"]), "destaque_rotulo": "acima do teto", "tom": "alerta"}


def conteudo_do_dia(emps, dest, meta, ant, auditoria, config, hoje):
    c = comparar(emps, dest, ant)
    t = meta["totais"]
    secoes, vistos, partes = [], set(), []
    if c["primeiro"]:
        tipo, titulo = "panorama", "O mapa completo, para começar"
        resumo = (f"Este é o primeiro boletim. O Faro acompanha {milhar(t['empreendimentos'])} prédios com alvará HIS/HMP na capital, "
                  f"com {milhar(t['vendas'])} primeiras vendas e {milhar(t['revendas'])} revendas registradas no ITBI. "
                  "A partir de amanhã, chega aqui só o que mudou de um dia para o outro.")
        numeros = [{"valor": milhar(t["empreendimentos"]), "rotulo": "prédios HIS/HMP"},
                   {"valor": milhar(t["revendas"]), "rotulo": "revendas registradas"},
                   {"valor": milhar(t["acima_teto"]), "rotulo": "vendas acima do teto"}]
        itens = [_item_alvara(e) for e in sorted(emps, key=lambda e: e["def1"] or "", reverse=True)[:3]]
        secoes.append({"titulo": "Alvarás mais recentes", "nota": f"Últimos publicados pela Prefeitura (até {data_br(meta['ultimo_deferimento'])}).", "itens": itens})
        vistos |= {i["id"] for i in itens}
    else:
        tipo, titulo = "diario", "O que rolou ontem"
        n_alv = len(c["novos_alvaras"])
        partes = [x for x in [
            n_alv and plural(n_alv, "alvará HIS/HMP novo", "alvarás HIS/HMP novos"),
            c["vendas_novas"] and plural(c["vendas_novas"], "venda nova", "vendas novas"),
            c["revendas_novas"] and plural(c["revendas_novas"], "revenda", "revendas"),
            c["acima_novas"] and plural(c["acima_novas"], "venda acima do teto", "vendas acima do teto")] if x]
        if partes:
            resumo = "Desde o último boletim: " + (", ".join(partes[:-1]) + " e " if len(partes) > 1 else "") + partes[-1] + "."
        else:
            resumo = (f"A Prefeitura não publicou dados novos desde o último boletim (alvarás de {data_br(meta['geosampa_atualizacao'])}; "
                      f"vendas do ITBI até {mes_extenso(meta['itbi_ultimo_mes'])}). Separamos oportunidades da base que valem um contato hoje.")
        numeros = [{"valor": str(n_alv), "rotulo": "alvarás novos"}, {"valor": str(c["revendas_novas"]), "rotulo": "revendas novas"},
                   {"valor": str(c["acima_novas"]), "rotulo": "alertas de teto"}]
        if n_alv:
            itens = [_item_alvara(e) for e in c["novos_alvaras"][:5]]
            secoes.append({"titulo": "Alvarás novos", "nota": "Prédios HIS/HMP licenciados que ainda não estavam no Faro.", "itens": itens})
            vistos |= {i["id"] for i in itens}
        if c["revendas"]:
            secoes.append({"titulo": "Revendas registradas", "nota": "Unidades que trocaram de dono, com o ganho já descontada a inflação.",
                           "itens": [_item_revenda(r) for r in c["revendas"]]})
            vistos |= {r["id"] for r in c["revendas"]}
        if c["acima"]:
            secoes.append({"titulo": "Alertas de teto", "nota": "Vendas acima do preço máximo da lei. Pode ser erro de cadastro: confira antes de agir.",
                           "itens": [_item_acima(a) for a in c["acima"]]})
            vistos |= {a["id"] for a in c["acima"]}
    opp = rotativos([r for r in dest["revendas"] + dest["maiores_ganhos"] if oportunidade_plausivel(r)], 3, hoje, vistos)
    if opp:
        secoes.append({"titulo": "Oportunidades do dia", "nota": "Unidades que já valorizaram acima da inflação. Toque para achar quem vende.",
                       "itens": [_item_revenda(r) for r in opp]})
    falhas = [v["verificacao"] for v in auditoria["verificacoes"] if not v["ok"]]
    dia = data_br(hoje.isoformat())
    if tipo == "panorama":
        assunto = f"Faro · {dia[:5]} · o mapa completo: {milhar(t['empreendimentos'])} prédios HIS/HMP"
    else:
        assunto = f"Faro · {dia[:5]} · " + (", ".join(partes) if partes else "sem dados novos ontem · 3 oportunidades do dia")
    return {
        "data": hoje.isoformat(), "tipo": tipo, "assunto": assunto,
        "rotulo": f"Boletim de {DIAS[hoje.weekday()]}, {dia}",
        "titulo": titulo, "resumo": resumo, "numeros": numeros, "secoes": secoes,
        "aviso": ("Aviso do Auditor: " + "; ".join(falhas) + ".") if auditoria["status"] == "alerta" else None,
        "fontes": (f"Alvarás HIS/HMP do GeoSampa (atualizado em {data_br(meta['geosampa_atualizacao'])}); guias de ITBI da Secretaria da Fazenda "
                   f"(até {mes_extenso(meta['itbi_ultimo_mes'])}); IPCA e CDI do Banco Central (até {mes_extenso(meta['cdi_ultimo'])}); "
                   "teto de preço pelo Decreto 64.895/2026."),
        "link": config["link_radar"], "link_boletim": config["link_radar"] + "#boletim",
    }


# ---------------------------------------------------------------- e-mail
ROTULO = f"font-family:{FONTE_DADO};font-size:11px;font-weight:500;letter-spacing:2.4px;text-transform:uppercase"


def logo_html(negativo=True):
    """Assinatura Faro em texto (sem imagem): FARO em Bodoni com versais espaçadas e o descritor em latão."""
    cor = COR["tinta_texto"] if negativo else COR["tinta"]
    desc = COR["facho_claro"] if negativo else COR["facho_escuro"]
    return (f'<div style="font-family:{FONTE_MARCA};font-weight:500;font-size:27px;line-height:1;letter-spacing:7px;color:{cor}">FARO</div>'
            f'<div style="{ROTULO};font-size:8.5px;letter-spacing:3px;color:{desc};padding-top:7px">Inteligência imobiliária</div>')


def _rotulo_secao(n, titulo):
    num = ROMANOS[n - 1] if n <= len(ROMANOS) else str(n)
    return (f'<tr><td style="padding:34px 0 8px;{ROTULO};color:{COR["facho_escuro"]};border-bottom:1px solid {COR["linha"]}">'
            f'<span style="font-family:{FONTE_MARCA};font-size:15px;letter-spacing:0;text-transform:none">{num}</span> &nbsp;·&nbsp; {_e(titulo)}</td></tr>')


def _item_email(i, link):
    cor = {"ganho": COR["ganho"], "alerta": COR["alerta"]}.get(i["tom"], COR["tinta"])
    return f"""<tr><td style="padding:18px 0;border-bottom:1px solid {COR['linha']}">
 <table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr>
  <td valign="top" style="width:18px;padding-top:4px;font-size:9px;line-height:14px;color:{COR['facho']}">&#9670;</td>
  <td valign="top">
   <div style="font-family:{FONTE_MARCA};font-weight:500;font-size:18px;line-height:1.3;color:{COR['tinta']}">{_e(i['titulo'])}</div>
   <div style="{ROTULO};font-size:10.5px;letter-spacing:1.6px;color:{COR['grafite']};padding-top:4px">{_e(i['contexto'])}</div>
   <div style="font-family:{FONTE_TEXTO};font-size:14.5px;line-height:1.5;color:{COR['texto']};padding-top:8px">{_e(i['detalhe'])}</div>
   <div style="padding-top:10px"><a href="{link}#imovel-{i['id']}" style="{ROTULO};font-size:11px;letter-spacing:1.8px;color:{COR['facho_escuro']};text-decoration:none">Ver contatos e detalhes &rarr;</a></div>
  </td>
  <td valign="top" align="right" style="width:120px;padding-left:12px">
   <div style="font-family:{FONTE_MARCA};font-weight:500;font-size:28px;line-height:1.05;color:{cor};white-space:nowrap">{_e(i['destaque'])}</div>
   <div style="font-family:{FONTE_TEXTO};font-size:11.5px;color:{COR['grafite']};padding-top:4px">{_e(i['destaque_rotulo'])}</div>
  </td>
 </tr></table>
</td></tr>"""


def render_email(c):
    nums = "".join(
        f"""<td width="{100 // len(c['numeros'])}%" valign="top" style="padding:18px 12px 18px {'16px;border-left:1px solid ' + COR['linha'] if k else '0'}">
   <div style="font-family:{FONTE_MARCA};font-weight:500;font-size:42px;line-height:1;white-space:nowrap;color:{COR['tinta']}">{_e(n['valor'])}</div>
   <div style="{ROTULO};font-size:10px;letter-spacing:1.8px;color:{COR['grafite']};padding-top:8px">{_e(n['rotulo'])}</div></td>"""
        for k, n in enumerate(c["numeros"]))
    secoes = "".join(_rotulo_secao(k + 1, s["titulo"]) +
                     (f'<tr><td style="padding:10px 0 2px;font-family:{FONTE_TEXTO};font-size:13px;color:{COR["grafite"]}">{_e(s["nota"])}</td></tr>' if s.get("nota") else "") +
                     "".join(_item_email(i, c["link"]) for i in s["itens"]) for k, s in enumerate(c["secoes"]))
    aviso = (f'<tr><td style="padding:12px 14px;background:{COR["alerta_fundo"]};color:{COR["alerta"]};font-family:{FONTE_TEXTO};font-size:13px">{_e(c["aviso"])}</td></tr>'
             if c.get("aviso") else "")
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,500&family=Jost:wght@400;500&display=swap" rel="stylesheet"></head>
<body style="margin:0;padding:0;background:{COR['travertino']}">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:{COR['travertino']}"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width:600px;width:100%">
 <tr><td style="background:{COR['tinta']};padding:24px 28px;border-bottom:1px solid {COR['facho']}">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr>
   <td valign="middle">{logo_html(negativo=True)}</td>
   <td align="right" valign="middle" style="{ROTULO};font-size:10.5px;color:{COR['facho_claro']}">{data_br(c['data'])}</td>
  </tr></table>
 </td></tr>
 <tr><td style="background:{COR['papel']};padding:36px 32px 10px">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
   <tr><td style="{ROTULO};color:{COR['facho_escuro']}">{_e(c['rotulo'])}</td></tr>
   <tr><td style="padding:14px 0 12px;font-family:{FONTE_MARCA};font-weight:500;font-size:42px;line-height:1.04;color:{COR['tinta']}">{_e(c['titulo'])}</td></tr>
   <tr><td style="padding:0 0 18px;font-family:{FONTE_TEXTO};font-size:16px;line-height:1.6;color:{COR['texto']}">{_e(c['resumo'])}</td></tr>
   {aviso}
   <tr><td style="border-top:1px solid {COR['facho']};border-bottom:1px solid {COR['linha']}"><table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr>{nums}</tr></table></td></tr>
   {secoes}
   <tr><td align="left" style="padding:32px 0 30px">
    <a href="{c['link_boletim']}" style="display:inline-block;background:{COR['tinta']};color:{COR['tinta_texto']};{ROTULO};font-size:12px;letter-spacing:2.4px;text-decoration:none;padding:16px 26px">Abrir o Faro &rarr;</a>
    <div style="font-family:{FONTE_TEXTO};font-size:13px;color:{COR['grafite']};padding-top:10px">Mapa, fichas e contatos de cada prédio. Pergunte o que quiser.</div>
   </td></tr>
  </table>
 </td></tr>
 <tr><td style="padding:18px 6px 0;font-family:{FONTE_TEXTO};font-size:11px;line-height:1.7;color:{COR['grafite']}">
  {_e(c['fontes'])}<br>Os dados públicos não trazem nome nem telefone de proprietários. Inteligência de mercado; não substitui consulta jurídica nem certidão de matrícula.
 </td></tr>
</table></td></tr></table></body></html>"""


def render_texto(c):
    linhas = [f"{c['titulo'].upper()} — {data_br(c['data'])}", "", c["resumo"], ""]
    linhas += [f"{n['valor']} {n['rotulo']}" for n in c["numeros"]] + [""]
    for k, s in enumerate(c["secoes"], 1):
        linhas.append(f"{k:02d} — {s['titulo'].upper()}")
        linhas += [f"- {i['titulo']} ({i['contexto']}): {i['detalhe'].rstrip('.')}. {i['destaque']} {i['destaque_rotulo']}. {c['link']}#imovel-{i['id']}" for i in s["itens"]]
        linhas.append("")
    linhas += [f"Abrir o Faro: {c['link_boletim']}", "", c["fontes"]]
    return "\n".join(linhas)


def redigir(pasta_dados, snapshot_anterior, auditoria, config, hoje=None):
    hoje = hoje or dt.date.today()
    pasta = pathlib.Path(pasta_dados)
    emps = json.loads((pasta / "empreendimentos.json").read_text(encoding="utf-8"))
    dest = json.loads((pasta / "destaques.json").read_text(encoding="utf-8"))
    meta = json.loads((pasta / "meta.json").read_text(encoding="utf-8"))
    c = conteudo_do_dia(emps, dest, meta, snapshot_anterior, auditoria, config, hoje)
    return {"assunto": c["assunto"], "conteudo": c, "html": render_email(c), "texto": render_texto(c),
            "snapshot_novo": snapshot(emps, meta)}
