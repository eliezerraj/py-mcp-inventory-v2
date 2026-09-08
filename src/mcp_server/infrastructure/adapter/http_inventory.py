import httpx
import logging

from config.logger import REQUEST_ID_CTX
from src.mcp_server.domain.dto.context import SecurityContext

from opentelemetry import trace, propagate
from opentelemetry.propagate import extract
from opentelemetry.context import attach, detach

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class HttpAdapterInventory():
    def __init__(self, base_url):
        logger.info(f"Initializing HttpAdapterInventory with base_url: {base_url} SUCCESSFULLY")
        self.base_url = base_url

    async def get_inventory_info(self):
        logger.info(f"Fetching inventory info")
        
        func_name = "get_inventory_info"
        url = f"{self.base_url}/v1/info"
        
        headers = {"Authorization": f"Bearer testetete",
                   "x-request-id": REQUEST_ID_CTX.get()
        }
          
        with tracer.start_as_current_span(func_name) as span:
            span.set_attribute("mcp.tool", func_name)
            span.set_attribute("request.url", url) 
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, headers=headers)
                    
                    span.set_attribute("http.status_code", response.status_code)
                    
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error fetching inventory info: {e}")
                return None

    async def get_product(self, sku):
        logger.info(f"Fetching product for sku: {sku}")
        
        func_name = "get_product"
        url = f"{self.base_url}/v1/product/{sku}"
        
        headers = {"Authorization": f"Bearer testetete",
                   "x-request-id": REQUEST_ID_CTX.get()
        }
          
        with tracer.start_as_current_span(func_name) as span:
            span.set_attribute("mcp.tool", func_name)
            span.set_attribute("request.url", url) 
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, headers=headers)
                    
                    span.set_attribute("http.status_code", response.status_code)
                    
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error fetching product for sku {sku}: {e}")
                return None

    async def post_product(self, payload):
        logger.info(f"Creating product with payload: {payload}")
        
        func_name = "post_product"
        url = f"{self.base_url}/v1/product/"
        
        headers = {"Authorization": f"Bearer testetete",
                   "x-request-id": REQUEST_ID_CTX.get()
        }
          
        with tracer.start_as_current_span(func_name) as span:
            span.set_attribute("mcp.tool", func_name)
            span.set_attribute("request.url", url) 
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(url, headers=headers, json=payload)
                    
                    span.set_attribute("http.status_code", response.status_code)
                    
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error creating product with payload {payload}: {e}")
                return None
            