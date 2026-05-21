"""Community Manager — gestione community e relazioni con i follower."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class CommunityManagerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.COMMUNITY_MANAGER,
            name="Francesca Amato",
            department="Social Media",
            specializations=[
                "gestione commenti",
                "engagement organico",
                "crisis management",
                "community building",
                "DM management",
                "ambassador program",
            ],
            years_experience=4,
        )

    def create_engagement_strategy(
        self,
        platform: str,
        audience_size: int,
        current_engagement_rate: float,
    ) -> AgentResponse:
        context = {
            "piattaforma": platform,
            "dimensione_audience": audience_size,
            "tasso_engagement_attuale": f"{current_engagement_rate:.1f}%",
        }
        task = (
            "Crea una strategia di engagement per aumentare le interazioni. "
            "Includi: come rispondere ai commenti, domande da porre alla community, "
            "contenuti UGC da stimolare, come gestire commenti negativi e "
            "piano per un programma ambassador."
        )
        return self.think_and_respond(task, context)

    def draft_comment_responses(
        self,
        comment_type: str,
        brand_voice: str,
        examples: list[str],
    ) -> AgentResponse:
        context = {
            "tipo_commento": comment_type,
            "tono_brand": brand_voice,
            "esempi_commenti": examples,
        }
        task = (
            "Scrivi 5 risposte ai commenti che siano autentiche, engaging e "
            "rispecchino il tono del brand. Devono stimolare ulteriori interazioni."
        )
        return self.think_and_respond(task, context)
