import logging
from src.mcp_server.domain.dto.context import SecurityContext

logger = logging.getLogger(__name__)

class InventoryUseCase:
    
    def __init__(self, inventory_adapter):
        logger.info("InventoryUseCase initialized SUCCESSFULLY.")
        self.inventory_adapter = inventory_adapter
            
    async def get_inventory_info(self):
        logger.info(f"Fetching inventory info asynchronously")
        
        try:
            response = await self.inventory_adapter.get_inventory_info()
        except Exception as e:
            logger.error(f"Error fetching inventory info asynchronously: {e}")
            response = {"message": e}
        
        return response

    async def get_product(self, sku):
        logger.info(f"Fetching product for sku: {sku}")
        
        try:
            response = await self.inventory_adapter.get_product(sku)
        except Exception as e:
            logger.error(f"Error fetching product for sku {sku}: {e}")
            response = {"message": e}

        return response    
 
    async def post_product(self, sku):
        logger.info(f"Creating product for sku: {sku}")
        
        try:
            response = await self.inventory_adapter.post_product(sku)
        except Exception as e:
            logger.error(f"Error creating product for sku {sku}: {e}")
            response = {"message": e}

        return response   
        