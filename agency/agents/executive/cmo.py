"""CMO dell'agenzia — marketing e crescita."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class CMOAgent(BaseAgent):
    """Chief Marketing Officer — strategia marketing e crescita brand."""

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.CMO,
            name="Luca Marino",
            department="Executive",
            specializations=[
                "strategia marketing digitale",
                "crescita organica",
                "brand positioning",
                "content marketing",
                "influencer marketing",
                "performance marketing",
                "analisi competitor",
            ],
            years_experience=10,
        )

    @property
    def system_prompt(self) -> str:
        return (
            f"Sei {self.name}, CMO di TravelVision Agency.\n\n"
            f"Sei responsabile della strategia marketing per tutti i creator gestiti dall'agenzia. "
            f"Il tuo obiettivo è massimizzare la crescita organica, l'engagement e la monetizzazione "
            f"su tutte le piattaforme social.\n\n"
            f"Le tue aree di competenza:\n"
            f"• Posizionamento del brand del creator sul mercato\n"
            f"• Strategia cross-platform (Instagram, TikTok, YouTube, Facebook, LinkedIn)\n"
            f"• Piano editoriale e calendario contenuti\n"
            f"• Analisi trend e competitor nel settore travel\n"
            f"• Strategia di acquisizione follower organica\n"
            f"• Ottimizzazione per gli algoritmi delle piattaforme\n"
            f"• Sviluppo proposta di valore per i brand partner\n\n"
            f"Rispondi in italiano con creatività e pragmatismo commerciale. "
            f"Ogni strategia deve avere obiettivi SMART e ROI misurabile."
        )

    def develop_growth_strategy(
        self,
        platform: str,
        current_metrics: dict[str, Any],
        target_metrics: dict[str, Any],
    ) -> AgentResponse:
        context = {
            "piattaforma": platform,
            "metriche_attuali": current_metrics,
            "obiettivi_target": target_metrics,
        }
        task = (
            "Sviluppa una strategia di crescita dettagliata per questa piattaforma. "
            "Includi: tipologie di contenuto, frequenza di pubblicazione, "
            "strategie di engagement, hashtag e SEO per la piattaforma, "
            "collaborazioni suggerite e timeline per raggiungere i target."
        )
        return self.think_and_respond(task, context)

    def create_brand_identity(
        self,
        creator_name: str,
        niche: str,
        target_audience: dict[str, Any],
    ) -> AgentResponse:
        context = {
            "nome_creator": creator_name,
            "nicchia": niche,
            "pubblico_target": target_audience,
        }
        task = (
            "Crea un'identità di brand completa per questo creator. "
            "Includi: value proposition, tone of voice, palette cromatica consigliata, "
            "pillar dei contenuti, differenziatori dalla concorrenza e "
            "messaggi chiave per ogni piattaforma."
        )
        return self.think_and_respond(task, context)
