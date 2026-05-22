"""Revenue Manager — ottimizzazione e diversificazione delle entrate."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class RevenueManagerAgent(BaseAgent):
    TOOLS = [
        "calculate_monthly_revenue_breakdown", "estimate_influencer_fee",
        "calculate_roi", "calculate_cpm",
        "log_deal", "get_deal_history", "list_brands",
    ]

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.REVENUE_MANAGER,
            name="Daniele Greco",
            department="Sponsorizzazioni",
            specializations=[
                "diversificazione revenue",
                "monetizzazione piattaforme",
                "affiliate marketing",
                "prodotti digitali",
                "subscription model",
                "previsioni finanziarie",
            ],
            years_experience=8,
        )

    def create_revenue_plan(
        self,
        creator_profile: dict[str, Any],
        current_monthly_revenue: float,
        target_monthly_revenue: float,
    ) -> AgentResponse:
        context = {
            "profilo_creator": creator_profile,
            "revenue_mensile_attuale": f"€{current_monthly_revenue:,.2f}",
            "target_mensile": f"€{target_monthly_revenue:,.2f}",
        }
        task = (
            "Crea un piano di monetizzazione diversificato. "
            "Analizza e proponi stream di revenue: sponsorizzazioni dirette, "
            "affiliate marketing, monetizzazione nativa piattaforme, "
            "prodotti digitali (preset, guide, corsi), "
            "subscription/membership, eventi e esperienze. "
            "Per ognuno: stima del potenziale mensile, effort necessario e timeline."
        )
        return self.think_and_respond(task, context)

    def set_pricing_strategy(
        self,
        creator_metrics: dict[str, Any],
        market_benchmarks: dict[str, Any],
    ) -> AgentResponse:
        context = {
            "metriche_creator": creator_metrics,
            "benchmark_mercato": market_benchmarks,
        }
        task = (
            "Definisci la strategia di pricing per le sponsorizzazioni. "
            "Calcola: CPM, CPE, fee per tipologia di contenuto e piattaforma, "
            "pacchetti bundle, sconti per campagne multi-mese e "
            "fee minima per non svalutare il profilo."
        )
        return self.think_and_respond(task, context)
