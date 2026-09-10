import logging

from src.mcp_server.domain.dto.context import SecurityContext
from src.mcp_server.domain.dto.product import ProductPayload
from src.mcp_server.domain.dto.product import PatchInventoryPayload
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
    async def post_product(payload: ProductPayload):
        """
        Creates a new product.

        Use this tool when the user wants to create a product
        or add product information.

        The product must contain:
        - SKU
        - type
        - name
        - status
        - lead time
        - price with currency and amount
        - initial inventory quantity
        """
        
        logger.info(f"Creating product: {payload}")
        
        try:
            response = await inventory_use_case.post_product(payload.model_dump()) 
        except Exception as e:
            logger.error(f"Error creating product for sku {payload.sku}: {e}")
            response = {"message": e}
        
        return response

    @mcp.tool()
    async def put_product(payload: ProductPayload):
        """
        Updates an existing product.

        Use this tool when the user wants to create a product
        or add product information.

        The product must contain:
        - SKU
        - type
        - name
        - status
        - lead time
        - price with currency and amount
        - initial inventory quantity
        """
        
        logger.info(f"Updating product for sku {payload.sku} with payload: {payload}")
        
        try:
            response = await inventory_use_case.put_product(payload.sku, payload.model_dump()) 
        except Exception as e:
            logger.error(f"Error updating product for sku {payload.sku} with payload {payload}: {e}")
            response = {"message": e}
        
        return response

    @mcp.tool()
    async def patch_product(payload: PatchInventoryPayload):
        """
        Updates an inventory.

        Use this tool when the user wants to update the inventory
        or add inventory information.

        The inventory must contain:
        - SKU
        - inventory quantity
        - inventory sold
        - inventory pending
        """
        
        logger.info(f"Patching product for sku {payload.sku} with payload: {payload}")
        
        try:
            response = await inventory_use_case.patch_product(payload.sku, payload.model_dump()) 
        except Exception as e:
            logger.error(f"Error patching product for sku {payload.sku} with payload {payload}: {e}")
            response = {"message": e}
        
        return response
        
    return get_inventory_info, get_product, post_product, put_product, patch_product