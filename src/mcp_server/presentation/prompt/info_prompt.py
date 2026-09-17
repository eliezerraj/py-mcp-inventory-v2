import logging

from mcp.server.fastmcp import FastMCP

from mcp_server.presentation.prompt.templates.inventory_prompt_templates import (
    INFORMATION_OVERVIEW_PROMPT,
)

logger = logging.getLogger(__name__)

def register_info_prompts(mcp: FastMCP) -> None:
    """
    Register info-related MCP prompts.

    MCP prompts provide reusable interaction templates for
    information analysis and monitoring workflows.
    """

    @mcp.prompt()
    def information_overview() -> str:
        """
        Start an information overview and monitoring workflow.

        Use this prompt when the user wants to understand the
        current state of the information and identify areas
        that may require attention.
        """

        logger.info("Information overview prompt requested")

        return INFORMATION_OVERVIEW_PROMPT

def register_prompts(mcp: FastMCP) -> None:
    """
    Register all MCP prompts.
    """

    register_info_prompts(mcp)