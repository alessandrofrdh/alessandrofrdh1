"""Archive Manager — archiviazione e catalogazione dei contenuti."""
from __future__ import annotations

from pathlib import Path
from typing import Any
import json

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class ArchiveManagerAgent(BaseAgent):
    TOOLS = [
        "list_files", "list_trip_structure", "read_file", "write_file",
        "search_trips", "get_content_inventory", "find_approved_content",
    ]

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.ARCHIVE_MANAGER,
            name="Cristina Ferretti",
            department="Operations",
            specializations=[
                "catalogazione contenuti",
                "metadata management",
                "archivio fotografico",
                "digital asset management",
                "retrieval system",
                "backup e ridondanza",
            ],
            years_experience=5,
        )

    def catalog_trip_content(
        self,
        trip_folder: str,
        trip_metadata: dict[str, Any],
    ) -> dict[str, Any]:
        """Crea un file indice JSON per il contenuto di un viaggio."""
        catalog = {
            "trip": trip_metadata,
            "folders": {},
            "total_files": 0,
        }

        trip_path = Path(trip_folder)
        if trip_path.exists():
            for subfolder in trip_path.iterdir():
                if subfolder.is_dir():
                    files = list(subfolder.rglob("*"))
                    file_list = [str(f.relative_to(trip_path)) for f in files if f.is_file()]
                    catalog["folders"][subfolder.name] = {
                        "count": len(file_list),
                        "files": file_list,
                    }
                    catalog["total_files"] += len(file_list)

        catalog_file = trip_path / "catalog.json"
        catalog_file.write_text(json.dumps(catalog, indent=2, ensure_ascii=False))
        return catalog

    def create_archive_strategy(
        self,
        content_volume: str,
        retention_requirements: dict[str, Any],
    ) -> AgentResponse:
        context = {
            "volume_contenuto": content_volume,
            "requisiti_retention": retention_requirements,
        }
        task = (
            "Crea una strategia di archiviazione professionale. "
            "Includi: struttura gerarchica degli archivi, politica di retention per tipo di file, "
            "strategia di backup (3-2-1 rule), sistema di tagging e ricerca, "
            "strumenti consigliati e SOP per il team."
        )
        return self.think_and_respond(task, context)
