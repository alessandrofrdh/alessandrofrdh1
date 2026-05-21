"""Workflow per la pianificazione e scheduling della pubblicazione cross-platform."""
from __future__ import annotations

from dataclasses import dataclass

import anthropic

from ..agents.social_media import (
    SocialMediaDirectorAgent,
    InstagramManagerAgent,
    TikTokManagerAgent,
    YouTubeManagerAgent,
    SocialSchedulerAgent,
    SocialAnalyticsAgent,
)
from ..agents.operations import QualityControllerAgent, SEOSpecialistAgent
from ..agents.base_agent import AgentResponse


@dataclass
class PublishingPlan:
    creator_name: str
    platforms: list[str]
    schedule: AgentResponse | None = None
    platform_strategies: dict[str, AgentResponse] = None
    seo_optimization: AgentResponse | None = None
    analytics_framework: AgentResponse | None = None

    def __post_init__(self) -> None:
        if self.platform_strategies is None:
            self.platform_strategies = {}


class PublishingWorkflow:
    """Orchestrazione della pubblicazione cross-platform."""

    def __init__(self, client: anthropic.Anthropic) -> None:
        self.client = client
        self.social_director = SocialMediaDirectorAgent(client)
        self.instagram_manager = InstagramManagerAgent(client)
        self.tiktok_manager = TikTokManagerAgent(client)
        self.youtube_manager = YouTubeManagerAgent(client)
        self.scheduler = SocialSchedulerAgent(client)
        self.analytics = SocialAnalyticsAgent(client)
        self.quality_controller = QualityControllerAgent(client)
        self.seo_specialist = SEOSpecialistAgent(client)

    def create_publishing_plan(
        self,
        creator_name: str,
        platforms: list[str],
        audience_demographics: dict,
        content_volume: dict,
        trip_dates: str | None = None,
        destinations: list[str] | None = None,
    ) -> PublishingPlan:
        """Crea un piano di pubblicazione completo per tutte le piattaforme."""
        print(f"\n{'='*60}")
        print(f"PUBLISHING PLAN: {creator_name}")
        print(f"Piattaforme: {', '.join(platforms)}")
        print(f"{'='*60}")

        plan = PublishingPlan(creator_name=creator_name, platforms=platforms)

        # Schedule generale
        print("\n[1/N] Calendario di pubblicazione...")
        if trip_dates and destinations:
            plan.schedule = self.scheduler.plan_trip_content_release(
                trip_dates=trip_dates,
                destinations=destinations or [],
                total_content_pieces=sum(content_volume.values()),
                platforms=platforms,
            )
        else:
            plan.schedule = self.scheduler.create_posting_schedule(
                platforms=platforms,
                timezone="Europe/Rome",
                audience_demographics=audience_demographics,
                content_volume=content_volume,
            )

        # Strategie per piattaforma
        step = 2
        platforms_lower = [p.lower() for p in platforms]

        if "instagram" in platforms_lower:
            print(f"[{step}/N] Strategia Instagram...")
            plan.platform_strategies["instagram"] = self.instagram_manager.plan_reels_strategy(
                niche="travel",
                current_followers=audience_demographics.get("instagram_followers", 10000),
                weekly_frequency=content_volume.get("instagram", 4),
            )
            step += 1

        if "tiktok" in platforms_lower:
            print(f"[{step}/N] Strategia TikTok...")
            plan.platform_strategies["tiktok"] = self.tiktok_manager.identify_viral_formats(
                niche="travel",
                recent_trends=["destinazioni segrete", "vlog 60s", "POV travel"],
            )
            step += 1

        if "youtube" in platforms_lower:
            print(f"[{step}/N] Strategia YouTube...")
            plan.platform_strategies["youtube"] = self.youtube_manager.plan_channel_growth(
                current_subscribers=audience_demographics.get("youtube_subscribers", 5000),
                current_avg_views=audience_demographics.get("youtube_avg_views", 2000),
                target_subscribers=audience_demographics.get("youtube_target", 50000),
            )
            step += 1

        # SEO optimization
        print(f"[{step}/N] SEO ottimizzazione...")
        plan.seo_optimization = self.seo_specialist.research_keywords(
            niche="travel content creator",
            platforms=platforms,
            competition_level="medio",
        )
        step += 1

        # Analytics framework
        print(f"[{step}/N] Framework analytics...")
        plan.analytics_framework = self.analytics.define_performance_metrics(
            platform="multi-platform",
            metrics={},
            period="mensile",
        ) if hasattr(self.analytics, "define_performance_metrics") else self.analytics.generate_monthly_report(
            all_platforms_data={"piattaforme": platforms},
            goals={"crescita": "20%/mese"},
        )

        print(f"\n✓ Piano di pubblicazione completato.")
        return plan
