import logging

from src.mcp_server.presentation.prompt.templates.inventory_prompt_templates import (
    INVENTORY_OVERVIEW_PROMPT,
)

logger = logging.getLogger(__name__)

def register_prompt(mcp: "MCPServer") -> None:
    """
    Register all MCP prompts.
    """

    register_inventory_prompt(mcp)
    
def register_inventory_prompt(mcp: "MCPServer") -> None:
    """
    Register inventory-related MCP prompts.

    MCP prompts provide reusable interaction templates for
    inventory analysis and monitoring workflows.
    """

    @mcp.prompt()
    def inventory_overview() -> str:
        """
        Start an inventory overview and monitoring workflow.

        Use this prompt when the user wants to understand the
        current state of the inventory and identify products
        that may require attention.
        """

        logger.info("Inventory overview prompt requested")

        return INVENTORY_OVERVIEW_PROMPT
