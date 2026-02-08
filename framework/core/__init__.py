"""
Framework Core Module

Provides core functionality for the multi-agentic system framework:
- LLM client for Azure OpenAI
- Check mechanism for testing and fixing systems
"""

from .llm_client import AzureLLMClient, get_llm_client
from .chk import CheckMechanism, run_check

__all__ = [
    "AzureLLMClient",
    "get_llm_client",
    "CheckMechanism",
    "run_check",
]
