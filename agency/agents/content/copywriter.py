"""Copywriter — testi, caption e copy per i social."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class CopywriterAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.COPYWRITER,
            name="Valentina De Luca",
            department="Contenuti",
            specializations=[
                "caption social",
                "storytelling",
                "copy per campagne sponsorizzate",
                "hashtag strategy",
                "call-to-action",
            ],
            years_experience=4,
        )

    def write_captions(
        self,
        content_description: str,
        platform: str,
        brand_voice: str,
        include_hashtags: bool = True,
    ) -> AgentResponse:
        context = {
            "descrizione_contenuto": content_description,
            "piattaforma": platform,
            "tono_brand": brand_voice,
            "includi_hashtag": include_hashtags,
        }
        task = (
            "Scrivi 3 varianti di caption per questo contenuto. "
            "Per ogni variante specifica: hook d'apertura, corpo del testo, "
            "call-to-action e (se richiesti) hashtag ottimizzati per la piattaforma. "
            "Le varianti devono differire per lunghezza e approccio emotivo."
        )
        return self.think_and_respond(task, context)

    def write_sponsored_content(
        self,
        brand: str,
        product: str,
        key_messages: list[str],
        platform: str,
    ) -> AgentResponse:
        context = {
            "brand": brand,
            "prodotto": product,
            "messaggi_chiave": key_messages,
            "piattaforma": platform,
        }
        task = (
            "Scrivi il copy per un contenuto sponsorizzato. "
            "Deve sembrare autentico e non pubblicitario, integrare naturalmente "
            "il messaggio del brand, rispettare le normative (disclosure #ad/#sponsored) "
            "e massimizzare l'engagement. Fornisci 2 versioni: corta e lunga."
        )
        return self.think_and_respond(task, context)


class SeniorCopywriterAgent(BaseAgent):
    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.COPYWRITER_SENIOR,
            name="Federico Lombardi",
            department="Contenuti",
            specializations=[
                "brand storytelling",
                "content strategy",
                "copywriting persuasivo",
                "email marketing",
                "pitch per brand",
                "comunicati stampa",
            ],
            years_experience=8,
        )

    def write_brand_pitch(
        self,
        creator_profile: dict[str, Any],
        target_brand: str,
        collaboration_type: str,
    ) -> AgentResponse:
        context = {
            "profilo_creator": creator_profile,
            "brand_target": target_brand,
            "tipo_collaborazione": collaboration_type,
        }
        task = (
            "Scrivi un pitch professionale per proporre una collaborazione con questo brand. "
            "Includi: opening hook, valore del creator, sinergia con il brand, "
            "proposta concreta di collaborazione, risultati attesi e call-to-action. "
            "Tono professionale ma personale, max 300 parole."
        )
        return self.think_and_respond(task, context)

    def develop_content_pillars(
        self,
        creator_niche: str,
        target_audience: dict[str, Any],
    ) -> AgentResponse:
        context = {
            "nicchia_creator": creator_niche,
            "pubblico_target": target_audience,
        }
        task = (
            "Sviluppa i 5 pillar di contenuto per questo creator. "
            "Per ogni pillar: nome, descrizione, tipologie di contenuto, "
            "frequenza consigliata e esempi concreti di post/video."
        )
        return self.think_and_respond(task, context)
