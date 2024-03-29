from dataclasses import dataclass
from typing import List


@dataclass
class User:
    username: str
    password: str = None
    first_name: str = None
    last_name: str = None
    email: str = None


@dataclass
class Agent:
    username: str
    password: str = None
    first_name: str = None
    last_name: str = None
    email: str = None
    organization: str = None


@dataclass
class Organization:
    name: str
    address: str = None
    phone: int = None
    description: str = None