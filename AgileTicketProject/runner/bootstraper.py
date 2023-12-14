from accounts.services import AccountsService
from accounts.interfaces import AbstractAccountsService
from tickets.interfaces import AbstractTicketServices
from tickets.services import TicketService


class Bootstrapper:
    def __init__(self, **kwargs) -> None:
        self._account_service = kwargs.get(
            'accounts_service',
            AccountsService()
        )
        self._ticket_service = kwargs.get(
            'accounts_service',
            TicketService()
        )

    def get_account_service(self) -> AccountsService:
        return self._account_service

    def get_ticket_service(self) -> TicketService:
        return self._ticket_service


def get_bootstrapper(**kwargs) -> Bootstrapper:
    return Bootstrapper(**kwargs)
