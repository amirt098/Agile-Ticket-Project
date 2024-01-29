from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Any


@dataclass
class Product:
    name: str
    owner: str = None
    uid: str = None
    description: str = None
    image: Any = None
    pre_set_reply: str = None


@dataclass
class ProductList:
    results: List[Product]


@dataclass
class Ticket:
    title: str
    product: Product = None
    owner: str = None
    uid: str = None
    description: str = None
    status: str = None
    priority: str = None
    assigned_to: str = None
    closed_date: str = None
    created_at: str = None
    updated_at: str = None
    dead_line_date: datetime = None


@dataclass
class TicketList:
    results: List[Ticket]


@dataclass
class FollowUp:
    title: str
    ticket_uid: str = None
    date: str = None
    text: str = None
    user: str = None
    created_at: str = None
    modified_at: str = None


@dataclass
class FollowUpList:
    results: List[FollowUp]


@dataclass
class ProductFilter:
    owner: Optional[str] = None
