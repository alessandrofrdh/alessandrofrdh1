"""Social Media Scheduler — pianificazione e timing delle pubblicazioni."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class SocialSchedulerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.SOCIAL_SCHEDULER,
            name="Andrea Morelli",
            department="Social Media",
            specializations=[
                "pianificazione pubblicazioni",
                "ottimizzazione timing",
                "analisi orari audience",
                "gestione content calendar",
                "automazione social",
            ],
            years_experience=3,
        )

    def create_posting_schedule(
        self,
        platforms: list[str],
        timezone: str,
        audience_demographics: dict[str, Any],
        content_volume: dict[str, int],
    ) -> AgentResponse:
        context = {
            "piattaforme": platforms,
            "fuso_orario": timezone,
            "demografia_audience": audience_demographics,
            "volume_contenuti_settimanale": content_volume,
        }
        task = (
            "Crea un calendario di pubblicazione ottimizzato. "
            "Per ogni piattaforma specifica: giorni e orari migliori, "
            "frequenza ottimale, distribuzione dei contenuti nella settimana e "
            "finestre temporali da evitare. Basa il timing sui dati demografici dell'audience."
        )
        return self.think_and_respond(task, context)

    def plan_trip_content_release(
        self,
        trip_dates: str,
        destinations: list[str],
        total_content_pieces: int,
        platforms: list[str],
    ) -> AgentResponse:
        context = {
            "date_viaggio": trip_dates,
            "destinazioni": destinations,
            "pezzi_contenuto_totali": total_content_pieces,
            "piattaforme": platforms,
        }
        task = (
            "Pianifica il rilascio dei contenuti di viaggio. "
            "Crea una timeline che copra: pre-viaggio (teaser), durante il viaggio "
            "(live/stories), e post-viaggio (contenuti curati). "
            "Massimizza l'interesse e il reach distribuendo i contenuti nel tempo."
        )
        return self.think_and_respond(task, context)
