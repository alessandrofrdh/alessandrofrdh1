"""Graphic designer — grafica, template e visual identity."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class GraphicDesignerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.GRAPHIC_DESIGNER,
            name="Serena Ricci",
            department="Contenuti",
            specializations=[
                "visual identity",
                "template social",
                "infografiche",
                "thumbnail YouTube",
                "loghi e branding",
                "motion design",
            ],
            years_experience=6,
        )

    def design_social_templates(
        self,
        brand_identity: dict[str, Any],
        platforms: list[str],
    ) -> AgentResponse:
        context = {
            "identita_brand": brand_identity,
            "piattaforme": platforms,
        }
        task = (
            "Progetta un sistema di template per i social media. "
            "Per ogni piattaforma specifica: layout, tipografia, colori, "
            "elementi grafici ricorrenti, dimensioni e varianti "
            "(post feed, stories, copertine). "
            "Il sistema deve essere coerente e facilmente replicabile."
        )
        return self.think_and_respond(task, context)

    def design_youtube_thumbnail(
        self,
        video_title: str,
        creator_style: str,
        emotion_to_convey: str,
    ) -> AgentResponse:
        context = {
            "titolo_video": video_title,
            "stile_creator": creator_style,
            "emozione_da_trasmettere": emotion_to_convey,
        }
        task = (
            "Progetta il concept per una thumbnail YouTube ad alto CTR. "
            "Descrivi: composizione visiva, testo sovrapposto, espressione/posa del creator, "
            "schema colori, elementi grafici e perché questa thumbnail funzionerà. "
            "Fornisci 3 varianti con diversi approcci."
        )
        return self.think_and_respond(task, context)
