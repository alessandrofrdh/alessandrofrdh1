"""Strumenti per leggere, scrivere e organizzare file nei viaggi."""
from __future__ import annotations

from pathlib import Path

BASE_TRIPS = Path("content/trips")


def read_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return f"Errore: file non trovato: {path}"
    try:
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return f"Errore lettura: {e}"


def write_file(path: str, content: str) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"File scritto: {path} ({len(content)} caratteri)"


def list_files(folder: str) -> str:
    fp = Path(folder)
    if not fp.exists():
        return f"Cartella non trovata: {folder}"
    lines = []
    for item in sorted(fp.iterdir()):
        if item.is_file():
            lines.append(f"  [file] {item.name} ({item.stat().st_size} B)")
        elif item.is_dir():
            count = sum(1 for _ in item.iterdir())
            lines.append(f"  [dir]  {item.name}/ ({count} elementi)")
    return "\n".join(lines) if lines else "Cartella vuota."


def move_file(source: str, destination: str) -> str:
    src = Path(source)
    dst = Path(destination)
    if not src.exists():
        return f"Errore: file non trovato: {source}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dst)
    return f"Spostato: {source} → {destination}"


def save_brief(trip_id: str, content: str, filename: str = "brief.md") -> str:
    path = BASE_TRIPS / trip_id / "07_briefs" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"Brief salvato: {path}"


def save_report(trip_id: str, content: str, filename: str = "report.md") -> str:
    path = BASE_TRIPS / trip_id / "06_reports" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"Report salvato: {path}"


def list_trip_structure(trip_id: str) -> str:
    trip_path = BASE_TRIPS / trip_id
    if not trip_path.exists():
        return f"Viaggio non trovato: {trip_id}"
    lines = [f"[{trip_id}]"]
    for item in sorted(trip_path.iterdir()):
        if item.is_dir():
            files = [f for f in item.rglob("*") if f.is_file()]
            lines.append(f"  {item.name}/  ({len(files)} file)")
            for sub in sorted(item.iterdir()):
                if sub.is_dir():
                    n = sum(1 for f in sub.iterdir() if f.is_file())
                    lines.append(f"    {sub.name}/  ({n} file)")
                elif sub.is_file():
                    lines.append(f"    {sub.name}")
        elif item.is_file():
            lines.append(f"  {item.name}")
    return "\n".join(lines)
