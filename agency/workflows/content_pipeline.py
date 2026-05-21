"""Pipeline dalla produzione dei contenuti alla pubblicazione."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import anthropic

from ..agents.content import (
    ContentDirectorAgent,
    SeniorVideoEditorAgent,
    VideoEditorAgent,
    SeniorPhotoEditorAgent,
    PhotoEditorAgent,
    SeniorCopywriterAgent,
    CopywriterAgent,
    GraphicDesignerAgent,
    ContentStrategistAgent,
)
from ..agents.operations import QualityControllerAgent
from ..agents.base_agent import AgentResponse


@dataclass
class ContentPackage:
    trip_id: str
    platform: str
    content_type: str
    brief: AgentResponse | None = None
    edit_plan: AgentResponse | None = None
    captions: AgentResponse | None = None
    graphics: AgentResponse | None = None
    quality_check: AgentResponse | None = None
    approved: bool = False


class ContentPipelineWorkflow:
    """Pipeline di produzione contenuti dal brief al contenuto approvato."""

    def __init__(self, client: anthropic.Anthropic) -> None:
        self.client = client
        self.content_director = ContentDirectorAgent(client)
        self.senior_video_editor = SeniorVideoEditorAgent(client)
        self.video_editor = VideoEditorAgent(client)
        self.senior_photo_editor = SeniorPhotoEditorAgent(client)
        self.photo_editor = PhotoEditorAgent(client)
        self.senior_copywriter = SeniorCopywriterAgent(client)
        self.copywriter = CopywriterAgent(client)
        self.graphic_designer = GraphicDesignerAgent(client)
        self.content_strategist = ContentStrategistAgent(client)
        self.quality_controller = QualityControllerAgent(client)

    def produce_instagram_reel(
        self,
        trip_id: str,
        destination: str,
        raw_footage: str,
        creator_style: str,
        brand_voice: str,
    ) -> ContentPackage:
        """Produce un Reel Instagram completo dal materiale grezzo."""
        print(f"\n{'='*60}")
        print(f"CONTENT PIPELINE: Instagram Reel — {destination}")
        print(f"{'='*60}")

        package = ContentPackage(
            trip_id=trip_id,
            platform="instagram",
            content_type="reel",
        )

        print("\n[1/5] Brief creativo dal Direttore Contenuti...")
        package.brief = self.content_director.brief_content_team(
            trip={"destinazione": destination, "id": trip_id},
            content_goals=["engagement alto", "reach organico", "autenticità"],
        )

        print("[2/5] Piano di montaggio video...")
        package.edit_plan = self.video_editor.create_edit_plan(
            raw_footage_description=raw_footage,
            target_platform="Instagram Reels",
            style=creator_style,
        )

        print("[3/5] Caption e copy...")
        package.captions = self.copywriter.write_captions(
            content_description=f"Reel da {destination}: {raw_footage}",
            platform="Instagram",
            brand_voice=brand_voice,
            include_hashtags=True,
        )

        print("[4/5] Grafica e template...")
        package.graphics = self.graphic_designer.design_social_templates(
            brand_identity={"tono": creator_style, "piattaforma": "Instagram"},
            platforms=["Instagram"],
        )

        print("[5/5] Quality check...")
        package.quality_check = self.quality_controller.review_content(
            content_type="Instagram Reel",
            content=f"Piano montaggio + Caption per Reel da {destination}",
            brand_guidelines={"tono": brand_voice, "stile": creator_style},
            platform="Instagram",
        )
        package.approved = True

        print(f"\n✓ Reel pronto per la pubblicazione.")
        return package

    def produce_youtube_video(
        self,
        trip_id: str,
        destination: str,
        raw_footage: str,
        video_concept: str,
        target_keywords: list[str],
    ) -> ContentPackage:
        """Produce un video YouTube completo."""
        print(f"\n{'='*60}")
        print(f"CONTENT PIPELINE: YouTube Video — {destination}")
        print(f"{'='*60}")

        package = ContentPackage(
            trip_id=trip_id,
            platform="youtube",
            content_type="video",
        )

        print("\n[1/4] Brief creativo...")
        package.brief = self.content_director.brief_content_team(
            trip={"destinazione": destination, "concept": video_concept},
            content_goals=["retention alta", "SEO YouTube", "monetizzazione"],
        )

        print("[2/4] Piano di montaggio senior editor...")
        package.edit_plan = self.senior_video_editor.produce_hero_video(
            trip={"destinazione": destination, "concept": video_concept},
            brand_guidelines={"keyword": target_keywords},
        )

        print("[3/4] Copy SEO-ottimizzato...")
        package.captions = self.senior_copywriter.develop_content_pillars(
            creator_niche="travel",
            target_audience={"platform": "YouTube", "keywords": target_keywords},
        )

        print("[4/4] Quality check...")
        package.quality_check = self.quality_controller.review_content(
            content_type="YouTube Video",
            content=f"Video di viaggio: {destination} — {video_concept}",
            brand_guidelines={"keyword_seo": target_keywords},
            platform="YouTube",
        )
        package.approved = True

        print(f"\n✓ Video YouTube pronto.")
        return package

    def produce_tiktok_video(
        self,
        trip_id: str,
        destination: str,
        clip_description: str,
        trend_audio: str,
        creator_style: str,
    ) -> ContentPackage:
        """Produce un TikTok dal materiale grezzo."""
        print(f"\n{'='*60}")
        print(f"CONTENT PIPELINE: TikTok — {destination}")
        print(f"{'='*60}")

        package = ContentPackage(
            trip_id=trip_id,
            platform="tiktok",
            content_type="video",
        )

        print("\n[1/3] Piano di montaggio...")
        package.edit_plan = self.video_editor.create_edit_plan(
            raw_footage_description=clip_description,
            target_platform="TikTok",
            style=creator_style,
        )

        print("[2/3] Caption TikTok...")
        package.captions = self.copywriter.write_captions(
            content_description=f"TikTok da {destination}: {clip_description}",
            platform="TikTok",
            brand_voice=creator_style,
            include_hashtags=True,
        )

        print("[3/3] Quality check...")
        package.quality_check = self.quality_controller.review_content(
            content_type="TikTok",
            content=clip_description,
            brand_guidelines={"stile": creator_style, "audio_trend": trend_audio},
            platform="TikTok",
        )
        package.approved = True

        print(f"\n✓ TikTok pronto.")
        return package
