from pydantic import BaseModel, Field
from typing import Literal

class Price(BaseModel):
    currency: str = Field(
        description="ISO currency code, for example BRL or USD"
    )
    amount: float = Field(
        description="Product price amount"
    )

class Inventory(BaseModel):
    available: int = Field(
        description="Initial quantity available in inventory"
    )
    sold: int = Field(
        default=None,
        description="Quantity of product sold. Optional when creating a new product."
    )
    pending: int = Field(
        default=None,
        description="Quantity of product pending in inventory. Optional when creating a new product."
    )

class ProductPayload(BaseModel):
    sku: str = Field(
        description="Unique product SKU"
    )

    type: str = Field(
        description="Product type, for example food"
    )

    name: str = Field(
        description="Product name"
    )

    status: Literal[
        "IN-STOCK",
        "OUT-OF-STOCK",
    ] = Field(
        description="Current product inventory status"
    )

    lead_time: int = Field(
        description="Lead time in minutes"
    )

    price: Price
    inventory: Inventory
    
class PatchInventoryPayload(BaseModel):
    sku: str = Field(
        description="Unique product SKU"
    )

    inventory: Inventory = Field(
        description="Inventory details for the product"
    )