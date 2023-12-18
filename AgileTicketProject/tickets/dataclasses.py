from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PreSetReply:
    name: str
    body: str
    user: str


@dataclass
class Product:
    name: str
    owner: str
    uid: str = None
    description: str = None
    image: str = None
    pre_set_replay = str = None


@dataclass
class ProductList:
    results: List[Product]


@dataclass
class Ticket:
    title: str
    owner: str
    product: Product
    uid: str = None
    description: str = None
    status: str = None
    priority: str = None
    assigned_to: str = None


@dataclass
class TicketList:
    results: List[Ticket]


@dataclass
class FollowUp:
    ticket_uid: str
    date: str
    title: str
    text: str = None
    user: str = None


@dataclass
class FollowUpList:
    results: List[FollowUp]


@dataclass
class ProductFilter:
    owner: Optional[str] = None
