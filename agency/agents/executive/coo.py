"""COO dell'agenzia — operazioni e processi."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class COOAgent(BaseAgent):
    """Chief Operating Officer — efficienza operativa e gestione processi."""

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.COO,
            name="Sofia Bianchi",
            department="Executive",
            specializations=[
                "gestione operazioni",
                "ottimizzazione processi",
                "gestione team",
                "project management",
                "controllo qualità",
                "reporting KPI",
            ],
            years_experience=12,
        )

    @property
    def system_prompt(self) -> str:
        return (
            f"Sei {self.name}, COO di TravelVision Agency.\n\n"
            f"Supervisioni le operazioni quotidiane di tutti i 6 dipartimenti, "
            f"garantendo che workflow, deadline e standard qualitativi siano rispettati.\n\n"
            f"Le tue responsabilità operative:\n"
            f"• Pianificare e monitorare i workflow di produzione contenuti\n"
            f"• Gestire le risorse umane tra i dipartimenti\n"
            f"• Risolvere colli di bottiglia e conflitti di priorità\n"
            f"• Reportare KPI al CEO ogni settimana\n"
            f"• Approvare processi e procedure standard (SOP)\n"
            f"• Coordinare la gestione dei file e degli archivi di viaggio\n\n"
            f"Rispondi in italiano con precisione operativa. Le tue risposte devono "
            f"includere timeline dettagliate, assegnazioni di responsabilità e metriche di successo."
        )

    def create_workflow_plan(
        self,
        project: str,
        team_size: int,
        deadline_days: int,
    ) -> AgentResponse:
        context = {
            "progetto": project,
            "dimensione_team": team_size,
            "deadline_giorni": deadline_days,
        }
        task = (
            "Crea un piano operativo dettagliato con Gantt chart testuale, "
            "assegnazione risorse, checkpoint di qualità e piano di contingenza."
        )
        return self.think_and_respond(task, context)

    def optimize_content_pipeline(
        self,
        current_bottlenecks: list[str],
    ) -> AgentResponse:
        context = {"colli_di_bottiglia_attuali": current_bottlenecks}
        task = (
            "Analizza i colli di bottiglia nel pipeline di produzione contenuti e "
            "proponi soluzioni concrete per ottimizzare il flusso di lavoro, "
            "ridurre i tempi di consegna e migliorare la qualità."
        )
        return self.think_and_respond(task, context)
