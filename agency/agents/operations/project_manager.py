"""Project Manager — coordinamento progetti e gestione timeline."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class ProjectManagerAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.PROJECT_MANAGER,
            name="Riccardo Barbieri",
            department="Operations",
            specializations=[
                "project management",
                "Agile/Scrum",
                "gestione risorse",
                "risk management",
                "reporting avanzamento",
                "coordinamento multi-team",
            ],
            years_experience=7,
        )

    def create_project_plan(
        self,
        project_name: str,
        objectives: list[str],
        team_members: list[str],
        deadline: str,
        constraints: list[str],
    ) -> AgentResponse:
        context = {
            "nome_progetto": project_name,
            "obiettivi": objectives,
            "membri_team": team_members,
            "deadline": deadline,
            "vincoli": constraints,
        }
        task = (
            "Crea un piano di progetto completo con metodologia Agile. "
            "Includi: work breakdown structure, sprint planning (2 settimane), "
            "matrice RACI, risk register con mitigation plan, "
            "milestone principali e piano di comunicazione al team."
        )
        return self.think_and_respond(task, context)

    def generate_status_report(
        self,
        project_name: str,
        completed_tasks: list[str],
        in_progress: list[str],
        blockers: list[str],
        next_week: list[str],
    ) -> AgentResponse:
        context = {
            "progetto": project_name,
            "completati": completed_tasks,
            "in_corso": in_progress,
            "blocchi": blockers,
            "prossima_settimana": next_week,
        }
        task = (
            "Genera uno status report settimanale. "
            "Struttura: semaforo (verde/giallo/rosso), avanzamento percentuale, "
            "summary esecutivo (3 righe), dettaglio task, "
            "azioni per sbloccare i blocchi e rischi emergenti."
        )
        return self.think_and_respond(task, context)
