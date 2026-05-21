"""Direttore Sponsorizzazioni — strategia e gestione partnership con i brand."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class SponsorshipDirectorAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.SPONSORSHIP_DIRECTOR,
            name="Paola Marchetti",
            department="Sponsorizzazioni",
            specializations=[
                "sviluppo partnership strategiche",
                "negoziazione contratti",
                "media kit",
                "pricing influencer",
                "gestione portafoglio brand",
                "compliance e disclosure",
            ],
            years_experience=11,
        )

    def create_media_kit(
        self,
        creator_profile: dict[str, Any],
        all_platforms_metrics: dict[str, Any],
        past_collaborations: list[str],
    ) -> AgentResponse:
        context = {
            "profilo_creator": creator_profile,
            "metriche_piattaforme": all_platforms_metrics,
            "collaborazioni_precedenti": past_collaborations,
        }
        task = (
            "Crea un media kit professionale e convincente per questo creator. "
            "Includi: bio professionale, statistiche chiave per ogni piattaforma, "
            "audience demographics, engagement rate, categorie di contenuto, "
            "case study di collaborazioni passate con risultati, "
            "pacchetti di collaborazione con prezzi e testimonial brand."
        )
        return self.think_and_respond(task, context)

    def evaluate_sponsorship_deal(
        self,
        brand: str,
        offer_details: dict[str, Any],
        creator_values: list[str],
    ) -> AgentResponse:
        context = {
            "brand": brand,
            "dettagli_offerta": offer_details,
            "valori_creator": creator_values,
        }
        task = (
            "Valuta questa proposta di sponsorizzazione. "
            "Analizza: allineamento con i valori del creator, fee vs. effort, "
            "termini contrattuali critici, rischi reputazionali, "
            "opportunità di upsell e raccomandazione finale (accettare/negoziare/rifiutare)."
        )
        return self.think_and_respond(task, context)
