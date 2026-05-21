"""Registro brand e deal — database JSON persistente."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

REGISTRY_PATH = Path("agency/storage/brand_registry.json")


def _load() -> dict:
    if REGISTRY_PATH.exists():
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {"brands": {}, "deals": []}


def _save(data: dict) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def register_brand(name: str, contact: str, niche: str, budget_range: str, notes: str = "") -> str:
    data = _load()
    data["brands"][name] = {
        "nome": name,
        "contatto": contact,
        "nicchia": niche,
        "budget_range": budget_range,
        "note": notes,
        "registrato": datetime.now().isoformat(),
    }
    _save(data)
    return f"Brand registrato: {name}  ({niche}, budget: {budget_range})"


def get_brand(name: str) -> str:
    data = _load()
    brand = data["brands"].get(name)
    if not brand:
        return f"Brand non trovato: {name}"
    return json.dumps(brand, indent=2, ensure_ascii=False)


def list_brands(niche: str = "") -> str:
    data = _load()
    brands = list(data["brands"].values())
    if niche:
        brands = [b for b in brands if niche.lower() in b.get("nicchia", "").lower()]
    if not brands:
        return "Nessun brand registrato."
    lines = [f"Brand registrati: {len(brands)}"]
    for b in brands:
        lines.append(f"  • {b['nome']:<25} {b['nicchia']:<20} budget: {b['budget_range']}")
    return "\n".join(lines)


def log_deal(
    brand: str,
    creator: str,
    deal_type: str,
    fee: float,
    status: str,
    notes: str = "",
) -> str:
    data = _load()
    deal = {
        "id": f"deal_{len(data['deals'])+1:04d}",
        "brand": brand,
        "creator": creator,
        "tipo": deal_type,
        "fee": fee,
        "status": status,
        "note": notes,
        "data": datetime.now().isoformat(),
    }
    data["deals"].append(deal)
    _save(data)
    return f"Deal registrato: {deal['id']}  {brand} × {creator}  €{fee:,.0f}  [{status}]"


def get_deal_history(brand: str = "", creator: str = "") -> str:
    data = _load()
    deals = data["deals"]
    if brand:
        deals = [d for d in deals if d["brand"].lower() == brand.lower()]
    if creator:
        deals = [d for d in deals if d["creator"].lower() == creator.lower()]
    if not deals:
        return "Nessun deal trovato."
    lines = [f"Deal trovati: {len(deals)}"]
    for d in deals:
        lines.append(
            f"  [{d['id']}]  {d['brand']} × {d['creator']}"
            f"  {d['tipo']}  €{d['fee']:,.0f}  [{d['status']}]"
        )
    return "\n".join(lines)


def update_deal_status(deal_id: str, status: str, notes: str = "") -> str:
    data = _load()
    for deal in data["deals"]:
        if deal["id"] == deal_id:
            deal["status"] = status
            if notes:
                deal["note"] = notes
            deal["aggiornato"] = datetime.now().isoformat()
            _save(data)
            return f"Deal {deal_id} aggiornato → {status}"
    return f"Deal non trovato: {deal_id}"
