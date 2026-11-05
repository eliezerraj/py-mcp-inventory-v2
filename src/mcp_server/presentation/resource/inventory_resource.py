import logging
import time

from opentelemetry import trace

from src.mcp_server.domain.external.error_response import AppError
from src.mcp_server.domain.usecase.inventory_usecase import InventoryUseCase
from src.mcp_server.config.settings import settings
from src.mcp_server.domain.model.product import ProductResponse

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

class InventoryResource:
    
    def __init__(self, mcp: "MCPServer", inventory_use_case: InventoryUseCase):
        self.mcp = mcp
        self.inventory_use_case = inventory_use_case
        logger.info("InventoryResource initialized SUCCESSFULLY.")

    def register_inventory_resource(self):
        logger.info("Registering inventory resource SUCCESSFULLY.")
        
        @self.mcp.resource("mcp_info://")
        def mcp_info():
            """
            Provides general information about the mcp server.
            
            Use this tool when the user asks for server details or status.
            """
            logger.info("Fetching server information.")
            
            return {"status": settings.__dict__}
          
        @self.mcp.resource("inventory_service_info://")
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
                    response = await self.inventory_use_case.get_inventory_service_info()
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

        #---------------------------------
        # get_product
        #---------------------------------        
        @self.mcp.resource("product://{sku}")
        async def get_product(sku: str) -> ProductResponse | dict:
            """
            Retrieve product data for a specific SKU.

            Resource URI:
                product://{sku}

            Example:
                product://sku-102

            Returns only the product SKU, type, name, lead time.
            """
            logger.info(f"Fetching product data for sku: {sku}")
                        
            with tracer.start_as_current_span("resource.get_product"):
                ACTIVE_REQUESTS.inc()
                start_time = time.perf_counter()
                
                try:
                    response = await self.inventory_use_case.get_product(sku)
                    TOOL_CALLS.labels(tool="product://{sku}").inc()
                                        
                    product_data = (
                        response.get("product")
                        if isinstance(response, dict) and "product" in response
                        else response
                    )
                    
                    product_response = ProductResponse(
                        id=product_data.get("id") if isinstance(product_data, dict) else None,
                        sku=sku,
                        name=product_data.get("name") if isinstance(product_data, dict) else None,
                        type=product_data.get("type") if isinstance(product_data, dict) else None,
                        lead_time=product_data.get("lead_time") if isinstance(product_data, dict) else None
                    )

                except AppError as e:
                    logger.error(f"Error AppError fetching product for sku {sku}: {e}")
                    return e.to_dict() 
                except Exception as e:
                    TOOL_ERRORS.labels(tool="product://{sku}").inc()
                    logger.error(f"Error fetching product for sku {sku}: {e}")
                    return {"message": str(e)}
                finally:
                    TOOL_DURATION.labels(tool="product://{sku}").observe(time.perf_counter() - start_time)
                    ACTIVE_REQUESTS.dec()
                    
                return {
                    "response": response.get("response") if isinstance(response, dict) else None,
                    "product": product_response.model_dump(exclude_none=True),
                }    

        #---------------------------------
        # get_product_price
        #---------------------------------     
        @self.mcp.resource("product://{sku}/price")
        async def get_product_price(sku: str) -> ProductResponse | dict:
            """
            Retrieve product price for a specific SKU.

            Resource URI:
                product://{sku}/price

            Example:
                product://sku-102/price

            Returns only the product SKU, type, name, status and price.
            """
            logger.info(f"Fetching product price for sku: {sku}")
                        
            with tracer.start_as_current_span("resource.get_product_price"):
                ACTIVE_REQUESTS.inc()
                start_time = time.perf_counter()
                
                try:
                    response = await self.inventory_use_case.get_product(sku)
                    
                    product_data = (
                        response.get("product")
                        if isinstance(response, dict) and "product" in response
                        else response
                    )
                    
                    product_response = ProductResponse(
                        id=product_data.get("id") if isinstance(product_data, dict) else None,
                        sku=sku,
                        name=product_data.get("name") if isinstance(product_data, dict) else None,
                        type=product_data.get("type") if isinstance(product_data, dict) else None,
                        status=product_data.get("status") if isinstance(product_data, dict) else None,
                        price=product_data.get("price") if isinstance(product_data, dict) else None,
                    )
                    TOOL_CALLS.labels(tool="product://{sku}/price").inc()
                except AppError as e:
                    logger.error(f"Error AppError fetching price for sku {sku}: {e}")
                    return e.to_dict() 
                except Exception as e:
                    TOOL_ERRORS.labels(tool="product://{sku}/price").inc()
                    logger.error(f"Error fetching price for sku {sku}: {e}")
                    return {"message": str(e)}
                finally:
                    TOOL_DURATION.labels(tool="product://{sku}/price").observe(time.perf_counter() - start_time)
                    ACTIVE_REQUESTS.dec()
                    
                return {
                    "response": response.get("response") if isinstance(response, dict) else None,
                    "product": product_response.model_dump(exclude_none=True),
                }    

        #---------------------------------
        # get_product_inventory
        #---------------------------------     
        @self.mcp.resource("product://{sku}/inventory")
        async def get_product_inventory(sku: str) -> ProductResponse | dict:
            """
            Retrieve product inventory for a specific SKU.

            Resource URI:
                product://{sku}/inventory

            Example:
                product://sku-102/inventory

            Returns only the product SKU, type, name, status and inventory.
            """
            logger.info(f"Fetching product inventory for sku: {sku}")
                        
            with tracer.start_as_current_span("resource.get_product_inventory"):
                ACTIVE_REQUESTS.inc()
                start_time = time.perf_counter()
                
                try:
                    response = await self.inventory_use_case.get_product(sku)
                    
                    product_data = (
                        response.get("product")
                        if isinstance(response, dict) and "product" in response
                        else response
                    )
                    
                    product_response = ProductResponse(
                        id=product_data.get("id") if isinstance(product_data, dict) else None,
                        sku=sku,
                        name=product_data.get("name") if isinstance(product_data, dict) else None,
                        type=product_data.get("type") if isinstance(product_data, dict) else None,
                        status=product_data.get("status") if isinstance(product_data, dict) else None,
                        inventory=product_data.get("inventory") if isinstance(product_data, dict) else None,
                    )
                                         
                    TOOL_CALLS.labels(tool="product://{sku}/inventory").inc()
                except AppError as e:
                    logger.error(f"Error AppError fetching inventory for sku {sku}: {e}")
                    return e.to_dict() 
                except Exception as e:
                    TOOL_ERRORS.labels(tool="product://{sku}/inventory").inc()
                    logger.error(f"Error fetching inventory for sku {sku}: {e}")
                    return {"message": str(e)}
                finally:
                    TOOL_DURATION.labels(tool="product://{sku}/inventory").observe(time.perf_counter() - start_time)
                    ACTIVE_REQUESTS.dec()
                    
                return {
                    "response": response.get("response") if isinstance(response, dict) else None,
                    "product": product_response.model_dump(exclude_none=True),
                }       