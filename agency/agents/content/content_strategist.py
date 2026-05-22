"""Content strategist — piano editoriale e calendario contenuti."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class ContentStrategistAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.CONTENT_STRATEGIST,
            name="Martina Costa",
            department="Contenuti",
            specializations=[
                "content planning",
                "calendar editoriale",
                "analisi trend",
                "strategia cross-platform",
                "ottimizzazione algoritmi",
                "repurposing contenuti",
            ],
            years_experience=6,
        )

    def create_editorial_calendar(
        self,
        creator_profile: dict[str, Any],
        platforms: list[str],
        period_weeks: int,
        upcoming_trips: list[str],
    ) -> AgentResponse:
        context = {
            "profilo_creator": creator_profile,
            "piattaforme": platforms,
            "periodo_settimane": period_weeks,
            "viaggi_previsti": upcoming_trips,
        }
        task = (
            "Crea un calendario editoriale dettagliato. "
            "Per ogni settimana specifica: post per piattaforma, tipologia contenuto, "
            "topic/tema, formato (video/foto/carousel/story) e orario di pubblicazione ottimale. "
            "Bilancia contenuti organici, branded e di engagement."
        )
        return self.think_and_respond(task, context)

    def repurpose_content(
        self,
        original_content: str,
        original_platform: str,
        target_platforms: list[str],
    ) -> AgentResponse:
        context = {
            "contenuto_originale": original_content,
            "piattaforma_originale": original_platform,
            "piattaforme_target": target_platforms,
        }
        task = (
            "Crea una strategia di repurposing per questo contenuto. "
            "Per ogni piattaforma target spiega come adattare il contenuto: "
            "formato, lunghezza, angolo narrativo, elementi da aggiungere/rimuovere."
        )
        return self.think_and_respond(task, context)
