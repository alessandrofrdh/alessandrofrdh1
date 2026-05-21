"""Analista ROI — misurazione del ritorno sugli investimenti delle campagne."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class ROIAnalystAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.ROI_ANALYST,
            name="Veronica Palumbo",
            department="Sponsorizzazioni",
            specializations=[
                "calcolo ROI campagne",
                "analisi conversion",
                "attribuzione multi-touch",
                "benchmark industry",
                "reporting finanziario",
                "previsioni revenue",
            ],
            years_experience=6,
        )

    def calculate_campaign_roi(
        self,
        brand: str,
        campaign_costs: dict[str, float],
        campaign_results: dict[str, Any],
    ) -> AgentResponse:
        context = {
            "brand": brand,
            "costi_campagna": campaign_costs,
            "risultati": campaign_results,
        }
        task = (
            "Calcola il ROI completo di questa campagna per il brand. "
            "Includi: media value earned, CPM effettivo, costo per engagement, "
            "valore stimate delle conversioni, confronto con benchmark industry e "
            "raccomandazione per investimenti futuri."
        )
        return self.think_and_respond(task, context)
