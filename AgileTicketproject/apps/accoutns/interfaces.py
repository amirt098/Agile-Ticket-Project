import abc


class AbstractAccountsService(abc.ABC):
    def login_with_username_and_password(self, username, password):
        raise NotImplementedError

    def modify_user(self, user):
        raise NotImplementedError

    def modify_agent(self, user):
        raise NotImplementedError

    def create_agent(self, user):
        raise NotImplementedError

    def create_organization(self, organization):
        raise NotImplementedError

    def modify_organization(self, organization):
        raise NotImplementedError

    def create_role(self, role, organization):
        raise NotImplementedError

    def change_agent_role(self, role, agent):
        raise NotImplementedError

    def add_pre_set_reply(self, agent, pre_set_reply):
        raise NotImplementedError

