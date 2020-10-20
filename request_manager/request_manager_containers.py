from dependency_injector import providers, containers
from request_manager.api_client import ApiClient
from request_manager.api_request_manager import ApiRequestManager
from request_manager.sparql_client import SparqlClient
from request_manager.sparql_request_manager import SparqlRequestManager


class Configs(containers.DeclarativeContainer):
    """Configuration containers for dependency injection for request managers usage.
    """
    config = providers.Configuration('config')


class Clients(containers.DeclarativeContainer):
    """Client containers for dependency injection for request managers usage.
    """
    api_client = providers.Singleton(ApiClient, Configs.config)
    sparql_client = providers.Singleton(SparqlClient, Configs.config)


class Managers(containers.DeclarativeContainer):
    """Manager containers for dependency injection for request managers usage.
    """
    api_request_manager = providers.Factory(ApiRequestManager, client=Clients.api_client)
    sparql_request_manager = providers.Factory(SparqlRequestManager, client=Clients.sparql_client)
