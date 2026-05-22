"""Tracker delle performance settimanali — usato dal proprietario per validare il lavoro."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

TRACKER_FILE = Path("agency/storage/performance_tracker.json")

REQUIRED_METRICS = ["follower_ig", "follower_tiktok", "follower_youtube",
                    "engagement_rate", "reach", "impressions", "conversioni"]


def _load() -> dict:
    if TRACKER_FILE.exists():
        return json.loads(TRACKER_FILE.read_text(encoding="utf-8"))
    return {"weeks": {}, "payments": [], "baseline": None}


def _save(data: dict) -> None:
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    TRACKER_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def log_weekly_metrics(week: int, metrics: dict, notes: str = "") -> str:
    """Registra le metriche di una settimana."""
    data = _load()

    # Prima settimana = baseline
    if data["baseline"] is None and week == 1:
        data["baseline"] = metrics.copy()

    data["weeks"][str(week)] = {
        "settimana": week,
        "metriche": metrics,
        "note": notes,
        "registrato": datetime.now().isoformat(),
    }
    _save(data)

    lines = [f"Metriche settimana {week} registrate:"]
    for k, v in metrics.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)


def get_weekly_metrics(week: int) -> str:
    data = _load()
    entry = data["weeks"].get(str(week))
    if not entry:
        return f"Nessun dato per la settimana {week}."
    lines = [f"Settimana {week}:"]
    for k, v in entry["metriche"].items():
        lines.append(f"  {k}: {v}")
    if entry.get("note"):
        lines.append(f"  Note: {entry['note']}")
    return "\n".join(lines)


def calculate_weekly_growth(week: int) -> str:
    """Calcola la crescita % rispetto alla settimana precedente."""
    if week < 2:
        return f"Settimana {week}: prima settimana, nessun confronto possibile (questa è la baseline)."

    data = _load()
    current = data["weeks"].get(str(week), {}).get("metriche")
    previous = data["weeks"].get(str(week - 1), {}).get("metriche")

    if not current:
        return f"Nessun dato per la settimana {week}."
    if not previous:
        return f"Nessun dato per la settimana {week - 1} (confronto non possibile)."

    lines = [f"Crescita settimana {week} vs settimana {week - 1}:"]
    all_above_target = True
    any_negative = False

    for key in current:
        if key not in previous:
            continue
        prev_val = float(previous[key]) if previous[key] else 0
        curr_val = float(current[key]) if current[key] else 0

        if prev_val == 0:
            growth_pct = 0.0
        else:
            growth_pct = ((curr_val - prev_val) / prev_val) * 100

        target_met = growth_pct >= 10.0
        status = "✓" if target_met else "✗"
        if not target_met:
            all_above_target = False
        if growth_pct < 0:
            any_negative = True

        lines.append(
            f"  {status} {key:<22} {prev_val:>10} → {curr_val:>10}  "
            f"({growth_pct:+.1f}%  target: +10%)"
        )

    verdict = "TUTTE LE METRICHE AL TARGET" if all_above_target else "ALCUNE METRICHE SOTTO TARGET"
    lines.append(f"\nVerdetto: {verdict}")
    if any_negative:
        lines.append("⚠️  Alcune metriche sono in CALO — situazione critica.")
    return "\n".join(lines)


def check_growth_target(week: int, target_pct: float = 10.0) -> str:
    """Verifica se la settimana ha raggiunto il target minimo su TUTTE le metriche chiave."""
    if week < 2:
        return f"Settimana {week}: baseline — nessun target applicabile."

    data = _load()
    current = data["weeks"].get(str(week), {}).get("metriche", {})
    previous = data["weeks"].get(str(week - 1), {}).get("metriche", {})

    if not current or not previous:
        return "Dati insufficienti per la verifica."

    failed = []
    passed = []

    for key in current:
        if key not in previous:
            continue
        prev_val = float(previous[key]) if previous[key] else 0
        curr_val = float(current[key]) if current[key] else 0
        if prev_val == 0:
            continue
        growth = ((curr_val - prev_val) / prev_val) * 100
        if growth >= target_pct:
            passed.append(f"{key}: +{growth:.1f}%")
        else:
            failed.append(f"{key}: +{growth:.1f}% (mancano {target_pct - growth:.1f}%)")

    if not failed:
        return (
            f"✅ SETTIMANA {week}: TARGET RAGGIUNTO\n"
            f"Tutte le {len(passed)} metriche superano il +{target_pct}%:\n"
            + "\n".join(f"  ✓ {p}" for p in passed)
        )
    else:
        return (
            f"❌ SETTIMANA {week}: TARGET NON RAGGIUNTO\n"
            f"Metriche sotto il +{target_pct}%:\n"
            + "\n".join(f"  ✗ {f}" for f in failed)
            + f"\nMetriche al target ({len(passed)}):\n"
            + "\n".join(f"  ✓ {p}" for p in passed)
        )


def get_performance_history() -> str:
    """Storico completo di tutte le settimane."""
    data = _load()
    if not data["weeks"]:
        return "Nessun dato registrato ancora."

    lines = [f"Storico performance ({len(data['weeks'])} settimane):"]
    for wk in sorted(data["weeks"].keys(), key=int):
        entry = data["weeks"][wk]
        metrics = entry["metriche"]
        lines.append(f"\n  Settimana {wk}:")
        for k, v in metrics.items():
            lines.append(f"    {k}: {v}")

    lines.append(f"\nPagamenti registrati: {len(data['payments'])}")
    return "\n".join(lines)


def log_payment_decision(
    week: int,
    approved: bool,
    reason: str,
    amount_eur: float = 0.0,
) -> str:
    """Registra la decisione di pagamento del proprietario."""
    data = _load()
    decision = {
        "settimana": week,
        "approvato": approved,
        "importo_eur": amount_eur if approved else 0.0,
        "motivo": reason,
        "data": datetime.now().isoformat(),
    }
    data["payments"].append(decision)
    _save(data)

    if approved:
        return (
            f"💳 PAGAMENTO APPROVATO — Settimana {week}\n"
            f"   Importo: €{amount_eur:,.2f}\n"
            f"   Motivo: {reason}"
        )
    else:
        return (
            f"🚫 PAGAMENTO RIFIUTATO — Settimana {week}\n"
            f"   Importo trattenuto: €{amount_eur:,.2f}\n"
            f"   Motivo: {reason}"
        )


def get_unpaid_weeks() -> str:
    """Elenca le settimane con pagamento rifiutato o mancante."""
    data = _load()
    weeks_with_data = set(data["weeks"].keys())
    paid_weeks = {str(p["settimana"]) for p in data["payments"] if p["approvato"]}
    refused_weeks = {str(p["settimana"]) for p in data["payments"] if not p["approvato"]}
    unpaid = weeks_with_data - paid_weeks

    if not unpaid:
        return "Nessuna settimana con pagamento in sospeso."

    lines = [f"Settimane non pagate / in sospeso: {len(unpaid)}"]
    for wk in sorted(unpaid, key=int):
        status = "RIFIUTATO" if wk in refused_weeks else "in attesa di valutazione"
        lines.append(f"  Settimana {wk}: {status}")
    return "\n".join(lines)
