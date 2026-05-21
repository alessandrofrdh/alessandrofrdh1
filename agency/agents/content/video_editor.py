"""Video editor — montaggio e produzione video per i social."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class VideoEditorAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.VIDEO_EDITOR,
            name="Davide Conti",
            department="Contenuti",
            specializations=[
                "montaggio video",
                "color grading",
                "motion graphics",
                "reels e short-form",
                "long-form YouTube",
            ],
            years_experience=5,
        )

    def create_edit_plan(
        self,
        raw_footage_description: str,
        target_platform: str,
        style: str,
    ) -> AgentResponse:
        context = {
            "materiale_grezzo": raw_footage_description,
            "piattaforma": target_platform,
            "stile_richiesto": style,
        }
        task = (
            "Crea un piano di montaggio dettagliato. Includi: struttura narrativa, "
            "selezione clip principali, musica suggerita, effetti e transizioni, "
            "formato output (risoluzione, aspect ratio, durata) e "
            "specifiche tecniche per la piattaforma target."
        )
        return self.think_and_respond(task, context)

    def write_editing_script(
        self,
        video_concept: str,
        duration_seconds: int,
        platform: str,
    ) -> AgentResponse:
        context = {
            "concept": video_concept,
            "durata_secondi": duration_seconds,
            "piattaforma": platform,
        }
        task = (
            "Scrivi uno script di montaggio dettagliato con timestamp. "
            "Specifica per ogni segmento: tipo di clip, durata, musica/audio, "
            "testo sovrapposto, transizione e note di color grading."
        )
        return self.think_and_respond(task, context)


class SeniorVideoEditorAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.VIDEO_EDITOR_SENIOR,
            name="Giulia Ferrara",
            department="Contenuti",
            specializations=[
                "produzione cinematografica",
                "color grading professionale",
                "documentari di viaggio",
                "campagne pubblicitarie video",
                "storytelling avanzato",
                "supervisione junior editor",
            ],
            years_experience=9,
        )

    def produce_hero_video(
        self,
        trip: dict[str, Any],
        brand_guidelines: dict[str, Any],
    ) -> AgentResponse:
        context = {"viaggio": trip, "linee_guida_brand": brand_guidelines}
        task = (
            "Progetta la produzione di un video hero (2-4 minuti) per YouTube. "
            "Includi: struttura atto per atto, regia consigliata, "
            "elenco B-roll essenziali, piano audio/colonna sonora, "
            "strategia thumbnail e ottimizzazione SEO YouTube."
        )
        return self.think_and_respond(task, context)


class JuniorVideoEditorAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.VIDEO_EDITOR_JUNIOR,
            name="Matteo Russo",
            department="Contenuti",
            specializations=[
                "montaggio reels",
                "TikTok editing",
                "sottotitoli e caption",
                "adattamento formati",
            ],
            years_experience=2,
        )

    def edit_short_form(
        self,
        clip_list: list[str],
        platform: str,
        trend_audio: str,
    ) -> AgentResponse:
        context = {
            "lista_clip": clip_list,
            "piattaforma": platform,
            "audio_trend": trend_audio,
        }
        task = (
            "Crea un piano di montaggio per un video short-form (15-60 secondi). "
            "Ottimizza per l'hook nei primi 3 secondi, ritmo dinamico e call-to-action finale."
        )
        return self.think_and_respond(task, context)
