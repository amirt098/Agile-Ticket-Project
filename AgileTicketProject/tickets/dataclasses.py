from dataclasses import dataclass
from typing import List


@dataclass
class PreSetReply:
    name: str
    body: str
    user: str


@dataclass
class Product:
    name: str
    owner: str
    description: str = None
    image: str = None
    pre_set_replay = PreSetReply = None


@dataclass
class ProductList:
    results: List[Product]


@dataclass
class Ticket:
    title: str
    owner: str
    description: str = None
    status: str = None
    priority: str = None
    assigned_to: str = None

@dataclass
class TicketList:
    results: List[Ticket]

@dataclass
class FollowUp:
    ticket: Ticket
    date: str
    title: str
    text: str = None
    user: str = None

@dataclass
class FollowUpList:
    results: List[FollowUp]







