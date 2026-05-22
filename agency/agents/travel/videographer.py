"""Videomaker di Viaggio — riprese video professionali in loco."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class TravelVideographerAgent(BaseAgent):
    TOOLS = [
        "analyze_video", "analyze_trip_videos",
        "list_files", "list_trip_structure", "save_brief",
    ]

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.TRAVEL_VIDEOGRAPHER,
            name="Alessandro Neri",
            department="Viaggi",
            specializations=[
                "riprese cinematografiche",
                "drone video",
                "GoPro e action cam",
                "stabilizzazione gimbal",
                "riprese timelapse",
                "video subacqueo",
            ],
            years_experience=7,
        )

    def create_shooting_plan(
        self,
        destination: str,
        final_formats: list[str],
        duration_days: int,
        style: str,
    ) -> AgentResponse:
        context = {
            "destinazione": destination,
            "formati_finali": final_formats,
            "giorni": duration_days,
            "stile_visivo": style,
        }
        task = (
            "Crea un piano di riprese video completo. "
            "Per ogni giorno: sequenze da girare, tipo di ripresa "
            "(droni, gimbal, action cam, handheld), "
            "impostazioni camera consigliate (fps, risoluzione, formato colore), "
            "audio da catturare (ambientale, parlato, sync) e "
            "lista materiale necessario."
        )
        return self.think_and_respond(task, context)
