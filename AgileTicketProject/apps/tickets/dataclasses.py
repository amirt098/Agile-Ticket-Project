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
class Ticket:
    title: str
    owner: str
    description: str = None
    status: str = None
    priority: str = None
    assigned_to: str = None


@dataclass
class FollowUp:
    ticket: Ticket
    date: str
    title: str
    text: str = None
    user: str = None









