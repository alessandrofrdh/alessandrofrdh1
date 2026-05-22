"""Instagram Manager — gestione e crescita profilo Instagram."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class InstagramManagerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.INSTAGRAM_MANAGER,
            name="Aurora Pellegrini",
            department="Social Media",
            specializations=[
                "Instagram Reels",
                "Instagram Stories",
                "ottimizzazione profilo",
                "crescita organica Instagram",
                "Instagram Shopping",
                "Collab post",
            ],
            years_experience=5,
        )

    def optimize_profile(
        self,
        current_bio: str,
        creator_niche: str,
        target_keywords: list[str],
    ) -> AgentResponse:
        context = {
            "bio_attuale": current_bio,
            "nicchia": creator_niche,
            "keyword_target": target_keywords,
        }
        task = (
            "Ottimizza il profilo Instagram. Fornisci: nuova bio ottimizzata (max 150 caratteri), "
            "nome profilo SEO-friendly, link in bio strategy, "
            "highlights consigliati e immagine profilo guidelines."
        )
        return self.think_and_respond(task, context)

    def plan_reels_strategy(
        self,
        niche: str,
        current_followers: int,
        weekly_frequency: int,
    ) -> AgentResponse:
        context = {
            "nicchia": niche,
            "follower_attuali": current_followers,
            "frequenza_settimanale": weekly_frequency,
        }
        task = (
            "Crea una strategia Reels per i prossimi 30 giorni. "
            "Per ogni Reel specifica: concept, hook (prime 3 secondi), "
            "durata ottimale, audio trend da usare, testo sovrapposto e caption."
        )
        return self.think_and_respond(task, context)

    def create_stories_sequence(
        self,
        topic: str,
        cta: str,
    ) -> AgentResponse:
        context = {"argomento": topic, "call_to_action": cta}
        task = (
            "Crea una sequenza di Stories Instagram (5-8 slide) su questo argomento. "
            "Per ogni slide: tipo (foto/video/boomerang/poll), testo, sticker interattivo "
            "e come si collega alla slide successiva."
        )
        return self.think_and_respond(task, context)
