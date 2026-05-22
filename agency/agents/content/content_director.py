"""Direttore del dipartimento contenuti."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class ContentDirectorAgent(BaseAgent):
    TOOLS = [
        "analyze_image", "analyze_trip_photos",
        "read_file", "save_brief", "list_trip_structure",
        "search_trips", "get_content_inventory",
    ]

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.CONTENT_DIRECTOR,
            name="Alessia Romano",
            department="Contenuti",
            specializations=[
                "direzione creativa",
                "storytelling visivo",
                "pianificazione editoriale",
                "supervisione video e foto",
                "brand consistency",
            ],
            years_experience=8,
        )

    def brief_content_team(
        self,
        trip: dict[str, Any],
        content_goals: list[str],
    ) -> AgentResponse:
        context = {"viaggio": trip, "obiettivi_contenuto": content_goals}
        task = (
            "Crea un brief creativo completo per il team di produzione. "
            "Includi: concept visivo, mood board testuale, lista shot da realizzare, "
            "divisione lavoro tra video editor e photo editor, "
            "tono narrativo per i copy e deadline per ogni deliverable."
        )
        return self.think_and_respond(task, context)

    def review_content_quality(
        self,
        content_type: str,
        content_description: str,
        platform: str,
    ) -> AgentResponse:
        context = {
            "tipo_contenuto": content_type,
            "descrizione": content_description,
            "piattaforma_destinazione": platform,
        }
        task = (
            "Analizza questo contenuto e fornisci feedback dettagliato sulla qualità. "
            "Valuta: aderenza al brief, qualità tecnica, appeal visivo, "
            "potenziale di engagement e suggerimenti specifici di miglioramento."
        )
        return self.think_and_respond(task, context)
