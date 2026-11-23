#!/usr/bin/env python3
"""Rotina diária do Radar HIS.

Agentes, em sequência:
  1. Coletor   (coletar.py)    baixa GeoSampa, ITBI e Banco Central
  2. Analista  (processar.py)  liga alvarás às vendas e gera os dados do site
  3. Auditor   (auditor.py)    confere a saída; pode bloquear a publicação
  4. Redator   (redator.py)    escreve o boletim comparando com a execução anterior
  5. Distribuidor              publica o site e envia o e-mail (feito pelo orquestrador,
                               conforme ROTINA_DIARIA.md, com as ferramentas de Artifact e Gmail)

Saídas: saida/boletim.json (para o Distribuidor), boletins/AAAA-MM-DD.html,
estado/snapshot.json (base de comparação do dia seguinte) e estado/execucoes.jsonl (registro).

Uso: python3 rotina_diaria.py [--sem-coleta]
"""
import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys
import time

import auditor
import redator

AQUI = pathlib.Path(__file__).resolve().parent


def escrever_json(caminho, obj):
    caminho.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def etapa(nome, comando):
    t = time.time()
    r = subprocess.run(comando, cwd=AQUI, capture_output=True, text=True)
    dur = round(time.time() - t, 1)
    print(f"[{nome}] {'ok' if r.returncode == 0 else 'FALHOU'} em {dur}s")
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-2000:])
    return {"agente": nome, "ok": r.returncode == 0, "segundos": dur, "saida": (r.stdout or "")[-800:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sem-coleta", action="store_true", help="reusa os dados já baixados em _dados")
    a = ap.parse_args()
    hoje = dt.date.today()
    inicio = dt.datetime.now().isoformat(timespec="seconds")
    config = json.loads((AQUI / "config.json").read_text(encoding="utf-8"))
    estado = AQUI / "estado"
    estado.mkdir(exist_ok=True)
    (AQUI / "boletins").mkdir(exist_ok=True)
    (AQUI / "saida").mkdir(exist_ok=True)
    arq_snap = estado / "snapshot.json"
    anterior = json.loads(arq_snap.read_text(encoding="utf-8")) if arq_snap.exists() else None

    etapas = []
    if not a.sem_coleta:
        etapas.append(etapa("Coletor", [sys.executable, "coletar.py", "--dados", "_dados"]))
    if all(e["ok"] for e in etapas):
        etapas.append(etapa("Analista", [sys.executable, "processar.py", "--dados", "_dados", "--saida", "site/dados"]))

    if not all(e["ok"] for e in etapas):
        auditoria = {"status": "bloqueado", "verificacoes": [{"verificacao": f"agente {e['agente']}", "ok": False, "gravidade": "bloqueio",
                                                               "detalhe": e["saida"][-300:]} for e in etapas if not e["ok"]]}
    else:
        auditoria = auditor.auditar(AQUI / "site" / "dados", anterior)
    print(f"[Auditor] {auditoria['status']}")

    boletim = None
    if auditoria["status"] != "bloqueado":
        boletim = redator.redigir(AQUI / "site" / "dados", anterior, auditoria, config, hoje)
        snap = boletim.pop("snapshot_novo")
        snap["boletim"] = hoje.isoformat()
        arq_snap.write_text(json.dumps(snap, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        (AQUI / "boletins" / f"{hoje.isoformat()}.html").write_text(boletim["html"], encoding="utf-8")
        escrever_json(AQUI / "boletins" / f"{hoje.isoformat()}.json", boletim["conteudo"])
        escrever_json(AQUI / "site" / "dados" / "boletim.json", boletim["conteudo"])
        historico = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((AQUI / "boletins").glob("*.json"), reverse=True)[:30]]
        escrever_json(AQUI / "site" / "dados" / "boletins.json",
                      [{k: b[k] for k in ("data", "assunto", "titulo", "resumo", "numeros")} for b in historico])
        print(f"[Redator] {boletim['assunto']}")

    saida = {
        "data": hoje.isoformat(), "status": auditoria["status"], "auditoria": auditoria,
        "destinatarios": config.get("destinatarios", []), "copia": config.get("copia", []),
        "assunto": boletim and boletim["assunto"], "html": boletim and boletim["html"], "texto": boletim and boletim["texto"],
        "site": {"file_path": str(AQUI / "site" / "index.html"), "root": str(AQUI / "site"),
                 "files": sorted(f"dados/{p.name}" for p in (AQUI / "site" / "dados").glob("*.json")), "url": config["link_radar"]},
    }
    (AQUI / "saida" / "boletim.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(estado / "execucoes.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"inicio": inicio, "fim": dt.datetime.now().isoformat(timespec="seconds"), "status": auditoria["status"],
                            "etapas": [{k: e[k] for k in ("agente", "ok", "segundos")} for e in etapas],
                            "falhas": [v["verificacao"] for v in auditoria["verificacoes"] if not v["ok"]],
                            "assunto": boletim and boletim["assunto"]}, ensure_ascii=False) + "\n")
    print("Saída para o Distribuidor: saida/boletim.json")
    return 0 if auditoria["status"] != "bloqueado" else 2


if __name__ == "__main__":
    sys.exit(main())
