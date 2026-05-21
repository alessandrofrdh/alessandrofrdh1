"""TikTok Manager — crescita e viralità su TikTok."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class TikTokManagerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.TIKTOK_MANAGER,
            name="Nicolò Ferretti",
            department="Social Media",
            specializations=[
                "trend TikTok",
                "viralità short-form",
                "TikTok SEO",
                "duetti e stitch",
                "TikTok Shop",
                "analisi For You Page",
            ],
            years_experience=4,
        )

    def identify_viral_formats(
        self,
        niche: str,
        recent_trends: list[str],
    ) -> AgentResponse:
        context = {"nicchia": niche, "trend_recenti": recent_trends}
        task = (
            "Identifica i 5 format TikTok con più potenziale virale per questa nicchia. "
            "Per ognuno: descrizione del format, hook, struttura del video, "
            "perché funziona sull'algoritmo e come adattarlo al creator."
        )
        return self.think_and_respond(task, context)

    def write_tiktok_script(
        self,
        topic: str,
        duration_seconds: int,
        style: str,
    ) -> AgentResponse:
        context = {
            "argomento": topic,
            "durata_secondi": duration_seconds,
            "stile": style,
        }
        task = (
            "Scrivi uno script TikTok con hook nei primi 2 secondi. "
            "Struttura: hook, sviluppo, twist/valore aggiunto, CTA. "
            "Includi: testo spoken, testo sovrapposto, sound suggerito e hashtag."
        )
        return self.think_and_respond(task, context)
