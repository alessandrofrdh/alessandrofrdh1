"""Orchestratore principale dell'agenzia — coordina tutti i dipartimenti."""
from __future__ import annotations

import os
from typing import Any

import anthropic

from .agents.executive import CEOAgent, COOAgent, CMOAgent
from .agents.content import ContentDirectorAgent, ContentStrategistAgent
from .agents.social_media import SocialMediaDirectorAgent, SocialAnalyticsAgent
from .agents.travel import TravelDirectorAgent
from .agents.sponsorship import SponsorshipDirectorAgent, RevenueManagerAgent
from .agents.operations import ProjectManagerAgent, FileManagerAgent, QualityControllerAgent
from .agents.client import OwnerAgent
from .workflows.travel_workflow import TravelWorkflow, TravelPlan
from .workflows.content_pipeline import ContentPipelineWorkflow, ContentPackage
from .workflows.sponsorship_workflow import SponsorshipWorkflow, SponsorshipDeal
from .workflows.publishing_workflow import PublishingWorkflow, PublishingPlan
from .workflows.owner_review_workflow import OwnerReviewWorkflow, WeeklyReviewResult
from .storage.content_manager import ContentManager


class TravelVisionAgency:
    """
    TravelVision Agency — sistema multi-agente da 100 persone.

    Coordina 6 dipartimenti:
    - Executive (CEO, COO, CMO)
    - Contenuti (Director + 15 specialisti)
    - Social Media (Director + 8 manager)
    - Viaggi (Director + 4 specialisti)
    - Sponsorizzazioni (Director + 5 manager)
    - Operations (6 specialisti)
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY")
        )

        # Agenti esecutivi
        self.ceo = CEOAgent(self.client)
        self.coo = COOAgent(self.client)
        self.cmo = CMOAgent(self.client)

        # Direttori di dipartimento
        self.content_director = ContentDirectorAgent(self.client)
        self.social_director = SocialMediaDirectorAgent(self.client)
        self.travel_director = TravelDirectorAgent(self.client)
        self.sponsorship_director = SponsorshipDirectorAgent(self.client)
        self.project_manager = ProjectManagerAgent(self.client)

        # Specialisti chiave
        self.content_strategist = ContentStrategistAgent(self.client)
        self.social_analytics = SocialAnalyticsAgent(self.client)
        self.revenue_manager = RevenueManagerAgent(self.client)
        self.quality_controller = QualityControllerAgent(self.client)
        self.file_manager = FileManagerAgent(self.client)

        # Workflow
        self.travel_workflow = TravelWorkflow(self.client)
        self.content_pipeline = ContentPipelineWorkflow(self.client)
        self.sponsorship_workflow = SponsorshipWorkflow(self.client)
        self.publishing_workflow = PublishingWorkflow(self.client)
        self.owner_review_workflow = OwnerReviewWorkflow(self.client)

        # Agente proprietario
        self.owner = OwnerAgent(self.client)

        # Storage
        self.content_manager = ContentManager()

    # ─── FUNZIONI PRINCIPALI ─────────────────────────────────────────────────

    def onboard_creator(
        self,
        creator_name: str,
        niche: str,
        platforms: list[str],
        monthly_revenue_goal: float,
        target_audience: dict[str, Any],
    ) -> dict[str, Any]:
        """Processo completo di onboarding di un nuovo creator."""
        print(f"\n{'='*70}")
        print(f"ONBOARDING CREATOR: {creator_name}")
        print(f"{'='*70}")

        creator_profile = {
            "nome": creator_name,
            "nicchia": niche,
            "piattaforme": platforms,
            "obiettivo_revenue": f"€{monthly_revenue_goal:,.0f}/mese",
            "pubblico_target": target_audience,
        }

        results: dict[str, Any] = {"creator": creator_profile}

        print("\n[CEO] Strategia di campagna...")
        results["ceo_strategy"] = self.ceo.create_campaign_strategy(
            creator_profile=creator_profile,
            goals=[
                f"Raggiungere €{monthly_revenue_goal:,.0f}/mese di revenue",
                "Crescita follower organica",
                "Brand positioning nel settore travel",
            ],
            budget=monthly_revenue_goal * 0.3,
        )

        print("\n[CMO] Brand identity...")
        results["brand_identity"] = self.cmo.create_brand_identity(
            creator_name=creator_name,
            niche=niche,
            target_audience=target_audience,
        )

        print("\n[Revenue] Piano monetizzazione...")
        results["revenue_plan"] = self.revenue_manager.create_revenue_plan(
            creator_profile=creator_profile,
            current_monthly_revenue=0,
            target_monthly_revenue=monthly_revenue_goal,
        )

        print("\n[Strategy] Pillar contenuti...")
        results["content_pillars"] = self.content_strategist.develop_content_pillars(
            creator_niche=niche,
            target_audience=target_audience,
        )

        print(f"\n✓ Onboarding completato per {creator_name}.")
        return results

    def plan_content_trip(
        self,
        creator_name: str,
        destination: str,
        start_date: str,
        duration_days: int,
        budget: float,
        platforms: list[str],
        content_goals: list[str] | None = None,
    ) -> TravelPlan:
        """Pianifica un viaggio di contenuto dall'inizio alla fine."""
        goals = content_goals or [
            f"Contenuti autentici da {destination}",
            "Viral potenziale su TikTok/Reels",
            "Materiale per sponsorizzazioni",
        ]
        return self.travel_workflow.plan_trip(
            destination=destination,
            creator_name=creator_name,
            start_date=start_date,
            duration_days=duration_days,
            budget=budget,
            content_goals=goals,
            platforms=platforms,
        )

    def produce_content_package(
        self,
        trip_id: str,
        destination: str,
        platform: str,
        raw_content_description: str,
        creator_style: str,
        brand_voice: str,
        keywords: list[str] | None = None,
    ) -> ContentPackage:
        """Produce un pacchetto di contenuto completo per una piattaforma."""
        platform_lower = platform.lower()
        if platform_lower == "instagram":
            return self.content_pipeline.produce_instagram_reel(
                trip_id=trip_id,
                destination=destination,
                raw_footage=raw_content_description,
                creator_style=creator_style,
                brand_voice=brand_voice,
            )
        elif platform_lower == "youtube":
            return self.content_pipeline.produce_youtube_video(
                trip_id=trip_id,
                destination=destination,
                raw_footage=raw_content_description,
                video_concept=raw_content_description,
                target_keywords=keywords or ["travel", destination.lower()],
            )
        elif platform_lower == "tiktok":
            return self.content_pipeline.produce_tiktok_video(
                trip_id=trip_id,
                destination=destination,
                clip_description=raw_content_description,
                trend_audio="trending sound",
                creator_style=creator_style,
            )
        else:
            return self.content_pipeline.produce_instagram_reel(
                trip_id=trip_id,
                destination=destination,
                raw_footage=raw_content_description,
                creator_style=creator_style,
                brand_voice=brand_voice,
            )

    def manage_sponsorship(
        self,
        creator_profile: dict[str, Any],
        brand: str,
        collaboration_type: str,
        mode: str = "outreach",
        brand_brief: dict | None = None,
        creator_values: list[str] | None = None,
    ) -> SponsorshipDeal:
        """Gestisce una sponsorizzazione (outreach o deal inbound)."""
        if mode == "outreach":
            return self.sponsorship_workflow.outreach_brand(
                creator_profile=creator_profile,
                target_brand=brand,
                collaboration_idea=collaboration_type,
            )
        else:
            return self.sponsorship_workflow.manage_incoming_deal(
                brand=brand,
                creator_profile=creator_profile,
                brand_brief=brand_brief or {"tipo": collaboration_type},
                creator_values=creator_values or ["autenticità", "qualità", "viaggi"],
                platform=creator_profile.get("piattaforma_principale", "Instagram"),
                key_messages=[collaboration_type],
            )

    def create_publishing_plan(
        self,
        creator_name: str,
        platforms: list[str],
        audience_data: dict[str, Any],
        weekly_content_volume: dict[str, int],
        trip_dates: str | None = None,
        destinations: list[str] | None = None,
    ) -> PublishingPlan:
        """Crea un piano di pubblicazione cross-platform."""
        return self.publishing_workflow.create_publishing_plan(
            creator_name=creator_name,
            platforms=platforms,
            audience_demographics=audience_data,
            content_volume=weekly_content_volume,
            trip_dates=trip_dates,
            destinations=destinations,
        )

    def run_owner_review(
        self,
        weekly_metrics_list: list[dict[str, Any]],
        weekly_deliverables: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Esegue il ciclo completo di revisione del proprietario (6 settimane).

        Args:
            weekly_metrics_list: Lista di 6 dizionari con metriche settimanali
            weekly_deliverables: Descrizione dei contenuti consegnati per settimana
        """
        return self.owner_review_workflow.run_full_program(
            weekly_metrics_list=weekly_metrics_list,
            weekly_deliverables=weekly_deliverables,
        )

    def list_trips(self, creator_name: str | None = None) -> list:
        """Lista tutti i viaggi registrati."""
        return self.content_manager.list_trips(creator_name)

    def get_agency_status(self) -> dict[str, Any]:
        """Ritorna lo status corrente dell'agenzia."""
        trips = self.content_manager.list_trips()
        return {
            "agenzia": "TravelVision Agency",
            "team_size": 100,
            "dipartimenti": 6,
            "viaggi_registrati": len(trips),
            "agenti_attivi": {
                "executive": ["CEO Marco Ferretti", "COO Sofia Bianchi", "CMO Luca Marino"],
                "contenuti": ["Alessia Romano (Dir.)", "Davide Conti", "Giulia Ferrara",
                              "Matteo Russo", "Chiara Esposito", "Eleonora Galli",
                              "Lorenzo Moretti", "Valentina De Luca", "Federico Lombardi",
                              "Serena Ricci", "Martina Costa"],
                "social_media": ["Camilla Vitali (Dir.)", "Aurora Pellegrini", "Nicolò Ferretti",
                                 "Beatrice Fontana", "Emanuele Greco", "Roberta Coppola",
                                 "Francesca Amato", "Andrea Morelli", "Simone Caruso"],
                "viaggi": ["Roberto Zanetti (Dir.)", "Isabella Colombo", "Gabriele Serra",
                           "Alessandro Neri", "Claudia Rizzo"],
                "sponsorizzazioni": ["Paola Marchetti (Dir.)", "Giacomo Ferri", "Silvia Montanari",
                                     "Daniele Greco", "Marco Carbone", "Veronica Palumbo"],
                "operations": ["Riccardo Barbieri", "Marta Toscano", "Stefano Manzi",
                               "Antonella Bruno", "Laura Fabbri", "Cristina Ferretti"],
            },
        }
