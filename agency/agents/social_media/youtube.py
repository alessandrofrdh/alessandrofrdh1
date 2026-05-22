"""YouTube Manager — crescita canale e monetizzazione YouTube."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class YouTubeManagerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.YOUTUBE_MANAGER,
            name="Beatrice Fontana",
            department="Social Media",
            specializations=[
                "YouTube SEO",
                "crescita canale",
                "monetizzazione YouTube",
                "YouTube Shorts",
                "analisi audience",
                "ottimizzazione retention",
            ],
            years_experience=7,
        )

    def optimize_video_for_youtube(
        self,
        video_topic: str,
        target_keywords: list[str],
        video_duration_minutes: int,
    ) -> AgentResponse:
        context = {
            "argomento": video_topic,
            "keyword_target": target_keywords,
            "durata_minuti": video_duration_minutes,
        }
        task = (
            "Ottimizza questo video per YouTube. Fornisci: "
            "titolo SEO ottimizzato (max 70 caratteri), "
            "descrizione completa con keyword (primo paragrafo, capitoli, link, hashtag), "
            "tag consigliati (20-30), categoria, card e end screen strategy."
        )
        return self.think_and_respond(task, context)

    def plan_channel_growth(
        self,
        current_subscribers: int,
        current_avg_views: int,
        target_subscribers: int,
    ) -> AgentResponse:
        context = {
            "iscritti_attuali": current_subscribers,
            "visualizzazioni_medie": current_avg_views,
            "target_iscritti": target_subscribers,
        }
        task = (
            "Crea un piano di crescita del canale YouTube. "
            "Includi: content mix ottimale, frequenza upload, "
            "strategia Shorts per attirare nuovi iscritti, "
            "collaborazioni suggerite e percorso di monetizzazione."
        )
        return self.think_and_respond(task, context)
