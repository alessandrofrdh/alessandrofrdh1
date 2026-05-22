"""Pianificatore Itinerari — logistica e ottimizzazione dei percorsi."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class ItineraryPlannerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.ITINERARY_PLANNER,
            name="Claudia Rizzo",
            department="Viaggi",
            specializations=[
                "ottimizzazione itinerari",
                "logistica di viaggio",
                "prenotazione strutture",
                "trasporti e mobilità",
                "esperienze local",
                "gestione tempi di shooting",
            ],
            years_experience=6,
        )

    def create_content_itinerary(
        self,
        destination: str,
        duration_days: int,
        content_team_size: int,
        priorities: list[str],
    ) -> AgentResponse:
        context = {
            "destinazione": destination,
            "durata_giorni": duration_days,
            "dimensione_team": content_team_size,
            "priorita": priorities,
        }
        task = (
            "Crea un itinerario ottimizzato per un team di produzione contenuti. "
            "Per ogni giorno: orario dettagliato, spostamenti, location di shooting, "
            "pasti (con considerazioni per possibili riprese durante i pasti), "
            "buffer time per imprevisiti, accommodation e "
            "nota sui contenuti che si possono produrre in ogni momento."
        )
        return self.think_and_respond(task, context)
