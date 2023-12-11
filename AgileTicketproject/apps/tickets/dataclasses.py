from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    name: str
    owner: str
    description: str = None
    image: str = None
    created_at: str = None
    updated_at: str = None


@dataclass
class Ticket:
    title: str
    owner: str
    description: str = None
    status: str = None
    priority: str = None
    waiting_for: str = None
    closed_date: str = None
    assigned_to: str = None
    created_at: str = None
    updated_at: str = None


@dataclass
class FollowUp:
    ticket: Ticket
    date: str
    title: str
    text: str = None
    user: str = None
    created_at: str = None
    modified_at: str = None









