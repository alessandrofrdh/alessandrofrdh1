"""
Workflow di revisione settimanale del proprietario.

Il proprietario valuta ogni settimana: se i risultati non raggiungono
+10% su tutte le metriche, l'agenzia rifà il lavoro (max 3 volte).
Se dopo 3 tentativi il target non è raggiunto, il pagamento viene trattenuto.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import anthropic

from ..agents.client.owner import OwnerAgent, WeeklyVerdict
from ..agents.executive.ceo import CEOAgent
from ..agents.social_media.social_director import SocialMediaDirectorAgent
from ..agents.content.content_strategist import ContentStrategistAgent
from ..tools.performance_tracker import log_weekly_metrics


@dataclass
class WeeklyReviewResult:
    week: int
    final_verdict: WeeklyVerdict
    rework_attempts: int
    agency_responses: list[str] = field(default_factory=list)
    total_paid_eur: float = 0.0


class OwnerReviewWorkflow:
    """
    Ciclo settimanale: agenzia consegna → proprietario valuta → rework se necessario.

    Regole contrattuali:
    - Target: +10% su tutte le metriche ogni settimana
    - Max 3 rework per settimana
    - Pagamento trattenuto se il target non viene raggiunto dopo i rework
    - Dopo 6 settimane: report finale e decisione contratto
    """

    WEEKLY_FEE = 2000.0

    def __init__(self, client: anthropic.Anthropic) -> None:
        self.client = client
        self.owner = OwnerAgent(client)
        self.ceo = CEOAgent(client)
        self.social_director = SocialMediaDirectorAgent(client)
        self.content_strategist = ContentStrategistAgent(client)

    def run_week(
        self,
        week: int,
        metrics: dict[str, Any],
        deliverables: str,
    ) -> WeeklyReviewResult:
        """
        Esegue il ciclo completo per una settimana:
        1. Registra le metriche nel tracker
        2. Il proprietario valuta
        3. Se rifiutato: il CEO risponde con un piano di rework
        4. Si reitera fino ad approvazione o max 3 tentativi
        """
        print(f"\n{'='*65}")
        print(f"SETTIMANA {week} — REVISIONE PROPRIETARIO")
        print(f"{'='*65}")

        # Registra metriche
        log_weekly_metrics(week, metrics)

        result = WeeklyReviewResult(week=week, final_verdict=None, rework_attempts=0)

        # Prima valutazione
        print(f"\n[Vittorio Ferrante] Prima valutazione...")
        verdict = self.owner.evaluate_week(week, metrics, deliverables, self.WEEKLY_FEE)
        result.final_verdict = verdict

        if verdict.approved:
            result.total_paid_eur = self.WEEKLY_FEE
            print(f"\n✅ SETTIMANA {week} APPROVATA — Pagamento €{self.WEEKLY_FEE:,.0f} autorizzato")
            return result

        # Loop di rework
        current_metrics = metrics.copy()
        for attempt in range(1, self.owner.MAX_REWORK_ATTEMPTS + 1):
            result.rework_attempts = attempt
            print(f"\n❌ RIFIUTATO. Tentativo di rework {attempt}/{self.owner.MAX_REWORK_ATTEMPTS}...")

            # CEO risponde al rifiuto con un piano correttivo
            print(f"[Marco Ferretti — CEO] Piano correttivo...")
            ceo_response = self.ceo.think_and_respond(
                task=(
                    f"Il proprietario ha RIFIUTATO il lavoro della settimana {week} "
                    f"(tentativo {attempt}). "
                    f"Il suo feedback è: {verdict.rework_instructions}\n\n"
                    f"Crea un piano d'azione correttivo urgente per il team. "
                    f"Cosa cambia nei contenuti, nella strategia e nei processi "
                    f"per raggiungere il target +10% richiesto?"
                ),
                context={"metriche_attuali": current_metrics, "settimana": week},
            )
            result.agency_responses.append(ceo_response.content)

            # Social director adatta la strategia
            print(f"[Camilla Vitali — Social Director] Revisione strategia...")
            social_response = self.social_director.think_and_respond(
                task=(
                    f"Dobbiamo migliorare del +10% TUTTE queste metriche entro 7 giorni: "
                    f"{current_metrics}. "
                    f"Il proprietario ha rifiutato il lavoro perché: {verdict.rework_instructions}. "
                    f"Proponi azioni concrete e immediate per ogni piattaforma."
                ),
            )
            result.agency_responses.append(social_response.content)

            # Simula metriche migliorate (in produzione reale arriverebbero dall'esterno)
            improved_metrics = _apply_corrective_growth(current_metrics, attempt)
            log_weekly_metrics(week, improved_metrics, notes=f"Rework tentativo {attempt}")
            current_metrics = improved_metrics

            # Proprietario rivaluta
            print(f"[Vittorio Ferrante] Rivalutazione rework {attempt}...")
            verdict = self.owner.request_rework(
                week=week,
                attempt=attempt,
                previous_feedback=verdict.rework_instructions,
                new_metrics=current_metrics,
            )
            result.final_verdict = verdict

            if verdict.approved:
                result.total_paid_eur = self.WEEKLY_FEE
                print(f"\n✅ APPROVATO al tentativo {attempt} — Pagamento €{self.WEEKLY_FEE:,.0f}")
                return result

        # Esauriti i tentativi senza approvazione
        print(
            f"\n🚫 SETTIMANA {week}: target non raggiunto dopo {self.owner.MAX_REWORK_ATTEMPTS} tentativi."
            f"\n   Pagamento €{self.WEEKLY_FEE:,.0f} TRATTENUTO."
        )
        result.total_paid_eur = 0.0
        return result

    def run_full_program(
        self,
        weekly_metrics_list: list[dict[str, Any]],
        weekly_deliverables: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Esegue il programma completo di 6 settimane.

        Args:
            weekly_metrics_list: Lista di 6 dizionari metriche (uno per settimana)
            weekly_deliverables: Descrizione contenuti consegnati per settimana
        """
        if not weekly_deliverables:
            weekly_deliverables = [f"Contenuti settimana {i+1}" for i in range(6)]

        results: list[WeeklyReviewResult] = []
        total_paid = 0.0
        total_due = 0.0

        for week_idx, (metrics, deliverables) in enumerate(
            zip(weekly_metrics_list, weekly_deliverables), start=1
        ):
            result = self.run_week(week_idx, metrics, deliverables)
            results.append(result)
            total_due += self.WEEKLY_FEE
            total_paid += result.total_paid_eur

        # Report finale del proprietario
        print(f"\n{'='*65}")
        print("REPORT FINALE — 6 SETTIMANE COMPLETATE")
        print(f"{'='*65}")
        final_report = self.owner.issue_final_report()

        approved_weeks = sum(1 for r in results if r.final_verdict.approved)
        refused_weeks = len(results) - approved_weeks
        withheld = total_due - total_paid

        summary = {
            "settimane_totali": len(results),
            "settimane_approvate": approved_weeks,
            "settimane_rifiutate": refused_weeks,
            "totale_dovuto": total_due,
            "totale_pagato": total_paid,
            "totale_trattenuto": withheld,
            "risultati_settimanali": [
                {
                    "settimana": r.week,
                    "approvata": r.final_verdict.approved,
                    "rework_effettuati": r.rework_attempts,
                    "pagamento": r.total_paid_eur,
                }
                for r in results
            ],
            "report_finale_proprietario": final_report.content,
        }

        print(f"\nSOMARIO FINANZIARIO:")
        print(f"  Dovuto:    €{total_due:,.2f}")
        print(f"  Pagato:    €{total_paid:,.2f}")
        print(f"  Trattenuto: €{withheld:,.2f}")
        print(f"\n{final_report.content}")

        return summary


def _apply_corrective_growth(metrics: dict[str, Any], attempt: int) -> dict[str, Any]:
    """
    Simula un miglioramento delle metriche dopo un rework.
    In produzione reale i dati arriverebbero dalle piattaforme social.
    Il moltiplicatore aumenta con i tentativi — l'agenzia si impegna di più.
    """
    multipliers = {1: 1.07, 2: 1.10, 3: 1.12}
    mult = multipliers.get(attempt, 1.10)
    improved = {}
    for k, v in metrics.items():
        try:
            improved[k] = round(float(v) * mult, 2)
        except (TypeError, ValueError):
            improved[k] = v
    return improved
