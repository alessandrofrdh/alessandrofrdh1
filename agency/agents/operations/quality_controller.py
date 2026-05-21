"""Quality Controller — controllo qualità su contenuti e processi."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class QualityControllerAgent(BaseAgent):
    TOOLS = ["read_file", "write_file", "save_report", "list_trip_structure"]

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.QUALITY_CONTROLLER,
            name="Laura Fabbri",
            department="Operations",
            specializations=[
                "quality assurance contenuti",
                "brand compliance",
                "fact checking",
                "revisione copy",
                "controllo tecnico video/foto",
                "checklist pre-pubblicazione",
            ],
            years_experience=5,
        )

    def review_content(
        self,
        content_type: str,
        content: str,
        brand_guidelines: dict[str, Any],
        platform: str,
    ) -> AgentResponse:
        context = {
            "tipo_contenuto": content_type,
            "contenuto": content,
            "linee_guida_brand": brand_guidelines,
            "piattaforma": platform,
        }
        task = (
            "Esegui un quality check completo su questo contenuto. "
            "Verifica: aderenza alle linee guida brand, accuratezza informazioni, "
            "qualità del copy (grammatica, tono, chiarezza), "
            "conformità alle policy della piattaforma, "
            "disclosure sponsorizzazioni (se applicabile) e "
            "ottimizzazione per l'algoritmo. Fornisci: approvato/da rivedere + feedback specifico."
        )
        return self.think_and_respond(task, context)

    def create_pre_publish_checklist(
        self,
        platform: str,
        content_type: str,
    ) -> AgentResponse:
        context = {"piattaforma": platform, "tipo_contenuto": content_type}
        task = (
            "Crea una checklist pre-pubblicazione completa per questo tipo di contenuto. "
            "Coprire: aspetti tecnici, copy, branding, SEO, disclosure legali e "
            "ottimizzazioni specifiche per la piattaforma."
        )
        return self.think_and_respond(task, context)
