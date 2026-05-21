"""SEO Specialist — ottimizzazione per i motori di ricerca e piattaforme."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class SEOSpecialistAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.SEO_SPECIALIST,
            name="Antonella Bruno",
            department="Operations",
            specializations=[
                "YouTube SEO",
                "Google SEO",
                "Pinterest SEO",
                "keyword research",
                "ottimizzazione profili social",
                "content SEO",
            ],
            years_experience=6,
        )

    def research_keywords(
        self,
        niche: str,
        platforms: list[str],
        competition_level: str,
    ) -> AgentResponse:
        context = {
            "nicchia": niche,
            "piattaforme": platforms,
            "livello_competizione": competition_level,
        }
        task = (
            "Conduci una ricerca keyword completa per questa nicchia. "
            "Per ogni piattaforma: top keyword (volume alto), "
            "keyword a coda lunga (bassa competizione), "
            "keyword stagionali, trend emergenti e "
            "come usarle nei contenuti in modo naturale."
        )
        return self.think_and_respond(task, context)
