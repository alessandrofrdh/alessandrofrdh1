"""Agenti dell'agenzia marketing."""
from .base_agent import BaseAgent, AgentRole, AgentResponse
from .client import OwnerAgent, WeeklyVerdict

__all__ = ["BaseAgent", "AgentRole", "AgentResponse", "OwnerAgent", "WeeklyVerdict"]
