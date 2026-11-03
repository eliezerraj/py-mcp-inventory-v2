from pydantic import BaseModel, Field
from typing import Literal, Optional

class Price(BaseModel):
    currency: str = Field(
        description="ISO currency code, for example BRL or USD"
    )
    amount: float = Field(
        description="Product price amount"
    )

class Inventory(BaseModel):
    available: int = Field(
        default=0,
        description="Initial quantity available in inventory"
    )
    sold: int = Field(
        default=0,
        description="Quantity of product sold. Optional when creating a new product."
    )
    pending: int = Field(
        default=0,
        description="Quantity of product pending in inventory. Optional when creating a new product."
    )

class ProductPayload(BaseModel):
    sku: str = Field(
        description="Unique product SKU"
    )

    type: str = Field(
        default=None,
        description="Product type, for example food"
    )

    name: str = Field(
        default=None,
        description="Product name"
    )

    status: Literal[
        "IN-STOCK",
        "OUT-OF-STOCK",
    ] = Field(
        default=None,
        description="Current product inventory status"
    )

    lead_time: int = Field(
        default=None,
        description="Lead time in minutes"
    )

    price: Optional[Price] = Field(
        default=None,
        description="Product price details"
    )
    inventory: Optional[Inventory] = Field(
        default=None,
        description="Inventory details for the product"
    )
    
class PatchInventoryPayload(BaseModel):
    sku: str = Field(
        description="Unique product SKU"
    )

    inventory: Inventory = Field(
        description="Inventory details for the product"
    )

class PatchPricePayload(BaseModel):
    sku: str = Field(
        description="Unique product SKU"
    )

    price: Price = Field(
        description="Price details for the product"
    )
            
class ProductResponse(BaseModel):
    
    response: Optional[dict] = Field(
        default=None,
        description="Raw response from the inventory system"
    )
    
    id: Optional[int] = Field(
        default=None,
        description="Unique product ID"
    )
    
    sku: str = Field(
        description="Unique product SKU"
    )

    type: Optional[str] = Field(
        default=None,
        description="Product type, for example food"
    )

    name: Optional[str] = Field(
        default=None,
        description="Product name"
    )

    status: Optional[Literal[
        "IN-STOCK",
        "OUT-OF-STOCK",
    ]] = Field(
        default=None,
        description="Current product inventory status"
    )

    lead_time: Optional[int] = Field(
        default=None,
        description="Lead time in minutes"
    )

    price: Optional[Price] = Field(
        default=None,
        description="Product price details"
    )
    inventory: Optional[Inventory] = Field(
        default=None,
        description="Inventory details for the product"
    )