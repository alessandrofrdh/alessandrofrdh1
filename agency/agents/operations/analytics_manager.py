"""Analytics Manager — raccolta e analisi dati di performance."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class AnalyticsManagerAgent(BaseAgent):
    TOOLS = [
        "calculate_engagement_rate", "calculate_cpm",
        "search_trips", "get_content_inventory",
        "save_report", "read_file",
    ]

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.ANALYTICS_MANAGER,
            name="Stefano Manzi",
            department="Operations",
            specializations=[
                "Google Analytics",
                "social media analytics",
                "data visualization",
                "KPI dashboard",
                "analisi cohort",
                "attribuzione revenue",
            ],
            years_experience=7,
        )

    def define_kpi_framework(
        self,
        business_goals: list[str],
        platforms: list[str],
    ) -> AgentResponse:
        context = {
            "obiettivi_business": business_goals,
            "piattaforme": platforms,
        }
        task = (
            "Definisci un framework di KPI completo. "
            "Per ogni obiettivo: KPI primari e secondari, "
            "come misurarli, frequenza di misurazione, "
            "target e soglie di allerta (verde/giallo/rosso)."
        )
        return self.think_and_respond(task, context)

    def analyze_content_performance_trends(
        self,
        historical_data: dict[str, Any],
        period: str,
    ) -> AgentResponse:
        context = {"dati_storici": historical_data, "periodo": period}
        task = (
            "Analizza i trend di performance dei contenuti. "
            "Identifica: pattern di crescita, contenuti evergreen vs. trending, "
            "correlazioni tra tipologie di contenuto e crescita follower, "
            "stagionalità e previsioni per il prossimo trimestre."
        )
        return self.think_and_respond(task, context)
