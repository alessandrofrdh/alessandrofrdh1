"""Ad Campaign Manager — gestione campagne ads a pagamento."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class AdCampaignManagerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.AD_CAMPAIGN_MANAGER,
            name="Marco Carbone",
            department="Sponsorizzazioni",
            specializations=[
                "Meta Ads",
                "TikTok Ads",
                "Google Ads",
                "boosting contenuti",
                "retargeting",
                "ottimizzazione campagne",
            ],
            years_experience=5,
        )

    def plan_boosting_strategy(
        self,
        content_type: str,
        budget: float,
        objective: str,
        target_audience: dict[str, Any],
    ) -> AgentResponse:
        context = {
            "tipo_contenuto": content_type,
            "budget": f"€{budget:,.2f}",
            "obiettivo": objective,
            "audience_target": target_audience,
        }
        task = (
            "Crea una strategia di boosting per questo contenuto. "
            "Specifica: piattaforma, tipo di campagna, targeting (demografico, interessi, lookalike), "
            "budget allocation, durata campagna, metriche da ottimizzare e "
            "A/B test da eseguire."
        )
        return self.think_and_respond(task, context)
