"""Facebook Manager — gestione pagina e community Facebook."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class FacebookManagerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.FACEBOOK_MANAGER,
            name="Emanuele Greco",
            department="Social Media",
            specializations=[
                "Facebook Groups",
                "Facebook Ads",
                "Facebook Reels",
                "gestione pagine",
                "Facebook Live",
                "traffico e remarketing",
            ],
            years_experience=6,
        )

    def manage_facebook_group(
        self,
        group_topic: str,
        member_count: int,
        engagement_goals: list[str],
    ) -> AgentResponse:
        context = {
            "tema_gruppo": group_topic,
            "numero_membri": member_count,
            "obiettivi_engagement": engagement_goals,
        }
        task = (
            "Crea una strategia di gestione per questo gruppo Facebook. "
            "Includi: regole del gruppo, tipologie di post settimanali, "
            "come stimolare la discussione, come moderare e "
            "come usare il gruppo per monetizzazione."
        )
        return self.think_and_respond(task, context)
