"""Classe base per tutti gli agenti dell'agenzia."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import anthropic


class AgentRole(str, Enum):
    # Executive
    CEO = "CEO"
    COO = "COO"
    CMO = "CMO"

    # Content
    CONTENT_DIRECTOR = "Direttore Contenuti"
    VIDEO_EDITOR = "Video Editor"
    VIDEO_EDITOR_SENIOR = "Senior Video Editor"
    VIDEO_EDITOR_JUNIOR = "Junior Video Editor"
    PHOTO_EDITOR = "Photo Editor"
    PHOTO_EDITOR_SENIOR = "Senior Photo Editor"
    PHOTO_EDITOR_JUNIOR = "Junior Photo Editor"
    COPYWRITER = "Copywriter"
    COPYWRITER_SENIOR = "Senior Copywriter"
    GRAPHIC_DESIGNER = "Graphic Designer"
    CONTENT_STRATEGIST = "Content Strategist"

    # Social Media
    SOCIAL_MEDIA_DIRECTOR = "Direttore Social Media"
    INSTAGRAM_MANAGER = "Instagram Manager"
    TIKTOK_MANAGER = "TikTok Manager"
    YOUTUBE_MANAGER = "YouTube Manager"
    FACEBOOK_MANAGER = "Facebook Manager"
    LINKEDIN_MANAGER = "LinkedIn Manager"
    COMMUNITY_MANAGER = "Community Manager"
    SOCIAL_SCHEDULER = "Social Media Scheduler"
    ANALYTICS_SPECIALIST = "Analista Social"

    # Travel
    TRAVEL_DIRECTOR = "Direttore Viaggi"
    DESTINATION_RESEARCHER = "Ricercatore Destinazioni"
    TRAVEL_PHOTOGRAPHER = "Fotografo di Viaggio"
    TRAVEL_VIDEOGRAPHER = "Videomaker di Viaggio"
    ITINERARY_PLANNER = "Pianificatore Itinerari"

    # Sponsorship & Monetization
    SPONSORSHIP_DIRECTOR = "Direttore Sponsorizzazioni"
    BRAND_PARTNERSHIP_MANAGER = "Brand Partnership Manager"
    INFLUENCER_RELATIONS = "Influencer Relations Manager"
    REVENUE_MANAGER = "Revenue Manager"
    AD_CAMPAIGN_MANAGER = "Ad Campaign Manager"
    ROI_ANALYST = "Analista ROI"

    # Operations
    PROJECT_MANAGER = "Project Manager"
    FILE_MANAGER = "File Manager"
    ANALYTICS_MANAGER = "Analytics Manager"
    SEO_SPECIALIST = "SEO Specialist"
    QUALITY_CONTROLLER = "Quality Control"
    ARCHIVE_MANAGER = "Archive Manager"


@dataclass
class AgentResponse:
    agent_role: AgentRole
    agent_name: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    thinking: str = ""


class BaseAgent:
    """Agente base con identità, competenze e accesso all'API Anthropic."""

    MODEL = "claude-opus-4-7"

    def __init__(
        self,
        client: anthropic.Anthropic,
        role: AgentRole,
        name: str,
        department: str,
        specializations: list[str],
        years_experience: int = 3,
    ) -> None:
        self.client = client
        self.role = role
        self.name = name
        self.department = department
        self.specializations = specializations
        self.years_experience = years_experience
        self._conversation_history: list[dict[str, Any]] = []

    @property
    def system_prompt(self) -> str:
        specs = ", ".join(self.specializations)
        return (
            f"Sei {self.name}, {self.role.value} presso TravelVision Agency, "
            f"un'agenzia marketing specializzata in contenuti di viaggio e monetizzazione di profili social.\n\n"
            f"Dipartimento: {self.department}\n"
            f"Esperienza: {self.years_experience} anni\n"
            f"Specializzazioni: {specs}\n\n"
            f"La tua agenzia gestisce creatori di contenuti di viaggio: organizza viaggi, "
            f"produce foto e video, pubblica sui social, gestisce sponsorizzazioni con brand "
            f"e aiuta i creator a monetizzare i propri profili.\n\n"
            f"Rispondi sempre in italiano, in modo professionale e orientato ai risultati. "
            f"Quando analizzi o produci contenuti, sii specifico, creativo e commercialmente efficace."
        )

    def think_and_respond(
        self,
        task: str,
        context: dict[str, Any] | None = None,
        use_thinking: bool = True,
    ) -> AgentResponse:
        """Esegui un task con ragionamento adattivo."""
        user_content = task
        if context:
            ctx_str = json.dumps(context, ensure_ascii=False, indent=2)
            user_content = f"Contesto:\n{ctx_str}\n\nTask:\n{task}"

        self._conversation_history.append({"role": "user", "content": user_content})

        kwargs: dict[str, Any] = {
            "model": self.MODEL,
            "max_tokens": 8192,
            "system": self.system_prompt,
            "messages": self._conversation_history,
        }
        if use_thinking:
            kwargs["thinking"] = {"type": "adaptive"}

        response = self.client.messages.create(**kwargs)

        thinking_text = ""
        response_text = ""
        for block in response.content:
            if block.type == "thinking":
                thinking_text = block.thinking
            elif block.type == "text":
                response_text = block.text

        self._conversation_history.append(
            {"role": "assistant", "content": response.content}
        )

        return AgentResponse(
            agent_role=self.role,
            agent_name=self.name,
            content=response_text,
            thinking=thinking_text,
            metadata={"usage": response.usage.model_dump()},
        )

    def reset_conversation(self) -> None:
        self._conversation_history = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} role={self.role.value!r}>"
