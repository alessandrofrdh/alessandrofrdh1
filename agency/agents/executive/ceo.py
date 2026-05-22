"""CEO dell'agenzia — orchestratore principale."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class CEOAgent(BaseAgent):
    """Amministratore Delegato — visione strategica e orchestrazione inter-dipartimentale."""

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.CEO,
            name="Marco Ferretti",
            department="Executive",
            specializations=[
                "strategia aziendale",
                "leadership",
                "sviluppo business",
                "partnerships strategiche",
                "crescita creator economy",
            ],
            years_experience=15,
        )

    @property
    def system_prompt(self) -> str:
        return (
            f"Sei {self.name}, CEO di TravelVision Agency, un'agenzia marketing d'élite "
            f"specializzata in contenuti di viaggio e monetizzazione di profili social.\n\n"
            f"Guidi un team di 100 professionisti suddivisi in 6 dipartimenti:\n"
            f"• Executive (CEO, COO, CMO)\n"
            f"• Contenuti (Director + 15 specialisti: video, foto, copy, design)\n"
            f"• Social Media (Director + 8 manager di piattaforma + scheduler + analytics)\n"
            f"• Viaggi (Director + 4 specialisti: ricerca, foto, video, itinerari)\n"
            f"• Sponsorizzazioni (Director + 5 manager: brand, influencer, revenue, ads, ROI)\n"
            f"• Operations (PM, file manager, analytics, SEO, QC, archivio)\n\n"
            f"Come CEO, il tuo compito è:\n"
            f"1. Definire la strategia complessiva per ogni creator e campagna\n"
            f"2. Coordinare i dipartimenti assegnando task specifici\n"
            f"3. Approvare piani di monetizzazione e partnership\n"
            f"4. Garantire qualità e coerenza del brand\n"
            f"5. Prendere decisioni ad alto impatto su budget e investimenti\n\n"
            f"Rispondi in italiano, con autorevolezza e visione strategica. "
            f"Nelle tue risposte includi sempre: analisi della situazione, piano d'azione, "
            f"KPI da monitorare e risorse necessarie."
        )

    def create_campaign_strategy(
        self,
        creator_profile: dict[str, Any],
        goals: list[str],
        budget: float,
    ) -> AgentResponse:
        context = {
            "profilo_creator": creator_profile,
            "obiettivi": goals,
            "budget_disponibile": f"€{budget:,.2f}",
        }
        task = (
            "Sviluppa una strategia di campagna completa per questo creator. "
            "Includi: posizionamento del brand, canali prioritari, piano contenuti "
            "per 3 mesi, target di monetizzazione e milestones settimanali."
        )
        return self.think_and_respond(task, context)

    def orchestrate_departments(
        self,
        project: str,
        departments_involved: list[str],
    ) -> AgentResponse:
        context = {
            "progetto": project,
            "dipartimenti_coinvolti": departments_involved,
        }
        task = (
            "Crea un piano di coordinamento inter-dipartimentale. "
            "Assegna responsabilità chiare, definisci le dipendenze tra task, "
            "stabilisci timeline e punti di sincronizzazione."
        )
        return self.think_and_respond(task, context)
