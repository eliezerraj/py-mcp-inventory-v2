import logging
import time

from opentelemetry import trace

from src.mcp_server.domain.model.context import SecurityContext
from src.mcp_server.domain.model.product import (
    ProductPayload,
    PatchInventoryPayload,
    ProductResponse,
    PatchPricePayload,
    Inventory,
)
from src.mcp_server.domain.usecase.inventory_usecase import InventoryUseCase

from src.mcp_server.infrastructure.observability.metric import (
    TOOL_CALLS,
    TOOL_DURATION, 
    TOOL_ERRORS, 
    ACTIVE_REQUESTS
)

#---------------------------------
# Configure logging
#---------------------------------
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

class InventoryTool:
    def __init__(self, mcp: "MCPServer", inventory_use_case: InventoryUseCase):
        self.mcp = mcp
        self.inventory_use_case = inventory_use_case
        
        logger.info("Inventory tool initialized SUCCESSFULLY.")
    
    def register_inventory_tool(self):
        logger.info("Registering inventory tool SUCCESSFULLY.")

        #---------------------------------
        # post_product
        #---------------------------------  
        @self.mcp.tool()
        async def post_product(payload: ProductPayload) -> ProductResponse | dict:
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
                    
            with tracer.start_as_current_span("tool.post_product"): 
                ACTIVE_REQUESTS.inc()
                start_time = time.perf_counter()
            
                try:
                    response = await self.inventory_use_case.post_product(payload.model_dump())
                    
                    product_data = (
                        response.get("product")
                        if isinstance(response, dict) and "product" in response
                        else response
                    )
                    
                    product_response = ProductResponse(
                        id=product_data.get("id") if isinstance(product_data, dict) else None,
                        sku=product_data.get("sku") if isinstance(product_data, dict) else None,
                        name=product_data.get("name") if isinstance(product_data, dict) else None,
                        type=product_data.get("type") if isinstance(product_data, dict) else None,
                        lead_time=product_data.get("lead_time") if isinstance(product_data, dict) else None,
                        price=product_data.get("price") if isinstance(product_data, dict) else None,
                        inventory=product_data.get("inventory") if isinstance(product_data, dict) else None
                    )
                    
                    TOOL_CALLS.labels(tool="post_product").inc()
                except Exception as e:
                    logger.error(f"Error creating product for sku {payload.sku}: {e}")
                    TOOL_ERRORS.labels(tool="post_product").inc()
                    response = {"message": str(e)}
                finally:
                    TOOL_DURATION.labels(tool="post_product").observe(time.perf_counter() - start_time)
                    ACTIVE_REQUESTS.dec()
            
                return {
                    "response": response.get("response") if isinstance(response, dict) else None,
                    "product": product_response.model_dump(exclude_none=True),
                }   

        #---------------------------------
        # patch_product_inventory
        #---------------------------------  
        @self.mcp.tool()
        async def patch_product_inventory(payload: PatchInventoryPayload) -> ProductResponse | dict:
            """
            Updates an inventory.

            Use this tool when the user wants to update the inventory or add inventory information.

            The inventory must contain:
            - SKU
            - inventory quantity
            - inventory sold
            - inventory pending
            """
            logger.info(f"Patching product with payload: {payload}")
                    
            with tracer.start_as_current_span("tool.patch_product_inventory"):
                ACTIVE_REQUESTS.inc()
                start_time = time.perf_counter()
                
                try:
                    response = await self.inventory_use_case.patch_product(payload.model_dump()) 
                    
                    product_data = (
                        response.get("product")
                        if isinstance(response, dict) and "product" in response
                        else response
                    )
                    
                    product_response = ProductResponse(
                        id=product_data.get("id") if isinstance(product_data, dict) else None,
                        sku=product_data.get("sku") if isinstance(product_data, dict) else None,
                        inventory=product_data.get("inventory") if isinstance(product_data, dict) else None,
                    )
                    
                    TOOL_CALLS.labels(tool="patch_product_inventory").inc()
                except Exception as e:
                    TOOL_ERRORS.labels(tool="patch_product_inventory").inc()
                    logger.error(f"Error patching product inventory with payload {payload}: {e}")
                    response = {"message": str(e)}
                finally:
                    TOOL_DURATION.labels(tool="patch_product_inventory").observe(time.perf_counter() - start_time)
                    ACTIVE_REQUESTS.dec()
                            
                return {
                    "response": response.get("response") if isinstance(response, dict) else None,
                    "product": product_response.model_dump(exclude_none=True),
                }
                
        #---------------------------------
        # patch_product_price
        #---------------------------------
        @self.mcp.tool()
        async def patch_product_price(payload: PatchPricePayload) -> ProductResponse | dict:
            """
            Updates a product prices.

            Use this tool when the user wants to update product prices

            The product must contain:
            - SKU
            - price with currency and amount
            """
            logger.info(f"Updating product with payload: {payload}")
                            
            with tracer.start_as_current_span("tool.patch_product_price"):
                ACTIVE_REQUESTS.inc()
                start_time = time.perf_counter()
            
                try:                                        
                    response = await self.inventory_use_case.patch_product_price(payload.model_dump())
                    
                    product_data = (
                        response.get("product")
                        if isinstance(response, dict) and "product" in response
                        else response
                    )

                    product_response = ProductResponse(
                        id=product_data.get("id") if isinstance(product_data, dict) else None,
                        sku=payload.sku,
                        name=product_data.get("name") if isinstance(product_data, dict) else None,
                        price=product_data.get("price") if isinstance(product_data, dict) else None,
                    )
                                                            
                    TOOL_CALLS.labels(tool="patch_product_price").inc()
                except Exception as e:
                    logger.error(f"Error updating product with payload {payload}: {e}")
                    TOOL_ERRORS.labels(tool="patch_product_price").inc()
                    response = {"message": str(e)}
                finally:
                    TOOL_DURATION.labels(tool="patch_product_price").observe(time.perf_counter() - start_time)
                    ACTIVE_REQUESTS.dec()

                return {
                    "response": response.get("response") if isinstance(response, dict) else None,
                    "product": product_response.model_dump(exclude_none=True),
                }  