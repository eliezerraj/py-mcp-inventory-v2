import logging

from src.mcp_server.domain.dto.context import SecurityContext
from src.mcp_server.domain.usecase.inventory_usecase import InventoryUseCase

logger = logging.getLogger(__name__)
    
def register_inventory_tool(mcp: "MCPServer", inventory_use_case: InventoryUseCase):
    logger.info("Registering inventory tool SUCCESSFULLY.")

    @mcp.tool()
    async def get_inventory_info():
        """
        Retrieves general inventory information.
        Use this tool when the user wants to get an overview of the inventory.
        """
        logger.info(f"Fetching inventory info")
        
        try:
            response = await inventory_use_case.get_inventory_info() 
        except Exception as e:
            logger.error(f"Error fetching inventory info: {e}")
            response = {"message": e}
        
        return response

    @mcp.tool()
    async def get_product(sku):
        """
        Retrieves product information for a given SKU.
        Use this tool when the user wants to get details about a specific product.
        """
        logger.info(f"Fetching product for sku: {sku}")
        
        try:
            response = await inventory_use_case.get_product(sku) 
        except Exception as e:
            logger.error(f"Error fetching product for sku {sku}: {e}")
            response = {"message": e}
        
        return response

    @mcp.tool()
    async def post_product(sku):
        """
        Creates product information for a given SKU.
        Use this tool when the user wants to add or modify details about a specific product.
        """
        logger.info(f"Creating product for sku: {sku}")
        
        try:
            response = await inventory_use_case.post_product(sku) 
        except Exception as e:
            logger.error(f"Error creating product for sku {sku}: {e}")
            response = {"message": e}
        
        return response

    return get_inventory_info, get_product, post_product