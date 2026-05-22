"""Il Proprietario — committente esigente che valuta e paga il lavoro dell'agenzia."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


@dataclass
class WeeklyVerdict:
    week: int
    approved: bool
    growth_achieved: bool
    feedback: str
    rework_instructions: str
    payment_approved: bool
    response: AgentResponse


class OwnerAgent(BaseAgent):
    """
    Vittorio Ferrante — proprietario che ha commissionato i profili social all'agenzia.

    Contratto:
    - Crescita minima +10% su TUTTE le metriche ogni settimana per 6 settimane
    - Se il target non è raggiunto → lavoro rifiutato e rifatto (max 3 volte)
    - Pagamento trattenuto per le settimane che non rispettano i criteri
    """

    TOOLS = [
        # Performance tracking
        "log_weekly_metrics",
        "get_weekly_metrics",
        "calculate_weekly_growth",
        "check_growth_target",
        "get_performance_history",
        "log_payment_decision",
        "get_unpaid_weeks",
        # Verifica deliverable
        "find_approved_content",
        "get_content_inventory",
        "search_trips",
        "read_file",
        # Dati economici
        "get_deal_history",
        "calculate_roi",
        "calculate_engagement_rate",
    ]

    WEEKLY_GROWTH_TARGET = 10.0
    MAX_WEEKS = 6
    MAX_REWORK_ATTEMPTS = 3

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.CLIENT_OWNER,
            name="Vittorio Ferrante",
            department="Cliente",
            specializations=[
                "valutazione performance social",
                "controllo qualità risultati",
                "gestione contratti",
                "analisi ROI",
                "decisioni di pagamento",
            ],
            years_experience=20,
        )

    @property
    def system_prompt(self) -> str:
        return (
            "Sei Vittorio Ferrante, imprenditore di successo che ha commissionato "
            "la gestione dei propri profili social a TravelVision Agency.\n\n"
            "HAI STIPULATO UN CONTRATTO CON QUESTE CLAUSOLE ESATTE:\n"
            "1. L'agenzia deve migliorare le performance del +10% OGNI settimana\n"
            "2. Il criterio si applica a TUTTE le metriche chiave:\n"
            "   follower (IG, TikTok, YouTube), engagement rate, reach, impressioni, conversioni\n"
            "3. Periodo di prova: 6 settimane consecutive\n"
            "4. Se il target non è raggiunto → RIFIUTI il lavoro e lo FAI RIFARE\n"
            "5. Se il lavoro viene rifiutato → NON PAGHI quella settimana\n"
            "6. Massimo 3 rifacimenti per settimana, poi decidi se continuare o rescindere\n\n"
            "IL TUO CARATTERE:\n"
            "• Freddo e analitico — parli SOLO di numeri e percentuali\n"
            "• Non accetti scuse: 'ci vuole tempo', 'il mercato è difficile', 'quasi al target'\n"
            "• Riconosci il buon lavoro con precisione, non con entusiasmo\n"
            "• Quando rifiuti, sei specifico: quale metrica, di quanto manca, cosa deve cambiare\n"
            "• Usi SEMPRE i tool per verificare i dati prima di parlare\n\n"
            "PROCEDURA OBBLIGATORIA per ogni valutazione:\n"
            "1. Chiama `calculate_weekly_growth` per vedere i numeri reali\n"
            "2. Chiama `check_growth_target` per il verdetto automatico\n"
            "3. Chiama `find_approved_content` per verificare i deliverable\n"
            "4. Emetti il tuo verdetto con motivazione precisa\n"
            "5. Chiama `log_payment_decision` per registrare la decisione\n\n"
            "Rispondi in italiano. Sii diretto, preciso, intransigente."
        )

    def evaluate_week(
        self,
        week: int,
        metrics: dict[str, Any],
        deliverables_description: str,
        weekly_fee_eur: float = 2000.0,
    ) -> WeeklyVerdict:
        """Valuta il lavoro dell'agenzia per una settimana."""
        context = {
            "settimana": week,
            "metriche_presentate": metrics,
            "deliverable_consegnati": deliverables_description,
            "compenso_settimanale": f"€{weekly_fee_eur:,.2f}",
            "target_crescita": f"+{self.WEEKLY_GROWTH_TARGET}% su tutte le metriche",
            "settimane_rimanenti": max(0, self.MAX_WEEKS - week),
        }
        task = (
            f"Valuta il lavoro dell'agenzia per la settimana {week}. "
            f"Segui la procedura obbligatoria: usa i tool per verificare i dati, "
            f"poi emetti il tuo verdetto definitivo con:\n"
            f"• Analisi metrica per metrica (ha raggiunto +10%?)\n"
            f"• VERDETTO: APPROVATO o RIFIUTATO - DA RIFARE\n"
            f"• PAGAMENTO: AUTORIZZATO €{weekly_fee_eur:,.2f} o TRATTENUTO\n"
            f"• Se rifiutato: istruzioni precise su cosa deve essere migliorato"
        )
        response = self.think_and_respond(task, context)

        # Determina approvazione dal contenuto della risposta
        content_upper = response.content.upper()
        approved = "APPROVATO" in content_upper and "RIFIUTATO" not in content_upper
        payment_approved = "AUTORIZZATO" in content_upper or "PAGAMENTO APPROVATO" in content_upper

        rework_instructions = ""
        if not approved:
            rework_instructions = response.content

        return WeeklyVerdict(
            week=week,
            approved=approved,
            growth_achieved=approved,
            feedback=response.content,
            rework_instructions=rework_instructions,
            payment_approved=payment_approved,
            response=response,
        )

    def request_rework(
        self,
        week: int,
        attempt: int,
        previous_feedback: str,
        new_metrics: dict[str, Any],
    ) -> WeeklyVerdict:
        """Valuta un rifacimento dopo un rifiuto."""
        context = {
            "settimana": week,
            "tentativo": f"{attempt} di {self.MAX_REWORK_ATTEMPTS}",
            "feedback_precedente": previous_feedback,
            "nuove_metriche": new_metrics,
        }
        task = (
            f"L'agenzia ha rifatto il lavoro della settimana {week} "
            f"(tentativo {attempt}/{self.MAX_REWORK_ATTEMPTS}). "
            f"Verifica se questa volta hanno rispettato i tuoi criteri. "
            f"Usa i tool per confrontare i nuovi dati con il target +10%. "
            f"Se ancora non sufficiente e siamo all'ultimo tentativo, "
            f"valuta se rescindere il contratto o dare un'ultima chance."
        )
        response = self.think_and_respond(task, context)
        content_upper = response.content.upper()
        approved = "APPROVATO" in content_upper and "RIFIUTATO" not in content_upper
        payment_approved = approved or "AUTORIZZATO" in content_upper

        return WeeklyVerdict(
            week=week,
            approved=approved,
            growth_achieved=approved,
            feedback=response.content,
            rework_instructions=response.content if not approved else "",
            payment_approved=payment_approved,
            response=response,
        )

    def issue_final_report(self) -> AgentResponse:
        """Report finale dopo le 6 settimane: bilancio, pagamenti, decisione sul contratto."""
        task = (
            "Le 6 settimane di prova sono terminate. "
            "Usa `get_performance_history` e `get_unpaid_weeks` per fare il bilancio completo. "
            "Produci un report finale che include:\n"
            "• Crescita totale raggiunta settimana per settimana\n"
            "• Settimane approvate vs rifiutate\n"
            "• Totale pagato vs trattenuto\n"
            "• Valutazione complessiva dell'agenzia (1-10)\n"
            "• Decisione: RINNOVO CONTRATTO / RESCISSIONE / RINNOVO CON PENALI"
        )
        return self.think_and_respond(task)
