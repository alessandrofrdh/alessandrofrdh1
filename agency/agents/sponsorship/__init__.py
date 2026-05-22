"""Agenti del dipartimento sponsorizzazioni e monetizzazione."""
from .sponsorship_director import SponsorshipDirectorAgent
from .brand_partnerships import BrandPartnershipManagerAgent
from .influencer_relations import InfluencerRelationsAgent
from .revenue_manager import RevenueManagerAgent
from .ad_campaign import AdCampaignManagerAgent
from .roi_analyst import ROIAnalystAgent

__all__ = [
    "SponsorshipDirectorAgent",
    "BrandPartnershipManagerAgent",
    "InfluencerRelationsAgent",
    "RevenueManagerAgent",
    "AdCampaignManagerAgent",
    "ROIAnalystAgent",
]
