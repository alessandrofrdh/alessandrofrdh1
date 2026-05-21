"""Influencer Relations Manager — outreach e relazioni con brand e agenzie."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class InfluencerRelationsAgent(BaseAgent):
    TOOLS = [
        "list_brands", "get_brand", "register_brand",
        "get_deal_history", "log_deal",
        "estimate_influencer_fee",
    ]

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.INFLUENCER_RELATIONS,
            name="Silvia Montanari",
            department="Sponsorizzazioni",
            specializations=[
                "outreach brand",
                "cold email e DM",
                "negoziazione fee",
                "gestione agenzie",
                "scouting brand partner",
                "contrattualistica",
            ],
            years_experience=5,
        )

    def write_brand_outreach(
        self,
        creator_profile: dict[str, Any],
        target_brand: str,
        collaboration_idea: str,
    ) -> AgentResponse:
        context = {
            "profilo_creator": creator_profile,
            "brand_target": target_brand,
            "idea_collaborazione": collaboration_idea,
        }
        task = (
            "Scrivi un'email di outreach professionale per questo brand. "
            "Deve essere: personalizzata, concisa (max 200 parole), "
            "evidenziare il valore unico del creator per quel brand specifico, "
            "includere una proposta chiara e un CTA diretto."
        )
        return self.think_and_respond(task, context)

    def identify_brand_targets(
        self,
        creator_niche: str,
        audience_demographics: dict[str, Any],
        excluded_brands: list[str],
    ) -> AgentResponse:
        context = {
            "nicchia_creator": creator_niche,
            "demografia_audience": audience_demographics,
            "brand_esclusi": excluded_brands,
        }
        task = (
            "Identifica 20 brand ideali da contattare per sponsorizzazioni. "
            "Per ognuno: nome brand, perché è un buon fit, "
            "tipo di collaborazione suggerita, canale di contatto "
            "e stima della fee di mercato per questo creator."
        )
        return self.think_and_respond(task, context)
