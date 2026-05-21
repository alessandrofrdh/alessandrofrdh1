"""Brand Partnership Manager — gestione operativa delle collaborazioni brand."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class BrandPartnershipManagerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.BRAND_PARTNERSHIP_MANAGER,
            name="Giacomo Ferri",
            department="Sponsorizzazioni",
            specializations=[
                "gestione account brand",
                "briefing e deliverable",
                "content approval",
                "reporting campagne",
                "relationship management",
                "upsell e rinnovi",
            ],
            years_experience=6,
        )

    def manage_brand_brief(
        self,
        brand: str,
        brief: dict[str, Any],
        creator_style: str,
    ) -> AgentResponse:
        context = {
            "brand": brand,
            "brief_ricevuto": brief,
            "stile_creator": creator_style,
        }
        task = (
            "Analizza il brief del brand e trasformalo in istruzioni creative per il creator. "
            "Spiega: messaggi chiave da comunicare, must-have e don'ts, "
            "come integrare il brand in modo naturale, "
            "deliverable richiesti con deadline e criteri di approvazione."
        )
        return self.think_and_respond(task, context)

    def create_campaign_report(
        self,
        brand: str,
        campaign_results: dict[str, Any],
        goals: dict[str, Any],
    ) -> AgentResponse:
        context = {
            "brand": brand,
            "risultati_campagna": campaign_results,
            "obiettivi_iniziali": goals,
        }
        task = (
            "Crea un report di campagna professionale per il brand. "
            "Includi: executive summary, reach e impression, "
            "engagement rate, link clicks/conversioni, "
            "sentiment analysis commenti, confronto con obiettivi, "
            "insight chiave e proposta per la prossima collaborazione."
        )
        return self.think_and_respond(task, context)
