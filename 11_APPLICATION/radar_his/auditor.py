"""Agente Auditor: confere a saída do Analista antes de publicar ou enviar qualquer coisa.

Status: "ok" (segue), "alerta" (segue, mas o boletim avisa) ou "bloqueado" (não publica nem envia).
"""
import json
import pathlib

ARQUIVOS = ["meta.json", "empreendimentos.json", "destaques.json", "indices.json", "distritos.json"]
MESES = "JAN FEV MAR ABR MAI JUN JUL AGO SET OUT NOV DEZ".split()


def _mes(aba):
    return (int(aba[-4:]), MESES.index(aba[:3]) + 1) if aba else (0, 0)


def auditar(pasta_dados, snapshot_anterior):
    pasta = pathlib.Path(pasta_dados)
    checks = []

    def registrar(nome, ok, gravidade, detalhe):
        checks.append({"verificacao": nome, "ok": bool(ok), "gravidade": gravidade, "detalhe": detalhe})

    faltando = [a for a in ARQUIVOS if not (pasta / a).exists() or (pasta / a).stat().st_size < 50]
    registrar("arquivos gerados", not faltando, "bloqueio", f"faltando: {faltando}" if faltando else "todos presentes")
    if faltando:
        return {"status": "bloqueado", "verificacoes": checks}

    meta = json.loads((pasta / "meta.json").read_text(encoding="utf-8"))
    t = meta["totais"]
    registrar("prédios carregados", t["empreendimentos"] > 1000, "bloqueio", f"{t['empreendimentos']} prédios")
    registrar("guias de ITBI lidas", meta["itbi_guias_lidas"] > 1_000_000, "bloqueio", f"{meta['itbi_guias_lidas']} guias")

    ant = snapshot_anterior or {}
    if ant:
        ta = ant.get("totais", {})
        registrar("prédios não caíram", t["empreendimentos"] >= 0.95 * ta.get("empreendimentos", 0), "bloqueio",
                  f"{ta.get('empreendimentos')} → {t['empreendimentos']}")
        registrar("guias de ITBI não caíram", meta["itbi_guias_lidas"] >= 0.98 * ant.get("itbi_guias_lidas", 0), "bloqueio",
                  f"{ant.get('itbi_guias_lidas')} → {meta['itbi_guias_lidas']}")
        registrar("mês do ITBI não voltou", _mes(meta["itbi_ultimo_mes"]) >= _mes(ant.get("itbi_ultimo_mes")), "alerta",
                  f"{ant.get('itbi_ultimo_mes')} → {meta['itbi_ultimo_mes']}")
        registrar("data dos alvarás não voltou", meta["geosampa_atualizacao"] >= ant.get("geosampa_atualizacao", ""), "alerta",
                  f"{ant.get('geosampa_atualizacao')} → {meta['geosampa_atualizacao']}")
        salto = t["acima_teto"] - ta.get("acima_teto", 0)
        registrar("vendas acima do teto sem salto anormal", salto <= 50, "alerta", f"+{salto} desde o último boletim")
        ligadas_ant = ant.get("itbi_ligadas", 0)
        registrar("ligação alvará-venda estável", meta["itbi_ligadas"] >= 0.8 * ligadas_ant, "alerta", f"{ligadas_ant} → {meta['itbi_ligadas']}")
    registrar("índices do Banco Central atuais", meta["ipca_ultimo"] >= (ant.get("ipca_ultimo") or ""), "alerta",
              f"IPCA até {meta['ipca_ultimo']}, CDI até {meta['cdi_ultimo']}")

    falhas = [c for c in checks if not c["ok"]]
    status = "bloqueado" if any(c["gravidade"] == "bloqueio" for c in falhas) else ("alerta" if falhas else "ok")
    return {"status": status, "verificacoes": checks}
