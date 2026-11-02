import logging

logger = logging.getLogger(__name__)

def register_prompt(mcp: "MCPServer") -> None:
    """ Register all MCP prompts. """

    register_inventory_prompt(mcp)
    
def register_inventory_prompt(mcp: "MCPServer") -> None:
    """ Register inventory-related MCP prompts. """

    @mcp.prompt()
    def inventory_retrieve(sku: str) -> str:
        """ Start an inventory retrieval workflow for the given SKU. """
        
        if not sku:
            raise ValueError("SKU must be provided.")
        
        return (
            f"Retrieve the product information for SKU {sku}\n\n"
            f"Show me the product at product://{sku}\n\n"
            f"Check the current inventory information for SKU {sku}\n\n"
            f"What is the price, status, and lead time for SKU {sku}\n\n"
            f"Give me a complete summary of product {sku}, including inventory and price."
        )
        
    @mcp.prompt()
    def inventory_create(sku: str, type: str, name: str, status: str, lead_time: int, price: float, available: int, sold: int, pending: int) -> str:
        """ Start an inventory creation workflow for the given SKU. """

        if not type:
            raise ValueError("Type must be provided.")
        if not name:
            raise ValueError("Name must be provided.")
        if not status:
            raise ValueError("Status must be provided.")
        if lead_time is None:
            raise ValueError("Lead time must be provided.")
        if price is None:
            raise ValueError("Price must be provided.")
        if available is None:
            raise ValueError("Available quantity must be provided.")
        if sold is None:
            raise ValueError("Sold quantity must be provided.")
        if pending is None:
            raise ValueError("Pending quantity must be provided.")

        if not sku:
            raise ValueError("SKU must be provided.")

        return (
            f"Create a new product with SKU {sku}, of type {type}, named {name}, with status {status}, a lead time of {lead_time} days, a price of BRL {price:,.2f}, and an initial inventory quantity of {available} units, sold {sold} units, and pending {pending} units.\n\n"
            f"We are launching a new product called {name}. Create it as SKU {sku}, type {type}, {status} status, {lead_time} lead time, priced at BRL {price:,.2f}, with {available} units initially available, sold {sold} units, and pending {pending} units."
        )

    @mcp.prompt()
    def inventory_patch(sku: str, quantity: int, pending: int, sold: int) -> str:
        """ Start an inventory update workflow for the given SKU and quantity. """

        if not sku:
            raise ValueError("SKU must be provided.")
        if quantity is None:
            raise ValueError("Quantity must be provided.")
        if pending is None:
            raise ValueError("Pending quantity must be provided.")
        if sold is None:
            raise ValueError("Sold quantity must be provided.")

        return (
            f"Update the inventory for SKU {sku} with quantity {quantity}\n\n"
            f"Update the inventory for SKU {sku} with quantity {quantity} and show me all details for SKU {sku}\n\n"
            f"Sold {sold} units for SKU {sku} and update the inventory accordingly.\n\n"
            f"Adjust the inventory for SKU {sku} by {pending} units accordingly."
        )
        
    @mcp.prompt()
    def inventory_update(sku: str, status: str, type: str, price: float, lead_time: int) -> str:
        """ Start an inventory adjustment workflow for the given SKU, status, type, and price. """

        if not sku:
            raise ValueError("SKU must be provided.")
        if type is None:
            raise ValueError("Type must be provided.")
        if price is None:
            raise ValueError("Price must be provided.")
        if status is None:
            raise ValueError("Status must be provided.")
        if lead_time is None:
            raise ValueError("Lead time must be provided.")

        return (
            f"Adjust the inventory for SKU {sku} with type {type}.\n"
            f"Update the status {status} for SKU {sku}.\n"
            f"The new lead time for SKU {sku} is {lead_time} days.\n"
            f"Adjust the price for SKU {sku} to BRL {price:,.2f} and update the inventory accordingly."
        )