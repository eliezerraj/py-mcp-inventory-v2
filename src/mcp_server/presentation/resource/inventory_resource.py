import logging
import time

from opentelemetry import trace

from src.mcp_server.domain.dto.apperrs import AppError
from src.mcp_server.infrastructure.telemetry.metric import TOOL_CALLS, TOOL_DURATION, TOOL_ERRORS, ACTIVE_REQUESTS
from src.mcp_server.domain.usecase.inventory_usecase import InventoryUseCase
from src.mcp_server.config.settings import settings

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

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
                
        with tracer.start_as_current_span("resource.get_inventory_service_info"):
            ACTIVE_REQUESTS.inc()
            start_time = time.perf_counter()
                            
            try:    
                response = await inventory_use_case.get_inventory_service_info()
                TOOL_CALLS.labels(tool="inventory_service_info://").inc()
            except AppError as e:
                return e.to_dict() 
            except Exception as e:
                TOOL_ERRORS.labels(tool="inventory_service_info://").inc()
                logger.error(f"Error fetching inventory service info: {e}")
                response = {"message": str(e)}
            finally:
                TOOL_DURATION.labels(tool="inventory_service_info://").observe(time.perf_counter() - start_time)
                ACTIVE_REQUESTS.dec()

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
                
        with tracer.start_as_current_span("resource.get_product"):
            ACTIVE_REQUESTS.inc()
            start_time = time.perf_counter()
        
            try:
                response = await inventory_use_case.get_product(sku)
                TOOL_CALLS.labels(tool="product://{sku}").inc()
            except AppError as e:
                return e.to_dict() 
            except Exception as e:
                TOOL_ERRORS.labels(tool="product://{sku}").inc()
                logger.error(f"Error fetching product for sku {sku}: {e}")
                response = {"message": str(e)}
            finally:
                TOOL_DURATION.labels(tool="product://{sku}").observe(time.perf_counter() - start_time)
                ACTIVE_REQUESTS.dec()

            return response
    
    return get_inventory_service_info, get_product, mcp_info