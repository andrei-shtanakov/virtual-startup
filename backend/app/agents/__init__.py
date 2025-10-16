"""Agent system for the virtual startup.

This package contains all agent implementations and management.
"""

from .base_agent import BaseVirtualAgent
from .driver import DriverAgent
from .creator import CreatorAgent
from .generator import GeneratorAgent
from .manager import AgentManager, agent_manager
from .config import (
    get_model_client,
    AGENT_CONFIGS,
    DRIVER_SYSTEM_PROMPT,
    CREATOR_SYSTEM_PROMPT,
    GENERATOR_SYSTEM_PROMPT,
)

__all__ = [
    "BaseVirtualAgent",
    "DriverAgent",
    "CreatorAgent",
    "GeneratorAgent",
    "AgentManager",
    "agent_manager",
    "get_model_client",
    "AGENT_CONFIGS",
    "DRIVER_SYSTEM_PROMPT",
    "CREATOR_SYSTEM_PROMPT",
    "GENERATOR_SYSTEM_PROMPT",
]
