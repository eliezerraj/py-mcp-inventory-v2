import logging

from src.mcp_server.domain.usecase.inventory_usecase import InventoryUseCase

from src.mcp_server.config.settings import settings

logger = logging.getLogger(__name__)

def register_inventory_resource(mcp: "MCPServer", inventory_use_case: InventoryUseCase):
    logger.info("Registering inventory resource SUCCESSFULLY.")
    
    @mcp.resource("mcp_info://")
    def mcp_info():
        """
        Provides general information about the mcp server.
        Use this tool when the user asks for server details or status.
        """
        logger.info("Fetching server information.")
        
        return {"status": settings.__dict__}
    
    @mcp.resource("inventory_service_info://")
    async def get_inventory_service_info():
        """
        Retrieves general inventory service information.
        Use this resource to get an overview of the inventory service.
        """
        logger.info(f"Fetching inventory service info")
        
        try:
            response = await inventory_use_case.get_inventory_service_info() 
        except Exception as e:
            logger.error(f"Error fetching inventory service info: {e}")
            response = {"message": e}
        
        return response
    
    @mcp.resource("product://{sku}")
    async def get_product(sku):
        """
        Retrieve product information for a specific SKU.

        Resource URI:
            product://{sku}

        Example:
            product://sku-102
        """
        
        logger.info(f"Fetching product for sku: {sku}")
        
        try:
            response = await inventory_use_case.get_product(sku) 
        except Exception as e:
            logger.error(f"Error fetching product for sku {sku}: {e}")
            response = {"message": e}
        
        return response
    
    return get_inventory_service_info, get_product, mcp_info