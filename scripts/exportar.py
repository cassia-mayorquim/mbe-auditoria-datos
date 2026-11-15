#!/usr/bin/env python3
"""Convierte la exportación de la base del artifact (export/<colección>/<id>.json)
en los archivos que lee la versión pública: data/topics.json, items.json,
anmat.json, normativa.json y meta.json.

Uso:  python3 -I scripts/exportar.py export data
"""
import json, os, sys

src = sys.argv[1] if len(sys.argv) > 1 else "export"
dst = sys.argv[2] if len(sys.argv) > 2 else "data"
os.makedirs(dst, exist_ok=True)

def leer(col):
    d = os.path.join(src, col)
    out = []
    if not os.path.isdir(d):
        return out
    for f in sorted(os.listdir(d)):
        if not f.endswith(".json"):
            continue
        with open(os.path.join(d, f), encoding="utf-8") as fh:
            doc = json.load(fh)
        data = doc.get("data", doc)
        doc_id = doc.get("id") or f[:-5]
        out.append({"id": doc_id, **data})
    return out

def guardar(nombre, valor):
    with open(os.path.join(dst, nombre), "w", encoding="utf-8") as fh:
        json.dump(valor, fh, ensure_ascii=False, separators=(",", ":"))

topics = sorted(leer("topics"), key=lambda t: t.get("order") or 0)
por_fecha = lambda xs: sorted(xs, key=lambda x: x.get("date") or "", reverse=True)
items = por_fecha(leer("items"))[:1000]
anmat = por_fecha(leer("anmat"))[:300]
normativa = por_fecha(leer("normativa"))[:300]
meta = next((m for m in leer("meta") if m["id"] == "status"), {})
meta.pop("id", None)

guardar("topics.json", topics)
guardar("items.json", items)
guardar("anmat.json", anmat)
guardar("normativa.json", normativa)
guardar("meta.json", meta)
print(f"topics={len(topics)} items={len(items)} anmat={len(anmat)} normativa={len(normativa)}")
