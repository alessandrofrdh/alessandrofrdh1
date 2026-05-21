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
class ToolCall:
    name: str
    input: dict[str, Any]
    result: str


@dataclass
class AgentResponse:
    agent_role: AgentRole
    agent_name: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    thinking: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)


class BaseAgent:
    """Agente base con identità, competenze, tool use e accesso all'API Anthropic."""

    MODEL = "claude-opus-4-7"

    # Sottoclassi dichiarano i nomi dei tool che vogliono usare
    TOOLS: list[str] = []

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

        # Risolve le definizioni Anthropic per i tool dichiarati
        if self.TOOLS:
            from ..tools.definitions import get_tools_by_name
            self._tool_definitions = get_tools_by_name(self.TOOLS)
        else:
            self._tool_definitions = []

    @property
    def system_prompt(self) -> str:
        specs = ", ".join(self.specializations)
        tool_note = (
            f"\n\nHai accesso a {len(self._tool_definitions)} tool che puoi usare per "
            f"leggere/scrivere file, consultare database e fare calcoli. Usali quando necessario."
            if self._tool_definitions else ""
        )
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
            f"{tool_note}"
        )

    def think_and_respond(
        self,
        task: str,
        context: dict[str, Any] | None = None,
        use_thinking: bool = True,
        max_tool_iterations: int = 10,
    ) -> AgentResponse:
        """Esegui un task con ragionamento adattivo e loop di tool use."""
        user_content = task
        if context:
            ctx_str = json.dumps(context, ensure_ascii=False, indent=2)
            user_content = f"Contesto:\n{ctx_str}\n\nTask:\n{task}"

        self._conversation_history.append({"role": "user", "content": user_content})

        thinking_text = ""
        response_text = ""
        all_tool_calls: list[ToolCall] = []

        for _ in range(max_tool_iterations):
            kwargs: dict[str, Any] = {
                "model": self.MODEL,
                "max_tokens": 8192,
                "system": self.system_prompt,
                "messages": self._conversation_history,
            }
            if use_thinking:
                kwargs["thinking"] = {"type": "adaptive"}
            if self._tool_definitions:
                kwargs["tools"] = self._tool_definitions

            response = self.client.messages.create(**kwargs)

            # Estrai testo e thinking dall'ultima risposta
            for block in response.content:
                if block.type == "thinking":
                    thinking_text = block.thinking
                elif block.type == "text":
                    response_text = block.text

            # Aggiungi la risposta dell'assistente alla history
            self._conversation_history.append(
                {"role": "assistant", "content": response.content}
            )

            # Se il modello ha chiamato dei tool, eseguili e continua il loop
            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = self._execute_tool(block.name, block.input)
                        all_tool_calls.append(
                            ToolCall(name=block.name, input=block.input, result=result)
                        )
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })
                self._conversation_history.append(
                    {"role": "user", "content": tool_results}
                )
            else:
                # stop_reason == "end_turn" — il modello ha finito
                break

        return AgentResponse(
            agent_role=self.role,
            agent_name=self.name,
            content=response_text,
            thinking=thinking_text,
            tool_calls=all_tool_calls,
            metadata={"usage": response.usage.model_dump()},
        )

    def _execute_tool(self, tool_name: str, tool_input: dict[str, Any]) -> str:
        from ..tools.executor import execute_tool
        return execute_tool(tool_name, tool_input)

    def reset_conversation(self) -> None:
        self._conversation_history = []

    def __repr__(self) -> str:
        tools_info = f", tools={len(self._tool_definitions)}" if self._tool_definitions else ""
        return f"<{self.__class__.__name__} name={self.name!r} role={self.role.value!r}{tools_info}>"
