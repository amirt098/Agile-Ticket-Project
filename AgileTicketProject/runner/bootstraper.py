from apps.accounts.services import AccountsService
from apps.accounts.interfaces import AbstractAccountsService
from apps.tickets.interfaces import AbstractTicketServices
from apps.tickets.services import TicketService


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
