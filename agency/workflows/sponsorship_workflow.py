"""Workflow per la gestione delle sponsorizzazioni dal prospecting alla pubblicazione."""
from __future__ import annotations

from dataclasses import dataclass

import anthropic

from ..agents.sponsorship import (
    SponsorshipDirectorAgent,
    BrandPartnershipManagerAgent,
    InfluencerRelationsAgent,
    RevenueManagerAgent,
    ROIAnalystAgent,
)
from ..agents.content import SeniorCopywriterAgent
from ..agents.base_agent import AgentResponse


@dataclass
class SponsorshipDeal:
    brand: str
    creator_name: str
    collaboration_type: str
    pitch: AgentResponse | None = None
    deal_evaluation: AgentResponse | None = None
    content_brief: AgentResponse | None = None
    sponsored_copy: AgentResponse | None = None
    campaign_report: AgentResponse | None = None


class SponsorshipWorkflow:
    """Gestisce l'intero ciclo di vita di una sponsorizzazione."""

    def __init__(self, client: anthropic.Anthropic) -> None:
        self.client = client
        self.sponsorship_director = SponsorshipDirectorAgent(client)
        self.brand_manager = BrandPartnershipManagerAgent(client)
        self.influencer_relations = InfluencerRelationsAgent(client)
        self.revenue_manager = RevenueManagerAgent(client)
        self.roi_analyst = ROIAnalystAgent(client)
        self.senior_copywriter = SeniorCopywriterAgent(client)

    def outreach_brand(
        self,
        creator_profile: dict,
        target_brand: str,
        collaboration_idea: str,
    ) -> SponsorshipDeal:
        """Processo di outreach verso un brand target."""
        print(f"\n{'='*60}")
        print(f"SPONSORSHIP OUTREACH: {target_brand}")
        print(f"{'='*60}")

        deal = SponsorshipDeal(
            brand=target_brand,
            creator_name=creator_profile.get("nome", "Creator"),
            collaboration_type=collaboration_idea,
        )

        print("\n[1/2] Scrittura pitch professionale...")
        deal.pitch = self.senior_copywriter.write_brand_pitch(
            creator_profile=creator_profile,
            target_brand=target_brand,
            collaboration_type=collaboration_idea,
        )

        print("[2/2] Identificazione target brand aggiuntivi...")
        deal.deal_evaluation = self.influencer_relations.identify_brand_targets(
            creator_niche=creator_profile.get("nicchia", "travel"),
            audience_demographics=creator_profile.get("demographics", {}),
            excluded_brands=[target_brand],
        )

        print(f"\n✓ Outreach pronto per {target_brand}.")
        return deal

    def manage_incoming_deal(
        self,
        brand: str,
        creator_profile: dict,
        brand_brief: dict,
        creator_values: list[str],
        platform: str,
        key_messages: list[str],
    ) -> SponsorshipDeal:
        """Gestisce una proposta ricevuta da un brand."""
        print(f"\n{'='*60}")
        print(f"DEAL MANAGEMENT: {brand}")
        print(f"{'='*60}")

        deal = SponsorshipDeal(
            brand=brand,
            creator_name=creator_profile.get("nome", "Creator"),
            collaboration_type=brand_brief.get("tipo", "post sponsorizzato"),
        )

        print("\n[1/3] Valutazione proposta...")
        deal.deal_evaluation = self.sponsorship_director.evaluate_sponsorship_deal(
            brand=brand,
            offer_details=brand_brief,
            creator_values=creator_values,
        )

        print("[2/3] Brief creativo per il creator...")
        deal.content_brief = self.brand_manager.manage_brand_brief(
            brand=brand,
            brief=brand_brief,
            creator_style=creator_profile.get("stile", "autentico"),
        )

        print("[3/3] Copy sponsorizzato...")
        deal.sponsored_copy = self.senior_copywriter.write_brand_pitch(
            creator_profile=creator_profile,
            target_brand=brand,
            collaboration_type=brand_brief.get("tipo", "integrazione organica"),
        )

        print(f"\n✓ Deal gestito per {brand}.")
        return deal

    def report_completed_campaign(
        self,
        brand: str,
        campaign_results: dict,
        campaign_goals: dict,
        campaign_costs: dict,
    ) -> SponsorshipDeal:
        """Genera report finale per un brand dopo la campagna."""
        print(f"\n{'='*60}")
        print(f"CAMPAIGN REPORT: {brand}")
        print(f"{'='*60}")

        deal = SponsorshipDeal(
            brand=brand,
            creator_name="",
            collaboration_type="completed",
        )

        print("\n[1/2] Report campagna...")
        deal.campaign_report = self.brand_manager.create_campaign_report(
            brand=brand,
            campaign_results=campaign_results,
            goals=campaign_goals,
        )

        print("[2/2] Analisi ROI...")
        deal.deal_evaluation = self.roi_analyst.calculate_campaign_roi(
            brand=brand,
            campaign_costs=campaign_costs,
            campaign_results=campaign_results,
        )

        print(f"\n✓ Report completato per {brand}.")
        return deal
