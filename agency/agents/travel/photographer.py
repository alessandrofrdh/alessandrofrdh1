"""Fotografo di Viaggio — fotografia professionale in loco."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class TravelPhotographerAgent(BaseAgent):
    TOOLS = [
        "analyze_image", "analyze_trip_photos",
        "list_files", "list_trip_structure", "save_brief",
    ]

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.TRAVEL_PHOTOGRAPHER,
            name="Gabriele Serra",
            department="Viaggi",
            specializations=[
                "fotografia paesaggistica",
                "ritrattistica lifestyle",
                "fotografia architettonica",
                "golden hour e blue hour",
                "fotografia subacquea",
                "drone photography",
            ],
            years_experience=8,
        )

    def create_shot_list(
        self,
        destination: str,
        duration_days: int,
        content_objectives: list[str],
        platforms: list[str],
    ) -> AgentResponse:
        context = {
            "destinazione": destination,
            "giorni_disponibili": duration_days,
            "obiettivi": content_objectives,
            "piattaforme": platforms,
        }
        task = (
            "Crea una shot list completa per questo viaggio. "
            "Organizza per giorno e location. Per ogni scatto: "
            "tipo di foto, attrezzatura consigliata, ora ideale del giorno, "
            "composizione, colori dominanti e piattaforma di destinazione. "
            "Includi scatti hero, di supporto e di lifestyle."
        )
        return self.think_and_respond(task, context)

    def plan_golden_hour_sessions(
        self,
        destination: str,
        dates: list[str],
        key_locations: list[str],
    ) -> AgentResponse:
        context = {
            "destinazione": destination,
            "date": dates,
            "location_chiave": key_locations,
        }
        task = (
            "Pianifica le sessioni fotografiche nelle ore d'oro. "
            "Per ogni data e location: orario golden hour e blue hour, "
            "angolazione solare consigliata, setup camera suggerito e "
            "tipo di scatti da prioritizzare."
        )
        return self.think_and_respond(task, context)
