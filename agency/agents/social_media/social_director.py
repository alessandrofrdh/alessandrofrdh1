"""Direttore Social Media."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class SocialMediaDirectorAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.SOCIAL_MEDIA_DIRECTOR,
            name="Camilla Vitali",
            department="Social Media",
            specializations=[
                "strategia multi-piattaforma",
                "crescita follower",
                "gestione community",
                "crisis management social",
                "algoritmi piattaforme",
                "social commerce",
            ],
            years_experience=9,
        )

    def define_platform_strategy(
        self,
        creator_profile: dict[str, Any],
        current_performance: dict[str, Any],
    ) -> AgentResponse:
        context = {
            "profilo_creator": creator_profile,
            "performance_attuali": current_performance,
        }
        task = (
            "Definisci la strategia social media completa. "
            "Per ogni piattaforma: obiettivi 90 giorni, tipologie contenuto prioritarie, "
            "frequenza pubblicazione, metriche di successo e budget ads suggerito."
        )
        return self.think_and_respond(task, context)

    def analyze_algorithm_changes(
        self,
        platform: str,
        recent_changes: str,
    ) -> AgentResponse:
        context = {"piattaforma": platform, "cambiamenti_recenti": recent_changes}
        task = (
            "Analizza come questi cambiamenti algoritmici impattano la nostra strategia. "
            "Proponi adattamenti concreti al piano editoriale e alle tattiche di distribuzione."
        )
        return self.think_and_respond(task, context)
