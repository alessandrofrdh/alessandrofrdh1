"""Direttore Viaggi — coordinamento dei trip e logistica."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class TravelDirectorAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.TRAVEL_DIRECTOR,
            name="Roberto Zanetti",
            department="Viaggi",
            specializations=[
                "pianificazione viaggi",
                "destinazioni emergenti",
                "negoziazione con hotel e DMC",
                "shooting location scouting",
                "travel budgeting",
                "partnership con enti del turismo",
            ],
            years_experience=12,
        )

    def plan_content_trip(
        self,
        destination: str,
        creator_profile: dict[str, Any],
        budget: float,
        duration_days: int,
        content_objectives: list[str],
    ) -> AgentResponse:
        context = {
            "destinazione": destination,
            "profilo_creator": creator_profile,
            "budget": f"€{budget:,.2f}",
            "durata_giorni": duration_days,
            "obiettivi_contenuto": content_objectives,
        }
        task = (
            "Pianifica un viaggio di produzione contenuti completo. "
            "Includi: itinerario giorno per giorno, location per gli shooting, "
            "hotel e strutture consigliate, trasporti, budget breakdown, "
            "contatti locali (guide, fixer, location scout) e "
            "piano B in caso di imprevisti meteo o logistici."
        )
        return self.think_and_respond(task, context)

    def negotiate_travel_partnership(
        self,
        partner_type: str,
        partner_name: str,
        offer_details: dict[str, Any],
    ) -> AgentResponse:
        context = {
            "tipo_partner": partner_type,
            "nome_partner": partner_name,
            "dettagli_offerta": offer_details,
        }
        task = (
            "Valuta questa partnership di viaggio e prepara una controproposta. "
            "Analizza: valore dell'offerta, obblighi richiesti, potenziale di contenuto, "
            "ROI per il creator e termini contrattuali da negoziare."
        )
        return self.think_and_respond(task, context)
