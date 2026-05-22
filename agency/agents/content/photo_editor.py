"""Photo editor — editing e produzione foto per i social."""
from __future__ import annotations

from typing import Any

import anthropic

from ..base_agent import AgentRole, AgentResponse, BaseAgent


class PhotoEditorAgent(BaseAgent):
    TOOLS = ["analyze_image", "analyze_trip_photos", "list_files", "save_report"]

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.PHOTO_EDITOR,
            name="Chiara Esposito",
            department="Contenuti",
            specializations=[
                "retouching fotografico",
                "color grading foto",
                "composizione",
                "Instagram feed aesthetic",
                "fotografia di viaggio",
            ],
            years_experience=5,
        )

    def create_photo_edit_plan(
        self,
        photo_collection: str,
        aesthetic: str,
        platform: str,
    ) -> AgentResponse:
        context = {
            "collezione_foto": photo_collection,
            "estetica_richiesta": aesthetic,
            "piattaforma": platform,
        }
        task = (
            "Crea un piano di editing fotografico per questa collezione. "
            "Includi: preset/LUT consigliato, parametri di editing "
            "(esposizione, contrasto, saturazione, temperatura), "
            "criteri di selezione delle foto migliori e "
            "piano di composizione del feed Instagram."
        )
        return self.think_and_respond(task, context)

    def design_instagram_feed(
        self,
        trip_location: str,
        num_posts: int,
        color_palette: str,
    ) -> AgentResponse:
        context = {
            "destinazione": trip_location,
            "numero_post": num_posts,
            "palette_colori": color_palette,
        }
        task = (
            "Progetta un grid Instagram coerente per questo viaggio. "
            "Definisci: sequenza delle foto, bilanciamento cromatico del grid, "
            "mix tra close-up/wide shot/lifestyle, ratio consigliati e "
            "filtro/preset unificato per la coerenza visiva."
        )
        return self.think_and_respond(task, context)


class SeniorPhotoEditorAgent(BaseAgent):
    TOOLS = [
        "analyze_image", "analyze_trip_photos",
        "list_files", "save_report", "save_brief",
        "search_trips", "get_content_inventory",
    ]

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.PHOTO_EDITOR_SENIOR,
            name="Eleonora Galli",
            department="Contenuti",
            specializations=[
                "fotografia editoriale",
                "direzione artistica",
                "campagne fotografiche brand",
                "retouching avanzato",
                "gestione shooting",
            ],
            years_experience=10,
        )

    def art_direct_shooting(
        self,
        brand: str,
        location: str,
        shot_list: list[str],
    ) -> AgentResponse:
        context = {
            "brand_sponsor": brand,
            "location": location,
            "lista_scatti": shot_list,
        }
        task = (
            "Crea un piano di direzione artistica per questo shooting. "
            "Includi: moodboard testuale, lighting setup, styling consigliato, "
            "angolazioni chiave, scatti hero e varianti, e "
            "linee guida per l'integrazione del brand nelle foto."
        )
        return self.think_and_respond(task, context)


class JuniorPhotoEditorAgent(BaseAgent):
    TOOLS = ["analyze_image", "list_files"]

    def __init__(self, client: anthropic.Anthropic) -> None:
        super().__init__(
            client=client,
            role=AgentRole.PHOTO_EDITOR_JUNIOR,
            name="Lorenzo Moretti",
            department="Contenuti",
            specializations=[
                "editing di base",
                "selezione foto",
                "ridimensionamento per piattaforme",
                "watermarking",
            ],
            years_experience=1,
        )

    def prepare_platform_assets(
        self,
        photos: list[str],
        platforms: list[str],
    ) -> AgentResponse:
        context = {"foto": photos, "piattaforme": platforms}
        task = (
            "Prepara un piano per adattare queste foto a tutte le piattaforme richieste. "
            "Specifica dimensioni, crop, formato file e ottimizzazione per ogni piattaforma."
        )
        return self.think_and_respond(task, context)
