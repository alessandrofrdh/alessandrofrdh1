"""Gestione centralizzata dei file e cartelle dei viaggi."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class TripRecord:
    trip_id: str
    name: str
    destination: str
    start_date: str
    creator_name: str
    folder_path: str
    created_at: str
    status: str = "active"
    tags: list[str] = None

    def __post_init__(self) -> None:
        if self.tags is None:
            self.tags = []


class ContentManager:
    """Gestisce la struttura di cartelle per i viaggi e i contenuti."""

    BASE_CONTENT_PATH = Path("content/trips")
    REGISTRY_FILE = Path("content/trips_registry.json")

    FOLDER_STRUCTURE = [
        "01_raw/photo",
        "01_raw/video",
        "01_raw/audio",
        "02_editing/photo_edit",
        "02_editing/video_edit",
        "02_editing/graphics",
        "03_approved/instagram",
        "03_approved/tiktok",
        "03_approved/youtube",
        "03_approved/facebook",
        "03_approved/linkedin",
        "04_published",
        "05_sponsorships/briefs",
        "05_sponsorships/deliverables",
        "06_reports",
        "07_briefs",
    ]

    def __init__(self, base_path: str | None = None) -> None:
        if base_path:
            self.BASE_CONTENT_PATH = Path(base_path)
        self.BASE_CONTENT_PATH.mkdir(parents=True, exist_ok=True)

    def create_trip(
        self,
        name: str,
        destination: str,
        start_date: str,
        creator_name: str,
        tags: list[str] | None = None,
    ) -> TripRecord:
        """Crea la struttura di cartelle per un nuovo viaggio."""
        safe_dest = destination.lower().replace(" ", "_")
        safe_date = start_date.replace("/", "-").replace(" ", "")
        trip_id = f"{safe_date}_{safe_dest}"
        trip_folder = self.BASE_CONTENT_PATH / trip_id

        for subfolder in self.FOLDER_STRUCTURE:
            (trip_folder / subfolder).mkdir(parents=True, exist_ok=True)

        record = TripRecord(
            trip_id=trip_id,
            name=name,
            destination=destination,
            start_date=start_date,
            creator_name=creator_name,
            folder_path=str(trip_folder),
            created_at=datetime.now().isoformat(),
            tags=tags or [],
        )

        self._write_info_file(trip_folder, record)
        self._register_trip(record)
        return record

    def get_trip(self, trip_id: str) -> TripRecord | None:
        registry = self._load_registry()
        data = registry.get(trip_id)
        if data:
            return TripRecord(**data)
        return None

    def list_trips(self, creator_name: str | None = None) -> list[TripRecord]:
        registry = self._load_registry()
        trips = [TripRecord(**v) for v in registry.values()]
        if creator_name:
            trips = [t for t in trips if t.creator_name == creator_name]
        return sorted(trips, key=lambda t: t.start_date, reverse=True)

    def get_trip_contents(self, trip_id: str) -> dict[str, list[str]]:
        """Restituisce i file presenti in ogni cartella del viaggio."""
        record = self.get_trip(trip_id)
        if not record:
            return {}

        trip_path = Path(record.folder_path)
        result: dict[str, list[str]] = {}
        for folder in self.FOLDER_STRUCTURE:
            folder_path = trip_path / folder
            if folder_path.exists():
                files = [f.name for f in folder_path.iterdir() if f.is_file()]
                if files:
                    result[folder] = files
        return result

    def move_to_approved(
        self,
        trip_id: str,
        source_subfolder: str,
        filename: str,
        platform: str,
    ) -> str | None:
        """Sposta un file da editing ad approved per una piattaforma."""
        record = self.get_trip(trip_id)
        if not record:
            return None

        trip_path = Path(record.folder_path)
        src = trip_path / source_subfolder / filename
        dst_dir = trip_path / "03_approved" / platform.lower()
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / filename

        if src.exists():
            src.rename(dst)
            return str(dst)
        return None

    def mark_published(self, trip_id: str, platform: str, filename: str) -> str | None:
        """Sposta un file da approved a published."""
        record = self.get_trip(trip_id)
        if not record:
            return None

        trip_path = Path(record.folder_path)
        src = trip_path / "03_approved" / platform.lower() / filename
        dst_dir = trip_path / "04_published"
        dst = dst_dir / f"{platform.lower()}_{filename}"

        if src.exists():
            src.rename(dst)
            return str(dst)
        return None

    def _write_info_file(self, trip_folder: Path, record: TripRecord) -> None:
        info = trip_folder / "INFO.md"
        info.write_text(
            f"# {record.name}\n\n"
            f"**ID:** {record.trip_id}\n"
            f"**Destinazione:** {record.destination}\n"
            f"**Data inizio:** {record.start_date}\n"
            f"**Creator:** {record.creator_name}\n"
            f"**Creato:** {record.created_at}\n"
            f"**Tag:** {', '.join(record.tags)}\n\n"
            f"## Struttura cartelle\n"
            f"- `01_raw/` — Materiale grezzo (foto, video, audio)\n"
            f"- `02_editing/` — Lavori in corso di editing\n"
            f"- `03_approved/` — Contenuti approvati per piattaforma\n"
            f"- `04_published/` — Contenuti già pubblicati\n"
            f"- `05_sponsorships/` — Materiali per sponsorizzazioni\n"
            f"- `06_reports/` — Report e analytics\n"
            f"- `07_briefs/` — Brief creativi e contratti\n",
            encoding="utf-8",
        )

    def _load_registry(self) -> dict[str, Any]:
        if self.REGISTRY_FILE.exists():
            return json.loads(self.REGISTRY_FILE.read_text(encoding="utf-8"))
        return {}

    def _register_trip(self, record: TripRecord) -> None:
        registry = self._load_registry()
        registry[record.trip_id] = asdict(record)
        self.REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.REGISTRY_FILE.write_text(
            json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8"
        )
