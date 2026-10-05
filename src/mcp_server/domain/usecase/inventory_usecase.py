import logging
from src.mcp_server.domain.dto.context import SecurityContext

from opentelemetry import trace

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class InventoryUseCase:
    
    def __init__(self, http_adapter):
        logger.info("InventoryUseCase initialized SUCCESSFULLY.")
        self.http_adapter = http_adapter
            
    async def get_inventory_service_info(self):
        logger.info(f"Fetching inventory service info asynchronously")
        with tracer.start_as_current_span("usecase.get_inventory_service_info"):
            try:
                response = await self.http_adapter.request(
                    method="GET",
                    path="/v1/info",
                    params=None,
                )
            except Exception as e:
                logger.error(f"Error fetching inventory info asynchronously: {e}")
                raise e
        
        return response

    async def get_product(self, sku):
        logger.info(f"Fetching product for sku: {sku}")
        with tracer.start_as_current_span("usecase.get_product"):
            try:
                response = await self.http_adapter.request(
                    method="GET",
                    path=f"/v1/product/{sku}",
                    params=None,
                )
            except Exception as e:
                logger.error(f"Error fetching product for sku {sku}: {e}")
                raise e

        return response    
 
    async def post_product(self, payload: dict):
        logger.info(f"Creating product: {payload}")
        with tracer.start_as_current_span("usecase.post_product"):
            try:
                response = await self.http_adapter.request(
                    method="POST",
                    path="/v1/product",
                    payload=payload,
                )
            except Exception as e:
                logger.error(f"Error creating product for sku {payload.get('sku')}: {e}")
                raise e

        return response   

    async def put_product(self, payload: dict):
        logger.info(f"Updating product with payload: {payload}")
        with tracer.start_as_current_span("usecase.put_product"):
            try:
                response = await self.http_adapter.request(
                    method="PUT",
                    path=f"/v1/product/{payload.get('sku')}",
                    payload=payload,
                )
            except Exception as e:
                logger.error(f"Error updating product with payload {payload}: {e}")
                raise e

        return response
    
    async def patch_product(self, payload: dict):
        logger.info(f"Patching product with payload: {payload}")
        with tracer.start_as_current_span("usecase.patch_product"):
            try:
                response = await self.http_adapter.request(
                    method="PATCH",
                    path=f"/v1/product/inventory/{payload.get('sku')}",
                    payload=payload,
                )
            except Exception as e:
                logger.error(f"Error patching product with payload {payload}: {e}")
                raise e

        return response   