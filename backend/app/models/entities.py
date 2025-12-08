"""Domain entities for ShopSight."""

from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Article:
    """Product article entity."""
    article_id: int
    prod_name: str
    product_type_name: str
    product_group_name: str
    colour_group_name: str
    department_name: str
    section_name: str
    garment_group_name: str
    index_name: Optional[str]  # Image URL


@dataclass
class Customer:
    """Customer entity."""
    customer_id: str
    age: Optional[int]
    postal_code: Optional[str]
    club_member_status: Optional[str]
    fashion_news_frequency: Optional[str]


@dataclass
class Transaction:
    """Transaction entity."""
    transaction_id: str
    t_dat: date
    article_id: int
    customer_id: str
    price: float
    sales_channel_id: int
