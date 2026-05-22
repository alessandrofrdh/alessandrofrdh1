"""Workflow per la pianificazione e produzione contenuti di viaggio."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import anthropic

from ..agents.travel import (
    TravelDirectorAgent,
    DestinationResearcherAgent,
    TravelPhotographerAgent,
    TravelVideographerAgent,
    ItineraryPlannerAgent,
)
from ..agents.base_agent import AgentResponse
from ..storage.content_manager import ContentManager


@dataclass
class TravelPlan:
    destination: str
    duration_days: int
    creator_name: str
    trip_id: str
    research: AgentResponse | None = None
    travel_plan: AgentResponse | None = None
    itinerary: AgentResponse | None = None
    photo_shot_list: AgentResponse | None = None
    video_shooting_plan: AgentResponse | None = None
    folder_path: str = ""


class TravelWorkflow:
    """Orchestrazione completa del workflow di pianificazione viaggio."""

    def __init__(self, client: anthropic.Anthropic) -> None:
        self.client = client
        self.travel_director = TravelDirectorAgent(client)
        self.researcher = DestinationResearcherAgent(client)
        self.photographer = TravelPhotographerAgent(client)
        self.videographer = TravelVideographerAgent(client)
        self.itinerary_planner = ItineraryPlannerAgent(client)
        self.content_manager = ContentManager()

    def plan_trip(
        self,
        destination: str,
        creator_name: str,
        start_date: str,
        duration_days: int,
        budget: float,
        content_goals: list[str],
        platforms: list[str],
        content_style: str = "cinematico e autentico",
    ) -> TravelPlan:
        """Esegue l'intero processo di pianificazione di un viaggio di contenuto."""
        print(f"\n{'='*60}")
        print(f"TRAVEL WORKFLOW: {destination}")
        print(f"{'='*60}")

        # Crea cartella viaggio
        trip_record = self.content_manager.create_trip(
            name=f"Trip to {destination}",
            destination=destination,
            start_date=start_date,
            creator_name=creator_name,
            tags=platforms + [content_style],
        )

        plan = TravelPlan(
            destination=destination,
            duration_days=duration_days,
            creator_name=creator_name,
            trip_id=trip_record.trip_id,
            folder_path=trip_record.folder_path,
        )

        # 1. Ricerca destinazione
        print(f"\n[1/5] Ricerca destinazione: {destination}...")
        plan.research = self.researcher.research_destination(
            destination=destination,
            content_angle=content_goals[0] if content_goals else "viaggio autentico",
        )

        # 2. Piano di viaggio del direttore
        print(f"[2/5] Piano di viaggio completo...")
        plan.travel_plan = self.travel_director.plan_content_trip(
            destination=destination,
            creator_profile={"nome": creator_name, "piattaforme": platforms},
            budget=budget,
            duration_days=duration_days,
            content_objectives=content_goals,
        )

        # 3. Itinerario dettagliato
        print(f"[3/5] Creazione itinerario...")
        plan.itinerary = self.itinerary_planner.create_content_itinerary(
            destination=destination,
            duration_days=duration_days,
            content_team_size=2,
            priorities=content_goals,
        )

        # 4. Shot list fotografica
        print(f"[4/5] Shot list fotografica...")
        plan.photo_shot_list = self.photographer.create_shot_list(
            destination=destination,
            duration_days=duration_days,
            content_objectives=content_goals,
            platforms=platforms,
        )

        # 5. Piano di riprese video
        print(f"[5/5] Piano di riprese video...")
        final_formats = []
        if "youtube" in [p.lower() for p in platforms]:
            final_formats.append("YouTube long-form 16:9")
        if "instagram" in [p.lower() for p in platforms]:
            final_formats.append("Reels 9:16")
        if "tiktok" in [p.lower() for p in platforms]:
            final_formats.append("TikTok 9:16")
        if not final_formats:
            final_formats = ["video social 9:16"]

        plan.video_shooting_plan = self.videographer.create_shooting_plan(
            destination=destination,
            final_formats=final_formats,
            duration_days=duration_days,
            style=content_style,
        )

        print(f"\n✓ Viaggio pianificato. Cartella: {trip_record.folder_path}")
        return plan
