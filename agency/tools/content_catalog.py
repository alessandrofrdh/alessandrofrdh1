"""Catalogo contenuti — ricerca e inventario dei viaggi."""
from __future__ import annotations

import json
from pathlib import Path

REGISTRY_PATH = Path("content/trips_registry.json")


def _load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        return {}
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def search_trips(destination: str = "", creator: str = "", tag: str = "") -> str:
    registry = _load_registry()
    trips = list(registry.values())

    if destination:
        trips = [t for t in trips if destination.lower() in t.get("destination", "").lower()]
    if creator:
        trips = [t for t in trips if creator.lower() in t.get("creator_name", "").lower()]
    if tag:
        trips = [t for t in trips if tag.lower() in [x.lower() for x in t.get("tags", [])]]

    if not trips:
        return "Nessun viaggio trovato."
    lines = [f"Viaggi trovati: {len(trips)}"]
    for t in trips:
        lines.append(
            f"  [{t['trip_id']}]  {t['name']:<30}"
            f"  {t['destination']:<20}  {t['start_date']}  creator: {t['creator_name']}"
        )
    return "\n".join(lines)


def get_content_inventory(trip_id: str) -> str:
    registry = _load_registry()
    trip = registry.get(trip_id)
    if not trip:
        return f"Viaggio non trovato: {trip_id}"

    trip_path = Path(trip["folder_path"])
    if not trip_path.exists():
        return f"Cartella non trovata: {trip['folder_path']}"

    lines = [f"Inventario: {trip['name']} [{trip_id}]"]
    total = 0
    for subfolder in sorted(trip_path.iterdir()):
        if subfolder.is_dir():
            files = [f for f in subfolder.rglob("*") if f.is_file()]
            total += len(files)
            if files:
                lines.append(f"\n  {subfolder.name}/  ({len(files)} file)")
                for f in sorted(files)[:8]:
                    lines.append(f"    • {f.relative_to(subfolder)}")
                if len(files) > 8:
                    lines.append(f"    ... +{len(files)-8} altri")
    lines.append(f"\nTotale file: {total}")
    return "\n".join(lines)


def find_approved_content(platform: str = "", trip_id: str = "") -> str:
    registry = _load_registry()
    if trip_id:
        registry = {k: v for k, v in registry.items() if k == trip_id}

    results = []
    for tid, trip in registry.items():
        approved_path = Path(trip["folder_path"]) / "03_approved"
        if not approved_path.exists():
            continue
        if platform:
            pp = approved_path / platform.lower()
            if pp.exists():
                files = [f.name for f in pp.iterdir() if f.is_file()]
                if files:
                    results.append(f"  [{tid}] {platform}: {', '.join(files)}")
        else:
            for pdir in sorted(approved_path.iterdir()):
                if pdir.is_dir():
                    files = [f.name for f in pdir.iterdir() if f.is_file()]
                    if files:
                        results.append(f"  [{tid}] {pdir.name}: {', '.join(files)}")

    if not results:
        return "Nessun contenuto approvato trovato."
    return "Contenuti approvati:\n" + "\n".join(results)
