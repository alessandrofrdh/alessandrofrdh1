"""LinkedIn Manager — presenza professionale e B2B."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class LinkedInManagerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.LINKEDIN_MANAGER,
            name="Roberta Coppola",
            department="Social Media",
            specializations=[
                "personal branding LinkedIn",
                "content B2B",
                "lead generation",
                "networking professionale",
                "LinkedIn Newsletter",
            ],
            years_experience=5,
        )

    def build_linkedin_presence(
        self,
        creator_background: dict[str, Any],
        b2b_goals: list[str],
    ) -> AgentResponse:
        context = {
            "background_creator": creator_background,
            "obiettivi_b2b": b2b_goals,
        }
        task = (
            "Sviluppa una strategia LinkedIn per questo creator travel. "
            "Includi: ottimizzazione profilo per il settore, "
            "tipologie di contenuto per attrarre brand partner e agenzie di viaggio, "
            "piano di networking e come usare LinkedIn per acquisire sponsorizzazioni premium."
        )
        return self.think_and_respond(task, context)
