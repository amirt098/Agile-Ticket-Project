from dataclasses import dataclass
from typing import List


@dataclass
class AbstractUser:
    pass


@dataclass
class Role:
    name: str
    description: str


@dataclass
class PreSetReply:
    name: str
    body: str
    user: str


@dataclass
class Organization:
    name: str
    Address: str = None
    phone: int = None
    description: str = None
    users: List[User] = None
    pre_set_replies: List[PreSetReply] = None


@dataclass
class Product:
    name: str
    owner: Organization
    description: str = None
    image: str = None
    created_at: str = None
    updated_at: str = None


@dataclass
class Ticket:
    title: str
    owner: User = None
    description: str = None
    status: str = None
    priority: str = None
    waiting_for: str = None
    closed_date: str = None
    assigned_to: User = None
    created_at: str = None
    updated_at: str = None


@dataclass
class FollowUp:
    ticket: Ticket
    date: str
    title: str
    text: str = None
    user: User = None
    created_at: str = None
    modified_at: str = None
