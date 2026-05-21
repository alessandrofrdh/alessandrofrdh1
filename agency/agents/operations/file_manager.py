"""File Manager — organizzazione file e cartelle dei viaggi."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class FileManagerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.FILE_MANAGER,
            name="Marta Toscano",
            department="Operations",
            specializations=[
                "organizzazione file system",
                "naming convention",
                "backup strategy",
                "gestione storage cloud",
                "accesso e permessi",
                "catalogazione metadati",
            ],
            years_experience=4,
        )

    def create_trip_folder_structure(
        self,
        trip_name: str,
        destination: str,
        start_date: str,
        creator_name: str,
        base_path: str = "content/trips",
    ) -> dict[str, Any]:
        """Crea la struttura di cartelle fisica per un viaggio."""
        safe_name = trip_name.lower().replace(" ", "_").replace("/", "-")
        safe_dest = destination.lower().replace(" ", "_").replace("/", "-")
        trip_folder = Path(base_path) / f"{start_date}_{safe_dest}_{safe_name}"

        folders = [
            trip_folder / "01_raw" / "photo",
            trip_folder / "01_raw" / "video",
            trip_folder / "01_raw" / "audio",
            trip_folder / "02_editing" / "photo_edit",
            trip_folder / "02_editing" / "video_edit",
            trip_folder / "02_editing" / "graphics",
            trip_folder / "03_approved" / "instagram",
            trip_folder / "03_approved" / "tiktok",
            trip_folder / "03_approved" / "youtube",
            trip_folder / "03_approved" / "facebook",
            trip_folder / "04_published",
            trip_folder / "05_sponsorships",
            trip_folder / "06_reports",
            trip_folder / "07_briefs",
        ]

        created = []
        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)
            created.append(str(folder))

        info_file = trip_folder / "INFO.md"
        info_file.write_text(
            f"# {trip_name}\n\n"
            f"**Destinazione:** {destination}\n"
            f"**Data inizio:** {start_date}\n"
            f"**Creator:** {creator_name}\n\n"
            f"## Struttura cartelle\n"
            f"- `01_raw/` — Materiale grezzo (foto, video, audio)\n"
            f"- `02_editing/` — Lavori in corso di editing\n"
            f"- `03_approved/` — Contenuti approvati per piattaforma\n"
            f"- `04_published/` — Contenuti già pubblicati\n"
            f"- `05_sponsorships/` — Materiali per sponsorizzazioni\n"
            f"- `06_reports/` — Report e analytics\n"
            f"- `07_briefs/` — Brief creativi e contratti\n"
        )

        return {
            "trip_folder": str(trip_folder),
            "folders_created": created,
            "info_file": str(info_file),
        }

    def plan_naming_convention(
        self,
        content_types: list[str],
        platforms: list[str],
    ) -> AgentResponse:
        context = {
            "tipi_contenuto": content_types,
            "piattaforme": platforms,
        }
        task = (
            "Definisci una naming convention completa e scalabile per i file. "
            "Per ogni tipo di contenuto specifica: formato del nome file, "
            "metadati da includere, esempi pratici e come ordinare i file "
            "per facilitare il workflow di editing e pubblicazione."
        )
        return self.think_and_respond(task, context)
