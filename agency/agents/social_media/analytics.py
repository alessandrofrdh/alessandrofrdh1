"""Analista Social Media — metriche e performance dei canali."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class SocialAnalyticsAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.ANALYTICS_SPECIALIST,
            name="Simone Caruso",
            department="Social Media",
            specializations=[
                "analisi metriche social",
                "reporting performance",
                "audience insights",
                "A/B testing contenuti",
                "benchmark competitor",
                "previsioni crescita",
            ],
            years_experience=5,
        )

    def analyze_performance(
        self,
        platform: str,
        metrics: dict[str, Any],
        period: str,
    ) -> AgentResponse:
        context = {
            "piattaforma": platform,
            "metriche": metrics,
            "periodo": period,
        }
        task = (
            "Analizza le performance di questo periodo. "
            "Identifica: contenuti migliori e peggiori, trend di crescita, "
            "audience insights chiave, anomalie e opportunità. "
            "Fornisci raccomandazioni concrete per il prossimo periodo."
        )
        return self.think_and_respond(task, context)

    def generate_monthly_report(
        self,
        all_platforms_data: dict[str, Any],
        goals: dict[str, Any],
    ) -> AgentResponse:
        context = {
            "dati_tutte_piattaforme": all_platforms_data,
            "obiettivi_mensili": goals,
        }
        task = (
            "Genera un report mensile completo. "
            "Struttura: executive summary, performance per piattaforma, "
            "raggiungimento obiettivi, top 3 insight del mese, "
            "raccomandazioni per il mese successivo e previsioni."
        )
        return self.think_and_respond(task, context)
