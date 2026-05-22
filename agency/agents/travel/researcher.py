"""Ricercatore Destinazioni — ricerca e scouting di nuove mete."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class DestinationResearcherAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.DESTINATION_RESEARCHER,
            name="Isabella Colombo",
            department="Viaggi",
            specializations=[
                "ricerca destinazioni",
                "trend di viaggio",
                "destinazioni off-the-beaten-path",
                "analisi concorrenza creator",
                "stagionalità e clima",
                "visti e documentazione",
            ],
            years_experience=5,
        )

    def research_destination(
        self,
        destination: str,
        content_angle: str,
    ) -> AgentResponse:
        context = {
            "destinazione": destination,
            "angolo_narrativo": content_angle,
        }
        task = (
            "Conduci una ricerca approfondita su questa destinazione. "
            "Includi: attrazioni principali e nascoste, migliore periodo per visitare, "
            "costi stimati, location più fotografabili, "
            "aspetti culturali da rispettare, visti necessari, "
            "creator che hanno già visitato questa meta e angoli narrativi inesplorati."
        )
        return self.think_and_respond(task, context)

    def find_hidden_gems(
        self,
        country: str,
        content_style: str,
    ) -> AgentResponse:
        context = {"paese": country, "stile_contenuto": content_style}
        task = (
            "Trova 10 location o esperienze non mainstream in questo paese "
            "che potrebbero fare contenuto virale e differenziante. "
            "Per ognuna: descrizione, come arrivarci, potenziale virale e "
            "tipo di contenuto che si potrebbe creare."
        )
        return self.think_and_respond(task, context)
