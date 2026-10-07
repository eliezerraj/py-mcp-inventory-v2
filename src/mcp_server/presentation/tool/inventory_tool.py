import logging
import time

from opentelemetry import trace

from src.mcp_server.infrastructure.telemetry.metric import TOOL_CALLS, ACTIVE_REQUESTS, TOOL_DURATION, TOOL_ERRORS
from src.mcp_server.domain.dto.context import SecurityContext
from src.mcp_server.domain.dto.product import ProductPayload
from src.mcp_server.domain.dto.product import PatchInventoryPayload
from src.mcp_server.domain.usecase.inventory_usecase import InventoryUseCase

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
    
def register_inventory_tool(mcp: "MCPServer", inventory_use_case: InventoryUseCase):
    logger.info("Registering inventory tool SUCCESSFULLY.")

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
                
        with tracer.start_as_current_span("tool.post_product"):
            
            ACTIVE_REQUESTS.inc()
            start_time = time.perf_counter()
        
            try:
                response = await inventory_use_case.post_product(payload.model_dump())
                TOOL_CALLS.labels(tool="post_product").inc()
            except Exception as e:
                logger.error(f"Error creating product for sku {payload.sku}: {e}")
                TOOL_ERRORS.labels(tool="post_product").inc()
                response = {"message": str(e)}
            finally:
                TOOL_DURATION.labels(tool="post_product").observe(time.perf_counter() - start_time)
                ACTIVE_REQUESTS.dec()
        
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
        logger.info(f"Updating product with payload: {payload}")
                        
        with tracer.start_as_current_span("tool.put_product"):
            ACTIVE_REQUESTS.inc()
            start_time = time.perf_counter()
        
            try:
                response = await inventory_use_case.put_product(payload.model_dump()) 
                TOOL_CALLS.labels(tool="put_product").inc()
            except Exception as e:
                logger.error(f"Error updating product with payload {payload}: {e}")
                TOOL_ERRORS.labels(tool="put_product").inc()
                response = {"message": str(e)}
            finally:
                TOOL_DURATION.labels(tool="put_product").observe(time.perf_counter() - start_time)
                ACTIVE_REQUESTS.dec()

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
        logger.info(f"Patching product with payload: {payload}")
                
        with tracer.start_as_current_span("tool.patch_product"):
            ACTIVE_REQUESTS.inc()
            start_time = time.perf_counter()
            
            try:
                response = await inventory_use_case.patch_product(payload.model_dump()) 
                TOOL_CALLS.labels(tool="patch_product").inc()
            except Exception as e:
                TOOL_ERRORS.labels(tool="patch_product").inc()
                logger.error(f"Error patching product with payload {payload}: {e}")
                response = {"message": str(e)}
            finally:
                TOOL_DURATION.labels(tool="patch_product").observe(time.perf_counter() - start_time)
                ACTIVE_REQUESTS.dec()
                        
            return response
        
    return post_product, put_product, patch_product