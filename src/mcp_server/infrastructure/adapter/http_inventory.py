import httpx
import logging

from config.logger import REQUEST_ID_CTX
from src.mcp_server.domain.dto.context import SecurityContext

from opentelemetry import trace, propagate
from opentelemetry.propagate import extract
from opentelemetry.context import attach, detach

from src.mcp_server.infrastructure.context.request_context import (
    get_security_context,
)

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class HttpAdapterInventory():
    def __init__(self, base_url):
        logger.info(f"Initializing HttpAdapterInventory with base_url: {base_url} SUCCESSFULLY")
        self.base_url = base_url

    async def get_inventory_info(self):
        logger.info(f"Fetching inventory info")
        
        security_context = get_security_context()
        if security_context is None:
            logger.warning("Security context is not available")

        auth_token = security_context.auth_token if security_context else None
        request_id = security_context.x_request_id
        
        func_name = "get_inventory_info"
        url = f"{self.base_url}/v1/info"
        
        headers = {"Authorization": f"Bearer {auth_token}" if auth_token else "",
                   "x-request-id": request_id
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
        security_context = get_security_context()
        if security_context is None:
            logger.warning("Security context is not available")

        auth_token = security_context.auth_token if security_context else None
        request_id = security_context.x_request_id if security_context else None

        func_name = "get_product"
        url = f"{self.base_url}/v1/product/{sku}"
        
        headers = {"Authorization": f"Bearer {auth_token}" if auth_token else "",
                   "x-request-id": request_id
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
        security_context = get_security_context()
        if security_context is None:
            logger.warning("Security context is not available")

        auth_token = security_context.auth_token if security_context else None
        request_id = security_context.x_request_id if security_context else None

        func_name = "post_product"
        url = f"{self.base_url}/v1/product/"
        
        headers = {"Authorization": f"Bearer {auth_token}" if auth_token else "",
                   "x-request-id": request_id
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

    async def put_product(self, sku, payload):
        logger.info(f"Updating product with payload: {payload}")
        
        security_context = get_security_context()
        if security_context is None:
            logger.warning("Security context is not available")

        auth_token = security_context.auth_token if security_context else None
        request_id = security_context.x_request_id if security_context else None

        func_name = "put_product"
        url = f"{self.base_url}/v1/product/{sku}"
        
        headers = {"Authorization": f"Bearer {auth_token}" if auth_token else "",
                   "x-request-id": request_id
        }
          
        with tracer.start_as_current_span(func_name) as span:
            span.set_attribute("mcp.tool", func_name)
            span.set_attribute("request.url", url) 
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.put(url, headers=headers, json=payload)
                    
                    span.set_attribute("http.status_code", response.status_code)
                    
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error updating product with payload {payload}: {e}")
                return None
            
    async def patch_product(self, sku, payload):
        logger.info(f"Patching product with payload: {payload}")
        
        security_context = get_security_context()
        if security_context is None:
            logger.warning("Security context is not available")

        auth_token = security_context.auth_token if security_context else None
        request_id = security_context.x_request_id if security_context else None

        func_name = "patch_product"
        url = f"{self.base_url}/v1/product/inventory/{sku}"
        
        headers = {"Authorization": f"Bearer {auth_token}" if auth_token else "",
                   "x-request-id": request_id
        }
          
        with tracer.start_as_current_span(func_name) as span:
            span.set_attribute("mcp.tool", func_name)
            span.set_attribute("request.url", url) 
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.patch(url, headers=headers, json=payload)
                    
                    span.set_attribute("http.status_code", response.status_code)
                    
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error patching product with payload {payload}: {e}")
                return None